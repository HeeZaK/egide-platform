from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps.auth import require_rssi_principal
from app.engines.risk_score_engine import RiskScoreEngine
from app.schemas.auth import Principal
from app.schemas.risk import RiskInput, RiskScoreReport

router = APIRouter()

_BATCH_MAX = 200


def get_risk_score_engine() -> RiskScoreEngine:
    return RiskScoreEngine()


@router.post(
    "/score",
    response_model=RiskScoreReport,
    status_code=status.HTTP_200_OK,
    summary="Calcule un Score de Risque Humain",
    description=(
        "Agrège la séniorité OSINT, l'exposition publique, l'historique HIBP, "
        "les résultats de simulation de phishing (flags booléens uniquement — aucun mot de passe), "
        "et la complétion des modules de sensibilisation en un score normalisé 0-100 "
        "mappé à une note (A→F). "
        "Requiert le rôle Keycloak **rssi**."
    ),
)
def compute_risk_score(
    payload: RiskInput,
    _principal: Principal = Depends(require_rssi_principal),
    engine: RiskScoreEngine = Depends(get_risk_score_engine),
) -> RiskScoreReport:
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
    summary="Calcule les Scores de Risque Humain pour plusieurs cibles",
    description=(
        f"Version batch de /risk/score. Accepte jusqu'à {_BATCH_MAX} objets RiskInput "
        "et retourne un RiskScoreReport pour chacun. Utile pour le scoring par département "
        "ou à l'échelle de l'entreprise depuis le Dashboard RSSI."
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
            detail="La liste de payloads ne doit pas être vide.",
        )
    if len(payloads) > _BATCH_MAX:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Maximum {_BATCH_MAX} profils par batch (reçu : {len(payloads)}).",
        )
    results: list[RiskScoreReport] = []
    errors: list[str] = []
    for i, p in enumerate(payloads):
        try:
            results.append(engine.compute(risk_input=p))
        except ValueError as exc:
            errors.append(f"[{i}] {p.target_email}: {exc}")
    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Certains profils ont échoué au calcul", "errors": errors},
        )
    return results
