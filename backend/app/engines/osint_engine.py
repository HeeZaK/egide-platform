from __future__ import annotations

from datetime import datetime, timezone
from typing import Protocol
from uuid import uuid4

from pydantic import EmailStr

from app.schemas.osint import B2BEnrichmentResult, CompanyInfo, EmploymentInfo, OsintProfile


class B2BEnrichmentClient(Protocol):
    """Abstraction for sovereign/third-party enrichment providers."""

    async def enrich(self, email: EmailStr) -> B2BEnrichmentResult:
        """Return enriched B2B information from an email address."""


class MockB2BEnrichmentClient:
    """
    Deterministic mock provider for local development and tests.

    This class simulates a vendor such as Apollo/Clearbit without exposing
    real external calls while keeping a realistic response shape.
    """

    async def enrich(self, email: EmailStr) -> B2BEnrichmentResult:
        local_part = str(email).split("@")[0]
        domain = str(email).split("@")[1]
        company_slug = domain.split(".")[0].capitalize()

        inferred_first_name = local_part.split(".")[0].capitalize()
        inferred_last_name = (
            local_part.split(".")[1].capitalize()
            if "." in local_part
            else "Unknown"
        )

        return B2BEnrichmentResult(
            provider="mock-b2b-provider",
            confidence_score=0.87,
            full_name=f"{inferred_first_name} {inferred_last_name}",
            first_name=inferred_first_name,
            last_name=inferred_last_name,
            linkedin_url=f"https://www.linkedin.com/in/{local_part}",
            company=CompanyInfo(
                name=company_slug,
                website=f"https://www.{domain}",
                industry="Information Technology",
                employee_count=250,
                country="FR",
            ),
            employment=EmploymentInfo(
                title="Security Program Manager",
                seniority="manager",
                department="IT Security",
            ),
        )


class OsintEngine:
    """Application engine responsible for passive, lawful OSINT enrichment."""

    def __init__(self, enrichment_client: B2BEnrichmentClient) -> None:
        self._enrichment_client = enrichment_client

    async def build_profile(self, email: EmailStr) -> OsintProfile:
        """
        Enrich an email and map it to a normalized OSINT profile.

        Security note:
            This flow is passive and does not collect credentials, tokens,
            or sensitive secrets from end users.
        """

        enrichment = await self._enrichment_client.enrich(email=email)

        return OsintProfile(
            profile_id=str(uuid4()),
            email=email,
            source_provider=enrichment.provider,
            confidence_score=enrichment.confidence_score,
            full_name=enrichment.full_name,
            first_name=enrichment.first_name,
            last_name=enrichment.last_name,
            linkedin_url=enrichment.linkedin_url,
            company=enrichment.company,
            employment=enrichment.employment,
            collected_at=datetime.now(timezone.utc),
            tags=["osint", "b2b-enrichment", "passive-recon"],
        )
