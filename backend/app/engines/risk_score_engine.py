from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.risk import (
    RiskFactor,
    RiskInput,
    RiskScoreReport,
    score_to_grade,
)


# ---------------------------------------------------------------------------
# Weights  (must sum to 1.0)
# ---------------------------------------------------------------------------

_W_SENIORITY        = 0.20  # High-value targets carry more inherent risk
_W_EXPOSURE         = 0.10  # LinkedIn / public surface exposure
_W_BREACH           = 0.25  # HIBP breach history (count + password leak)
_W_PHISHING         = 0.30  # Actual click / credential-submission behaviour
_W_TRAINING         = 0.15  # Awareness training completion gap

assert abs((_W_SENIORITY + _W_EXPOSURE + _W_BREACH + _W_PHISHING + _W_TRAINING) - 1.0) < 1e-9


# ---------------------------------------------------------------------------
# Sub-scorers  (each returns a value in [0, 100])
# ---------------------------------------------------------------------------

def _seniority_score(seniority: str) -> float:
    """Map seniority level to an inherent exposure score."""
    table: dict[str, float] = {
        "intern":    10.0,
        "junior":    20.0,
        "mid":       30.0,
        "senior":    45.0,
        "lead":      55.0,
        "manager":   65.0,
        "director":  75.0,
        "vp":        85.0,
        "cxo":       95.0,
        "unknown":   40.0,  # Conservative default
    }
    return table.get(seniority, 40.0)


def _exposure_score(exposed_on_linkedin: bool, employee_count: int) -> float:
    """
    Public surface score.
    LinkedIn presence raises the score; smaller companies are softer targets
    because employees are often more identifiable.
    """
    base = 60.0 if exposed_on_linkedin else 20.0
    # Small companies (<50) add 15 pts; mid-size (50-500) add 5 pts; large = 0
    if employee_count < 50:
        base += 15.0
    elif employee_count < 500:
        base += 5.0
    return min(base, 100.0)


def _breach_score(breached: bool, breach_count: int, includes_passwords: bool) -> float:
    """Dark-web / HIBP exposure score."""
    if not breached:
        return 0.0
    # Base: 40 pts for any breach; +5 per additional breach (capped at 30 extra)
    base = 40.0 + min(breach_count - 1, 6) * 5.0
    # Password leaks are critical: +20 pts
    if includes_passwords:
        base += 20.0
    return min(base, 100.0)


def _phishing_score(outcomes: list) -> float:
    """Behavioural score from phishing simulation results."""
    if not outcomes:
        return 0.0  # No data → no penalty (but no credit either)
    total = len(outcomes)
    clicks = sum(1 for o in outcomes if o.clicked_link)
    creds  = sum(1 for o in outcomes if o.submitted_credentials)
    # Click rate * 60 + cred submission rate * 40
    click_rate = clicks / total
    cred_rate  = creds  / total
    return min(click_rate * 60.0 + cred_rate * 40.0, 100.0)


def _training_gap_score(completed: int, total: int) -> float:
    """Awareness gap: 0 = fully trained, 100 = no training at all."""
    if total == 0:
        return 100.0
    completion_rate = completed / total
    return round((1.0 - completion_rate) * 100.0, 2)


# ---------------------------------------------------------------------------
# Recommendation builder
# ---------------------------------------------------------------------------

