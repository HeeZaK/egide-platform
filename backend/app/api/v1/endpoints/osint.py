from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.osint import OsintEnrichmentResponse, OsintProfileResponse
from app.services.osint_service import OSINTService

router = APIRouter(prefix="/osint", tags=["OSINT"])


@router.post("/lookup", response_model=OsintEnrichmentResponse, status_code=status.HTTP_200_OK)
def enrich_osint_profile(
    email: str = Query(..., min_length=6, max_length=254),
    persist: bool = Query(False),
    db: Session = Depends(get_db),
) -> OsintEnrichmentResponse:
    service = OSINTService(db)
    return service.enrich_by_email(email=email, persist=persist)


@router.get(
    "/profiles/{profile_id}",
    response_model=OsintProfileResponse,
    status_code=status.HTTP_200_OK,
)
def get_persisted_osint_profile(
    profile_id: str,
    db: Session = Depends(get_db),
) -> OsintProfileResponse:
    try:
        parsed_profile_id = UUID(profile_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="profile_id must be a valid UUID",
        ) from exc

    service = OSINTService(db)
    result = service.get_persisted_profile(str(parsed_profile_id))
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return OsintProfileResponse(profile=result)
