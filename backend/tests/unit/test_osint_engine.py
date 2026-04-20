import pytest

from app.engines.osint_engine import MockB2BEnrichmentClient, OsintEngine


@pytest.mark.asyncio
async def test_osint_engine_builds_structured_profile() -> None:
    engine = OsintEngine(enrichment_client=MockB2BEnrichmentClient())

    profile = await engine.build_profile(email="alice.martin@example.com")

    assert profile.email == "alice.martin@example.com"
    assert profile.company.name == "Example"
    assert profile.source_provider == "mock-b2b-provider"
    assert "osint" in profile.tags
