from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.crypto import FieldEncryptor, decode_aes256_key_b64
from app.repositories.osint_profile_repository import OsintProfileRepository
from app.schemas.osint import OsintProfile


class GetOsintProfileByIdUseCase:
    def run(self, session: Session, profile_id: str) -> OsintProfile | None:
        key = decode_aes256_key_b64(settings.field_encryption_key_b64)
        if key is None:
            raise ValueError("EGIDE_FIELD_ENCRYPTION_KEY_B64 is not configured")
        repo = OsintProfileRepository(FieldEncryptor(key))
        return repo.get_by_profile_id(session, profile_id)
