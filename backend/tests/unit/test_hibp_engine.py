import pytest

from app.engines.hibp_engine import MockHibpLeakCheckClient


@pytest.mark.asyncio
async def test_hibp_mock_clean_email() -> None:
    client = MockHibpLeakCheckClient()
    r = await client.check_breaches("alice@example.com")
    assert r.breached is False
    assert r.breaches == []


@pytest.mark.asyncio
async def test_hibp_mock_pwned_email() -> None:
    client = MockHibpLeakCheckClient()
    r = await client.check_breaches("pwned@example.com")
    assert r.breached is True
    assert len(r.breaches) >= 1
    assert r.breaches[0].name
