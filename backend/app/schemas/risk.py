from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------------------------------------------------------------------------
# Grade
# ---------------------------------------------------------------------------

RiskGrade = Literal["A", "B", "C", "D", "E", "F"]


def score_to_grade(score: float) -> RiskGrade:
    """
    Map a normalized risk score (0-100) to a letter grade.

    Higher score = higher risk.

        A  0-19   Excellent posture
        B  20-39  Good posture, minor gaps
        C  40-59  Moderate risk, action recommended
        D  60-74  High risk, remediation required
        E  75-89  Critical risk
        F  90-100 Severe / immediate threat
    """
    if score < 20:
        return "A"
    if score < 40:
        return "B"
    if score < 60:
        return "C"
    if score < 75:
        return "D"
    if score < 90:
        return "E"
    return "F"


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

class PhishingOutcome(BaseModel):
    """Boolean flags only — passwords are NEVER stored or transmitted."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: str = Field(min_length=36, max_length=36)
    clicked_link: bool = False
    submitted_credentials: bool = False  # flag only — no actual creds


class RiskInput(BaseModel):
    """
    All signals required to compute a Human Risk Score for one individual.

    Security contract:
        ``PhishingOutcome`` carries boolean flags only.  No password,
        no token, no credential value ever reaches this model.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    target_email: EmailStr
    osint_profile_id: str = Field(min_length=36, max_length=36)

    # OSINT signals
    seniority: Literal[
        "intern", "junior", "mid", "senior",
        "lead", "manager", "director", "vp", "cxo", "unknown",
    ] = "unknown"
    exposed_on_linkedin: bool = False
    company_employee_count: int = Field(default=1, ge=1, le=1_000_000)

    # HIBP signals
    breached: bool = False
    breach_count: int = Field(default=0, ge=0, le=500)
    breach_includes_passwords: bool = False

    # Phishing simulation signals
    phishing_outcomes: list[PhishingOutcome] = Field(
        default_factory=list, max_length=100
    )

    # Awareness training signals
    completed_training_modules: int = Field(default=0, ge=0, le=100)
    total_training_modules: int = Field(default=1, ge=1, le=100)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

class RiskFactor(BaseModel):
    """One explainable contributor to the final risk score."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=80)
    description: str = Field(min_length=2, max_length=300)
    weight: float = Field(ge=0.0, le=1.0, description="Relative weight in the model")
    raw_value: float = Field(ge=0.0, le=100.0, description="Partial score before weighting")
    weighted_contribution: float = Field(
        ge=0.0, le=100.0, description="Contribution to the final score"
    )


class RiskScoreReport(BaseModel):
    """
    Full Human Risk Score report for one individual.

    Designed to be stored encrypted (AES-256) and displayed
    in the RSSI Dashboard with per-factor drill-down.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    report_id: str = Field(
        default_factory=lambda: str(uuid4()),
        min_length=36,
        max_length=36,
    )
    target_email: EmailStr
    osint_profile_id: str = Field(min_length=36, max_length=36)

    score: float = Field(
        ge=0.0, le=100.0,
        description="Normalized risk score: 0 (no risk) → 100 (maximum risk)",
    )
    grade: RiskGrade
    factors: list[RiskFactor]

    recommendations: list[str] = Field(
        default_factory=list,
        max_length=20,
        description="Actionable remediation steps for the RSSI",
    )
    computed_at: datetime
    tags: list[str] = Field(default_factory=list, max_length=20)


class BatchRiskScoreError(BaseModel):
    """Décrit l'échec du calcul pour un profil dans un batch."""

    model_config = ConfigDict(extra="forbid")

    index: int = Field(ge=0, description="Position du profil dans la liste d'entrée")
    target_email: str
    detail: str


class BatchRiskScoreReport(BaseModel):
    """
    FIX: Résultat d'un batch /risk/score/batch avec support des résultats partiels.

    Remplace le comportement précédent (tout-ou-rien) par :
    - ``results``  : rapports calculés avec succès
    - ``errors``   : profils en échec avec index + détail
    - ``partial``  : True si au moins un profil a échoué
    """

    model_config = ConfigDict(extra="forbid")

    results: list[RiskScoreReport]
    errors: list[BatchRiskScoreError] = Field(default_factory=list)
    partial: bool = False
    total_requested: int = Field(ge=0)
    total_computed: int = Field(ge=0)
    total_failed: int = Field(ge=0)
