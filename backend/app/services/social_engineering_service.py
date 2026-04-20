from __future__ import annotations

from app.engines.osint_engine import MockB2BEnrichmentClient, OsintEngine
from app.engines.social_engineering_engine import (
    MockMistralClient,
    SocialEngineeringEngine,
)
from app.schemas.osint import OsintProfile
from app.schemas.spear_phishing import SpearPhishingRequest, SpearPhishingScenario


class SocialEngineeringService:
    """
    Application service that orchestrates the full spear-phishing scenario
    generation pipeline:

        1. Build (or retrieve) the OSINT profile for the target email.
        2. Feed the profile into the SocialEngineeringEngine (Mistral LLM).
        3. Return the ready-to-persist SpearPhishingScenario.

    Dependency injection:
        Both engines are injected via their Protocol abstractions so the service
        is fully testable without network I/O.  The factory helper
        ``SocialEngineeringService.default()`` wires the mock adapters for
        local development; production wiring will swap in real HTTP clients.

    Security contract:
        - Passwords typed by phishing targets are NEVER passed through here.
        - Only a boolean click/credential flag is recorded downstream.
    """

    def __init__(
        self,
        osint_engine: OsintEngine,
        se_engine: SocialEngineeringEngine,
    ) -> None:
        self._osint_engine = osint_engine
        self._se_engine = se_engine

    # ------------------------------------------------------------------
    # Factory helper (dev / mock wiring)
    # ------------------------------------------------------------------

    @classmethod
    def default(cls) -> "SocialEngineeringService":
        """Return a service wired with mock adapters (dev / CI)."""
        return cls(
            osint_engine=OsintEngine(enrichment_client=MockB2BEnrichmentClient()),
            se_engine=SocialEngineeringEngine(llm_client=MockMistralClient()),
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def generate_scenario(
        self,
        request: SpearPhishingRequest,
    ) -> SpearPhishingScenario:
        """
        Generate a spear-phishing scenario for the target defined in *request*.

        The OSINT profile is rebuilt on-the-fly from the target email so the
        scenario is always based on the freshest available enrichment data.
        In a production setup this would first attempt a cache/DB lookup by
        ``request.osint_profile_id`` before falling back to a live enrichment.

        Args:
            request: Validated ``SpearPhishingRequest`` from the API layer.

        Returns:
            A ``SpearPhishingScenario`` ready for AES-256 encryption and
            persistence in the campaigns table.
        """
        osint_profile: OsintProfile = await self._osint_engine.build_profile(
            email=request.target_email,
        )

        return await self._se_engine.generate_scenario(
            request=request,
            osint_profile=osint_profile,
        )
