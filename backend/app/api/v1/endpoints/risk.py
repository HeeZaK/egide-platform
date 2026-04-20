from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps.auth import require_rssi_principal
from app.engines.risk_score_engine import RiskScoreEngine
from app.schemas.auth import Principal
from app.schemas.risk import RiskInput, RiskScoreReport

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------------

def get_risk_score_engine() -> RiskScoreEngine:
    return RiskScoreEngine()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.post(
    "/score",
    response_model=RiskScoreReport,
    status_code=status.HTTP_200_OK,
    summary="Compute a Human Risk Score",
    description=(
        "Aggregates OSINT seniority, public exposure, HIBP breach history, "
        "phishing simulation outcomes (boolean flags only — no passwords), "
        "and awareness training completion into a normalized 0-100 risk score "
        "mapped to a letter grade (A→F). "
        "Requires the **rssi** Keycloak role."
    ),
)
def compute_risk_score(
    payload: RiskInput,
    _principal: Principal = Depends(require_rssi_principal),
    engine: RiskScoreEngine = Depends(get_risk_score_engine),
) -> RiskScoreReport:
    """
    **POST /api/v1/risk/score**

    Returns a full ``RiskScoreReport`` with:
    - Normalized score (0-100)
    - Letter grade A→F
    - Per-factor breakdown with weights and contributions
    - Actionable recommendations in French for the RSSI
    """
    try:
        return engine.compute(risk_input=payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/score/batch",
    response_model=list[RiskScoreReport],
    status_code=status.HTTP_200_OK,
    summary="Compute Human Risk Scores for multiple targets",
    description=(
        "Batch version of /risk/score. Accepts up to 200 RiskInput objects "
        "and returns a RiskScoreReport for each. Useful for department-level "
        "or company-wide scoring in the RSSI Dashboard."
    ),
)
def compute_risk_scores_batch(
    payloads: list[RiskInput],
    _principal: Principal = Depends(require_rssi_principal),
    engine: RiskScoreEngine = Depends(get_risk_score_engine),
) -> list[RiskScoreReport]:
    if not payloads:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Payload list must not be empty.",
        )
    if len(payloads) > 200:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Batch size exceeds the limit of 200 targets per request.",
        )
    try:
        return [engine.compute(risk_input=p) for p in payloads]
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
