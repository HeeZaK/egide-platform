from __future__ import annotations

from datetime import datetime, timezone
from typing import Protocol

from app.schemas.osint import OsintProfile
from app.schemas.spear_phishing import (
    AttackVector,
    DifficultyLevel,
    MistralRawOutput,
    SpearPhishingRequest,
    SpearPhishingScenario,
    ToneProfile,
)


# ---------------------------------------------------------------------------
# Mistral client abstraction (Protocol — Zero Trust / dependency injection)
# ---------------------------------------------------------------------------

class MistralClient(Protocol):
    """
    Abstraction for the sovereign Mistral AI adapter.

    Any concrete implementation (HTTP client, local inference, mock) must
    satisfy this interface so the engine never depends on a specific vendor.
    """

    async def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1_024,
    ) -> MistralRawOutput:
        """Send a chat completion request and return a structured output."""
        ...


# ---------------------------------------------------------------------------
# Mock Mistral client (dev / CI — no external call)
# ---------------------------------------------------------------------------

class MockMistralClient:
    """
    Deterministic mock for local development and unit tests.

    Produces a realistic-looking spear-phishing scenario from the prompts
    without any network I/O, keeping the test suite fast and offline-safe.
    """

    MODEL_VERSION = "mistral-small-mock-v1"

    async def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1_024,
    ) -> MistralRawOutput:
        # Extract a hint from the user prompt to vary the output slightly
        hint = user_prompt[:80].replace("\n", " ")

        return MistralRawOutput(
            model_version=self.MODEL_VERSION,
            prompt_tokens=len(system_prompt.split()) + len(user_prompt.split()),
            completion_tokens=148,
            subject_line="[ACTION REQUISE] Mise à jour obligatoire de vos accès VPN",
            sender_alias="Support Informatique Interne",
            body=(
                f"Bonjour,\n\n"
                f"Suite à notre audit de sécurité (contexte : {hint[:60]}…), "
                f"nous vous demandons de renouveler vos identifiants d'accès "
                f"au portail VPN d'ici ce soir 18h00.\n\n"
                f"Sans action de votre part, votre accès sera suspendu "
                f"conformément à notre politique NIS2.\n\n"
                f"Cliquez sur le lien ci-dessous pour procéder :\n"
                f"{{PAYLOAD_HOOK}}\n\n"
                f"Cordialement,\nL'équipe Sécurité SI"
            ),
            payload_hook_url="https://vpn-update.internal.example.com/renew",
        )


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

def _build_system_prompt(language: str, tone: ToneProfile) -> str:
    tone_instructions: dict[ToneProfile, str] = {
        "urgent_authority": (
            "Tu joues le rôle d'un responsable hiérarchique ou d'un service IT "
            "qui impose une action urgente sous peine de conséquences graves."
        ),
        "friendly_colleague": (
            "Tu joues le rôle d'un collègue de confiance qui demande un service "
            "de façon informelle et naturelle."
        ),
        "it_support": (
            "Tu joues le rôle du support informatique interne qui contacte "
            "l'utilisateur pour un problème technique nécessitant son action."
        ),
        "vendor_invoice": (
            "Tu joues le rôle d'un fournisseur externe relançant pour le "
            "règlement d'une facture avec des coordonnées bancaires modifiées."
        ),
        "regulatory_notice": (
            "Tu joues le rôle d'un organisme de conformité (ANSSI, CNIL, NIS2) "
            "qui notifie une obligation légale urgente."
        ),
    }

    return (
        f"Tu es un expert en ingénierie sociale opérant dans un cadre légal de "
        f"test de sensibilisation autorisé par l'entreprise cliente.\n"
        f"Langue de la réponse : {language}.\n"
        f"Registre de ton message : {tone_instructions[tone]}\n"
        f"Génère UNIQUEMENT le contenu demandé, sans explication ni commentaire. "
        f"Réponds en JSON structuré avec les clés : "
        f"subject_line, sender_alias, body, payload_hook_url."
    )


