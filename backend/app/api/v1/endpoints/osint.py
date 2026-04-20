from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.orm import Session

from app.api.deps.auth import require_rssi_principal
from app.core.config import settings
from app.core.crypto import decode_aes256_key_b64
from app.db.session import get_db
from app.schemas.auth import Principal
from app.schemas.osint import OsintEnrichmentResponse, OsintProfile
from app.services.osint_service import OsintService

router = APIRouter()


class OsintLookupRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr


def get_osint_service() -> OsintService:
    return OsintService()


@router.post("/lookup", response_model=OsintEnrichmentResponse)
async def lookup_osint_profile(
    payload: OsintLookupRequest,
    persist: bool = False,
    db: Session = Depends(get_db),
    service: OsintService = Depends(get_osint_service),
) -> OsintEnrichmentResponse:
    if persist and decode_aes256_key_b64(settings.field_encryption_key_b64) is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Persistence requires EGIDE_FIELD_ENCRYPTION_KEY_B64 "
                "(base64-encoded 32-byte AES-256 key)"
            ),
        )
    try:
        return await service.lookup_by_email(
            email=payload.email,
            persist=persist,
            db=db,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get("/profiles/{profile_id}", response_model=OsintProfile)
def get_persisted_osint_profile(
    profile_id: str,
    _principal: Principal = Depends(require_rssi_principal),
    db: Session = Depends(get_db),
    service: OsintService = Depends(get_osint_service),
) -> OsintProfile:
    if decode_aes256_key_b64(settings.field_encryption_key_b64) is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Reading persisted profiles requires EGIDE_FIELD_ENCRYPTION_KEY_B64",
        )
    try:
        profile = service.get_persisted_profile(db, profile_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    return profile
