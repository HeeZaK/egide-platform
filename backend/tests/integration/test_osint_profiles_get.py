from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.core import config as app_config
from app.main import app


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


def test_get_persisted_profile_roundtrip(client: TestClient) -> None:
    create = client.post(
        "/api/v1/osint/lookup",
        params={"persist": "true"},
        json={"email": "roundtrip.user@example.com"},
    )
    assert create.status_code == 200, create.text
    body = create.json()
    profile_id = body["profile"]["profile_id"]

    fetched = client.get(f"/api/v1/osint/profiles/{profile_id}")
    assert fetched.status_code == 200, fetched.text
    assert fetched.json()["email"] == "roundtrip.user@example.com"
    assert fetched.json()["profile_id"] == profile_id


def test_get_profile_not_found(client: TestClient) -> None:
    r = client.get("/api/v1/osint/profiles/00000000-0000-0000-0000-000000000001")
    assert r.status_code == 404


def test_get_profile_requires_auth_when_bypass_off(client: TestClient) -> None:
    old = app_config.settings.auth_dev_bypass
    app_config.settings.auth_dev_bypass = False
    try:
        r = client.get("/api/v1/osint/profiles/00000000-0000-0000-0000-000000000002")
    finally:
        app_config.settings.auth_dev_bypass = old

    assert r.status_code == 401