def _build_recommendations(
    seniority_val:  float,
    breach_val:     float,
    phishing_val:   float,
    training_val:   float,
    includes_passwords: bool,
) -> list[str]:
    recs: list[str] = []

    if breach_val >= 40.0 and includes_passwords:
        recs.append(
            "Forcer la réinitialisation immédiate du mot de passe et activer le MFA "
            "(identifiants compromis détectés via HIBP)."
        )
    elif breach_val >= 40.0:
        recs.append(
            "Surveiller les accès anormaux : adresse e-mail présente dans au moins "
            "une fuite de données connue."
        )

    if phishing_val >= 60.0:
        recs.append(
            "Inscrire la cible à un parcours de sensibilisation anti-phishing "
            "intensif (simulation + module e-learning NIS2)."
        )
    elif phishing_val >= 30.0:
        recs.append(
            "Renforcer la vigilance face aux e-mails suspects via un rappel "
            "de bonne pratique et une simulation complémentaire."
        )

    if training_val >= 50.0:
        recs.append(
            "Compléter les modules de formation en cybersensibilisation manquants "
            "avant la prochaine évaluation périodique."
        )

    if seniority_val >= 65.0:
        recs.append(
            "Profil à haute valeur (manager+) : envisager un exercice Tabletop "
            "(War Room COMEX) pour tester la réaction face à une crise ransomware."
        )

    if not recs:
        recs.append(
            "Posture satisfaisante. Maintenir le rythme des simulations "
            "trimestrielles et des mises à jour de formation."
        )

    return recs


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class RiskScoreEngine:
    """
    Computes a Human Risk Score (0-100, grade A→F) for one individual.

    The model is a transparent weighted sum of five independent factors:
        1. Seniority          — inherent target value
        2. Public exposure    — LinkedIn / company size surface
        3. Breach history     — HIBP dark-web signals
        4. Phishing behaviour — click + credential-submission flags
        5. Training gap       — awareness completion rate

    Design principles:
        - Stateless: pure function of RiskInput → RiskScoreReport.
        - Explainable: every factor is returned with its weight and
          individual contribution so the RSSI Dashboard can drill down.
        - Secure: PhishingOutcome carries boolean flags only — no
          credential value ever enters this engine.
        - Extensible: add a new sub-scorer, register its weight, done.
    """

    def compute(self, risk_input: RiskInput) -> RiskScoreReport:
        """
        Compute the Human Risk Score from a validated ``RiskInput``.

        Returns:
            ``RiskScoreReport`` with score, grade A→F, per-factor breakdown,
            and actionable recommendations ready for the RSSI Dashboard.
        """
        # --- Sub-scores (0-100 each) ---
        sv = _seniority_score(risk_input.seniority)
        ev = _exposure_score(
            risk_input.exposed_on_linkedin,
            risk_input.company_employee_count,
        )
        bv = _breach_score(
            risk_input.breached,
            risk_input.breach_count,
            risk_input.breach_includes_passwords,
        )
        pv = _phishing_score(risk_input.phishing_outcomes)
        tv = _training_gap_score(
            risk_input.completed_training_modules,
            risk_input.total_training_modules,
        )

        # --- Weighted final score ---
        final_score = round(
            sv * _W_SENIORITY
            + ev * _W_EXPOSURE
            + bv * _W_BREACH
            + pv * _W_PHISHING
            + tv * _W_TRAINING,
            2,
        )

        grade = score_to_grade(final_score)

        factors = [
            RiskFactor(
                name="Seniority",
                description="Valeur intrinsèque de la cible selon son niveau hiérarchique.",
                weight=_W_SENIORITY,
                raw_value=round(sv, 2),
                weighted_contribution=round(sv * _W_SENIORITY, 2),
            ),
            RiskFactor(
                name="Public Exposure",
                description="Surface d'exposition publique (LinkedIn, taille de l'entreprise).",
                weight=_W_EXPOSURE,
                raw_value=round(ev, 2),
                weighted_contribution=round(ev * _W_EXPOSURE, 2),
            ),
            RiskFactor(
                name="Breach History",
                description="Exposition dans des fuites de données connues (HIBP / Dark Web).",
                weight=_W_BREACH,
                raw_value=round(bv, 2),
                weighted_contribution=round(bv * _W_BREACH, 2),
            ),
            RiskFactor(
                name="Phishing Behaviour",
                description="Taux de clics et de soumission de credentials lors des simulations.",
                weight=_W_PHISHING,
                raw_value=round(pv, 2),
                weighted_contribution=round(pv * _W_PHISHING, 2),
            ),
            RiskFactor(
                name="Training Gap",
                description="Taux d'incomplétude des modules de sensibilisation.",
                weight=_W_TRAINING,
                raw_value=round(tv, 2),
                weighted_contribution=round(tv * _W_TRAINING, 2),
            ),
        ]

        recommendations = _build_recommendations(
            seniority_val=sv,
            breach_val=bv,
            phishing_val=pv,
            training_val=tv,
            includes_passwords=risk_input.breach_includes_passwords,
        )

        return RiskScoreReport(
            target_email=risk_input.target_email,
            osint_profile_id=risk_input.osint_profile_id,
            score=final_score,
            grade=grade,
            factors=factors,
            recommendations=recommendations,
            computed_at=datetime.now(timezone.utc),
            tags=[
                "risk-score",
                f"grade:{grade}",
                f"seniority:{risk_input.seniority}",
            ],
        )