def _build_user_prompt(
    profile: OsintProfile,
    attack_vector: AttackVector,
    difficulty: DifficultyLevel,
    include_payload_hook: bool,
) -> str:
    difficulty_notes: dict[DifficultyLevel, str] = {
        "low": "Message générique, peu personnalisé, fautes mineures tolérées.",
        "medium": "Message semi-personnalisé, nom et entreprise intégrés.",
        "high": (
            "Message très personnalisé : utilise le poste, le département, "
            "le nom du manager supposé et des détails crédibles de l'entreprise."
        ),
        "expert": (
            "Message indiscernable d'un vrai email interne : ton parfait, "
            "références internes plausibles, signature réaliste, "
            "aucun indicateur de phishing évident."
        ),
    }

    hook_instruction = (
        "Inclure un lien (placeholder {{PAYLOAD_HOOK}}) naturellement intégré "
        "dans le texte."
        if include_payload_hook
        else "Ne pas inclure de lien cliquable."
    )

    return (
        f"Cible :\n"
        f"  - Prénom : {profile.first_name}\n"
        f"  - Nom    : {profile.last_name}\n"
        f"  - Poste  : {profile.employment.title}\n"
        f"  - Niveau : {profile.employment.seniority}\n"
        f"  - Départ.: {profile.employment.department}\n"
        f"  - Société: {profile.company.name} ({profile.company.industry}, "
        f"{profile.company.employee_count} employés, {profile.company.country})\n"
        f"  - LinkedIn: {profile.linkedin_url}\n\n"
        f"Vecteur d'attaque : {attack_vector}\n"
        f"Niveau de difficulté : {difficulty} — {difficulty_notes[difficulty]}\n"
        f"Lien payload : {hook_instruction}\n"
    )


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class SocialEngineeringEngine:
    """
    Orchestrates ultra-targeted spear-phishing scenario generation.

    Design principles:
        - Depends on MistralClient abstraction, never on a concrete HTTP client.
        - Stateless: receives an OsintProfile, returns a SpearPhishingScenario.
        - Security contract: NEVER stores or transmits credentials typed by
          targets. Only a boolean click / credential flag is recorded downstream
          by the campaign service.
    """

    def __init__(self, llm_client: MistralClient) -> None:
        self._llm = llm_client

    async def generate_scenario(
        self,
        request: SpearPhishingRequest,
        osint_profile: OsintProfile,
    ) -> SpearPhishingScenario:
        """
        Generate a spear-phishing scenario from a structured OSINT profile.

        Args:
            request:       Campaign-level parameters (vector, tone, difficulty…)
            osint_profile: Pre-built OsintProfile for the target.

        Returns:
            A fully populated SpearPhishingScenario, ready for persistence
            (encrypted at rest by the campaign service).
        """
        system_prompt = _build_system_prompt(
            language=request.language,
            tone=request.tone,
        )
        user_prompt = _build_user_prompt(
            profile=osint_profile,
            attack_vector=request.attack_vector,
            difficulty=request.difficulty,
            include_payload_hook=request.include_payload_hook,
        )

        llm_output: MistralRawOutput = await self._llm.complete(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        # Replace the generic placeholder with the actual hook URL if present
        body = llm_output.body
        if request.include_payload_hook and llm_output.payload_hook_url:
            body = body.replace("{PAYLOAD_HOOK}", llm_output.payload_hook_url)

        return SpearPhishingScenario(
            campaign_id=request.campaign_id,
            target_email=request.target_email,
            osint_profile_id=request.osint_profile_id,
            attack_vector=request.attack_vector,
            tone=request.tone,
            difficulty=request.difficulty,
            language=request.language,
            subject_line=llm_output.subject_line,
            body=body,
            sender_alias=llm_output.sender_alias,
            payload_hook_url=(
                llm_output.payload_hook_url
                if request.include_payload_hook
                else None
            ),
            llm_model_version=llm_output.model_version,
            prompt_tokens=llm_output.prompt_tokens,
            completion_tokens=llm_output.completion_tokens,
            generated_at=datetime.now(timezone.utc),
            tags=[
                "spear-phishing",
                f"vector:{request.attack_vector}",
                f"tone:{request.tone}",
                f"difficulty:{request.difficulty}",
                f"lang:{request.language}",
            ],
        )
