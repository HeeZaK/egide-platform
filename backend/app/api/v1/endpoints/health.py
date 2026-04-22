from __future__ import annotations

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.get(
    "/health",
    summary="Liveness / Readiness probe",
    description=(
        "Vérifie que l'API est en ligne **et** que la connexion PostgreSQL répond. "
        "Retourne HTTP 200 si tout est sain, HTTP 503 si la base est injoignable. "
        "Utilisable comme liveness/readiness probe Kubernetes."
    ),
)
def healthcheck(db: Session = Depends(get_db)) -> JSONResponse:
    """
    FIX: health check avec ping PostgreSQL.
    Était un simple {"status": "ok"} sans vérification infrastructure.
    """
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"

    overall = "ok" if db_status == "ok" else "degraded"
    http_status = status.HTTP_200_OK if db_status == "ok" else status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(
        status_code=http_status,
        content={
            "status": overall,
            "components": {
                "api": "ok",
                "database": db_status,
            },
        },
    )
