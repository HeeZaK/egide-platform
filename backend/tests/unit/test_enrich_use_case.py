import pytest

from app.use_cases.enrich_email_profile import EnrichEmailProfileUseCase


@pytest.mark.asyncio
async def test_enrich_without_persist_returns_leak_check() -> None:
    uc = EnrichEmailProfileUseCase()
    r = await uc.execute(
        "alice@example.com",
        persist=False,
        db=None,
    )
    assert r.persisted is False
    assert r.profile.email == "alice@example.com"
    assert r.leak_check.breached is False
