from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.core.keycloak_jwt import roles_from_claims, verify_keycloak_access_token
from app.schemas.auth import Principal

security = HTTPBearer(auto_error=False)


def _normalize_roles(roles: list[str]) -> set[str]:
    return {r.strip().lower() for r in roles if r and r.strip()}


def _principal_has_rssi(roles: list[str]) -> bool:
    required = settings.keycloak_rssi_role.strip().lower()
    return required in _normalize_roles(roles)


async def require_rssi_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> Principal:
    """
    Require a valid Keycloak JWT (RS256) with the configured RSSI realm/client role.

    Dev/test only: set EGIDE_AUTH_DEV_BYPASS=true with APP_ENV=dev|test to skip JWT
    (local tooling only; never enable in production).
    """
    if settings.auth_dev_bypass and settings.app_env in ("dev", "test"):
        return Principal(
            sub="dev-bypass",
            preferred_username="dev-bypass",
            roles=["rssi"],
        )

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    if not settings.keycloak_jwks_url or not settings.keycloak_issuer:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Keycloak JWT validation is not configured (KEYCLOAK_JWKS_URL, KEYCLOAK_ISSUER)",
        )

    try:
        claims = await verify_keycloak_access_token(
            token,
            jwks_url=settings.keycloak_jwks_url,
            issuer=settings.keycloak_issuer,
            audience=settings.keycloak_audience,
            verify_audience=settings.keycloak_verify_audience,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    roles = roles_from_claims(claims)
    if not _principal_has_rssi(roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing required role: {settings.keycloak_rssi_role}",
        )

    sub = str(claims.get("sub") or "")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing sub")

    preferred = claims.get("preferred_username")
    pref_str = str(preferred) if preferred is not None else None

    return Principal(sub=sub, preferred_username=pref_str, roles=roles)
