from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------------------------------------------------------------------------
# Enums / Literals
# ---------------------------------------------------------------------------

AttackVector = Literal[
    "email",
    "sms",
    "linkedin_dm",
    "phone_vishing",
    "whatsapp",
]

ToneProfile = Literal[
    "urgent_authority",   # Impersonates hierarchy / urgency
    "friendly_colleague",  # Lateral trust exploitation
    "it_support",         # Classic helpdesk pretext
    "vendor_invoice",     # BEC / supplier fraud
    "regulatory_notice",  # NIS2 / RGPD compliance lure
]

DifficultyLevel = Literal["low", "medium", "high", "expert"]


# ---------------------------------------------------------------------------
# Request
# ---------------------------------------------------------------------------

class SpearPhishingRequest(BaseModel):
    """Input parameters to generate a spear-phishing scenario."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    campaign_id: str = Field(
        min_length=36,
        max_length=36,
        description="UUID of the parent campaign",
    )
    target_email: EmailStr
    osint_profile_id: str = Field(
        min_length=36,
        max_length=36,
        description="UUID of the pre-built OsintProfile",
    )
    attack_vector: AttackVector = "email"
    tone: ToneProfile = "urgent_authority"
    difficulty: DifficultyLevel = "medium"
    language: str = Field(
        default="fr",
        min_length=2,
        max_length=5,
        description="BCP-47 language tag, e.g. 'fr', 'en'",
    )
    include_payload_hook: bool = Field(
        default=False,
        description="Append a placeholder for a BitB / QR-code payload URL",
    )


# ---------------------------------------------------------------------------
# LLM raw output (internal)
# ---------------------------------------------------------------------------

class MistralRawOutput(BaseModel):
    """Raw structured output returned by the Mistral LLM adapter."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    model_version: str = Field(min_length=3, max_length=60)
    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)
    subject_line: str = Field(
        min_length=5,
        max_length=150,
        description="Email subject or message opening hook",
    )
    body: str = Field(
        min_length=50,
        max_length=4_000,
        description="Full message body crafted by the LLM",
    )
    sender_alias: str = Field(
        min_length=2,
        max_length=120,
        description="Suggested spoofed sender display name",
    )
    payload_hook_url: str | None = Field(
        default=None,
        description="Placeholder URL injected when include_payload_hook=True",
    )


# ---------------------------------------------------------------------------
# Scenario (final output)
# ---------------------------------------------------------------------------

class SpearPhishingScenario(BaseModel):
    """
    Normalised spear-phishing scenario ready for campaign orchestration.

    Security contract:
        - Passwords typed by targets are NEVER stored here.
        - Only a boolean `click_flag` / `cred_flag` is persisted downstream.
        - This object is encrypted at rest (AES-256) in the campaigns table.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    scenario_id: str = Field(
        default_factory=lambda: str(uuid4()),
        min_length=36,
        max_length=36,
    )
    campaign_id: str = Field(min_length=36, max_length=36)
    target_email: EmailStr
    osint_profile_id: str = Field(min_length=36, max_length=36)

    attack_vector: AttackVector
    tone: ToneProfile
    difficulty: DifficultyLevel
    language: str = Field(min_length=2, max_length=5)

    subject_line: str = Field(min_length=5, max_length=150)
    body: str = Field(min_length=50, max_length=4_000)
    sender_alias: str = Field(min_length=2, max_length=120)
    payload_hook_url: str | None = None

    llm_model_version: str = Field(min_length=3, max_length=60)
    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)

    generated_at: datetime
    tags: list[str] = Field(default_factory=list, max_length=20)
