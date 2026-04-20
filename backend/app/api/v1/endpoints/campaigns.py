from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps.auth import require_rssi_principal
from app.schemas.auth import Principal
from app.schemas.spear_phishing import SpearPhishingRequest, SpearPhishingScenario
from app.services.social_engineering_service import SocialEngineeringService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------------

def get_social_engineering_service() -> SocialEngineeringService:
    """Wire the service with mock adapters (dev).  Swap for real clients in prod."""
    return SocialEngineeringService.default()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.post(
    "/{campaign_id}/scenarios/generate",
    response_model=SpearPhishingScenario,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a spear-phishing scenario",
    description=(
        "Consumes the OSINT profile of the target and calls the sovereign Mistral "
        "LLM to produce an ultra-targeted spear-phishing scenario. "
        "Requires the **rssi** Keycloak role. "
        "**Security**: passwords typed by targets are never stored — "
        "only a boolean click/credential flag is recorded downstream."
    ),
)
async def generate_scenario(
    campaign_id: str,
    payload: SpearPhishingRequest,
    _principal: Principal = Depends(require_rssi_principal),
    service: SocialEngineeringService = Depends(get_social_engineering_service),
) -> SpearPhishingScenario:
    """
    **POST /api/v1/campaigns/{campaign_id}/scenarios/generate**

    Path parameter ``campaign_id`` must match ``payload.campaign_id``.
    This double-check prevents accidental cross-campaign scenario injection.
    """
    if payload.campaign_id != campaign_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Path campaign_id '{campaign_id}' does not match "
                f"body campaign_id '{payload.campaign_id}'"
            ),
        )

    try:
        return await service.generate_scenario(request=payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM inference error: {exc}",
        ) from exc


@router.get(
    "/{campaign_id}/scenarios",
    summary="List scenarios for a campaign (stub)",
    description=(
        "Placeholder endpoint — will return persisted scenarios once the "
        "campaigns repository layer is implemented."
    ),
)
def list_scenarios(
    campaign_id: str,
    _principal: Principal = Depends(require_rssi_principal),
) -> dict:
    return {
        "campaign_id": campaign_id,
        "scenarios": [],
        "note": "Persistence layer not yet implemented — coming in next iteration.",
    }
