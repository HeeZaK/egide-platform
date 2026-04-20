from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.crypto import FieldEncryptor, decode_aes256_key_b64
from app.engines.hibp_engine import MockHibpLeakCheckClient
from app.engines.osint_engine import MockB2BEnrichmentClient, OsintEngine
from app.repositories.osint_profile_repository import OsintProfileRepository
from app.schemas.osint import OsintEnrichmentResponse


class EnrichEmailProfileUseCase:
    def __init__(self) -> None:
        self._engine = OsintEngine(enrichment_client=MockB2BEnrichmentClient())
        self._leak_checker = MockHibpLeakCheckClient()

    async def execute(
        self,
        email: EmailStr,
        *,
        persist: bool,
        db: Session | None,
    ) -> OsintEnrichmentResponse:
        profile = await self._engine.build_profile(email=email)
        leak_check = await self._leak_checker.check_breaches(email=email)

        persisted = False
        if persist:
            if db is None:
                raise ValueError("Database session is required when persist=true")
            key = decode_aes256_key_b64(settings.field_encryption_key_b64)
            if key is None:
                raise ValueError("EGIDE_FIELD_ENCRYPTION_KEY_B64 is not configured")
            repo = OsintProfileRepository(FieldEncryptor(key))
            repo.save(db, profile)
            db.commit()
            persisted = True

        return OsintEnrichmentResponse(
            profile=profile,
            leak_check=leak_check,
            persisted=persisted,
        )
