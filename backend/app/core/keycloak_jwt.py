from __future__ import annotations

import time
from typing import Any

import httpx
from jose import JWTError, jwk, jwt

_jwks_cache: dict[str, tuple[float, dict[str, Any]]] = {}
_JWKS_TTL_SEC = 300.0


async def fetch_jwks(jwks_url: str) -> dict[str, Any]:
    now = time.monotonic()
    cached = _jwks_cache.get(jwks_url)
    if cached is not None and (now - cached[0]) < _JWKS_TTL_SEC:
        return cached[1]

    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url, timeout=10.0)
        response.raise_for_status()
        data = response.json()

    _jwks_cache[jwks_url] = (now, data)
    return data


def _select_jwk(jwks: dict[str, Any], kid: str | None) -> dict[str, Any] | None:
    if not kid:
        return None
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key
    return None


def roles_from_claims(claims: dict[str, Any]) -> list[str]:
    roles: list[str] = []
    realm_access = claims.get("realm_access") or {}
    if isinstance(realm_access, dict):
        roles.extend(realm_access.get("roles") or [])
    resource_access = claims.get("resource_access") or {}
    if isinstance(resource_access, dict):
        for _client_id, payload in resource_access.items():
            if isinstance(payload, dict):
                roles.extend(payload.get("roles") or [])
    return roles


async def verify_keycloak_access_token(
    token: str,
    *,
    jwks_url: str,
    issuer: str,
    audience: str | None,
    verify_audience: bool,
) -> dict[str, Any]:
    jwks = await fetch_jwks(jwks_url)
    header = jwt.get_unverified_header(token)
    kid = header.get("kid")
    key_dict = _select_jwk(jwks, kid)
    if key_dict is None:
        raise ValueError("Signing key not found in JWKS")

    pem = jwk.construct(key_dict).to_pem().decode("utf-8")
    verify_aud = bool(verify_audience and audience)
    options: dict[str, bool | str] = {
        "verify_signature": True,
        "verify_exp": True,
        "verify_aud": verify_aud,
    }

    decode_kwargs: dict[str, Any] = {
        "algorithms": ["RS256"],
        "issuer": issuer,
        "options": options,
    }
    if verify_aud:
        decode_kwargs["audience"] = audience

    try:
        claims = jwt.decode(token, pem, **decode_kwargs)
    except JWTError as exc:
        raise ValueError("Invalid or expired token") from exc

    if not isinstance(claims, dict):
        raise ValueError("Invalid token payload")

    return claims
