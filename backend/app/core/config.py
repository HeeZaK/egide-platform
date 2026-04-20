from __future__ import annotations

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Egide HRM API"
    app_env: str = Field(default="dev", validation_alias="APP_ENV")
    app_debug: bool = False

    database_url: str = Field(
        default="postgresql+psycopg://egide:egide@localhost:5432/egide",
        validation_alias="DATABASE_URL",
    )
    field_encryption_key_b64: str | None = Field(
        default=None,
        validation_alias="EGIDE_FIELD_ENCRYPTION_KEY_B64",
        description="Base64-encoded 32-byte key for AES-256 field encryption at rest",
    )

    auto_create_tables: bool = Field(
        default=False,
        validation_alias="SQLALCHEMY_AUTO_CREATE_TABLES",
        description="If true, create tables at startup (dev only). Use Alembic in production.",
    )

    keycloak_issuer: str | None = Field(
        default=None,
        validation_alias="KEYCLOAK_ISSUER",
        description="OIDC issuer URL, e.g. https://keycloak.example/realms/egide",
    )
    keycloak_jwks_url: str | None = Field(
        default=None,
        validation_alias="KEYCLOAK_JWKS_URL",
        description="JWKS URL, e.g. .../realms/egide/protocol/openid-connect/certs",
    )
    keycloak_audience: str | None = Field(
        default=None,
        validation_alias="KEYCLOAK_AUDIENCE",
        description="Expected JWT aud (often the API client_id); optional if verify disabled",
    )
    keycloak_verify_audience: bool = Field(
        default=True,
        validation_alias="KEYCLOAK_VERIFY_AUDIENCE",
    )
    keycloak_rssi_role: str = Field(
        default="rssi",
        validation_alias="KEYCLOAK_RSSI_ROLE",
        description="Realm or client role name required for OSINT read endpoints",
    )
    auth_dev_bypass: bool = Field(
        default=False,
        validation_alias="EGIDE_AUTH_DEV_BYPASS",
        description="DEV/TEST ONLY: skip JWT and act as RSSI (never enable in production)",
    )

    cors_origins: str = Field(
        default="http://localhost:3000",
        validation_alias="CORS_ORIGINS",
        description="Comma-separated browser origins allowed by CORS (dev / SPA)",
    )

    @model_validator(mode="after")
    def reject_auth_bypass_in_production(self) -> Settings:
        if self.auth_dev_bypass and self.app_env.lower() == "prod":
            raise ValueError("EGIDE_AUTH_DEV_BYPASS cannot be true when APP_ENV=prod")
        return self


settings = Settings()
