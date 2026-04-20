from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Principal(BaseModel):
    """Authenticated subject after JWT validation (Keycloak / OIDC)."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    sub: str = Field(min_length=1, max_length=256)
    preferred_username: str | None = Field(default=None, max_length=256)
    roles: list[str] = Field(default_factory=list, max_length=128)
