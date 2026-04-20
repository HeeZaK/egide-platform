from __future__ import annotations

import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.crypto import FieldEncryptor
from app.models.osint_profile_record import OsintProfileRecord
from app.schemas.osint import OsintProfile, SensitiveOsintPayload


def email_fingerprint(email: str) -> str:
    return hashlib.sha256(email.lower().strip().encode("utf-8")).hexdigest()


class OsintProfileRepository:
    """Persists OSINT profiles with AES-256-GCM encrypted PII blob."""

    def __init__(self, encryptor: FieldEncryptor) -> None:
        self._encryptor = encryptor

    def save(self, session: Session, profile: OsintProfile) -> None:
        payload = SensitiveOsintPayload(
            email=profile.email,
            full_name=profile.full_name,
            first_name=profile.first_name,
            last_name=profile.last_name,
            linkedin_url=profile.linkedin_url,
            company=profile.company,
            employment=profile.employment,
            tags=profile.tags,
        )
        plaintext = payload.model_dump_json().encode("utf-8")
        blob_b64 = self._encryptor.encrypt_to_b64(plaintext)

        row = OsintProfileRecord(
            profile_id=profile.profile_id,
            email_fingerprint=email_fingerprint(str(profile.email)),
            encrypted_sensitive_blob_b64=blob_b64,
            source_provider=profile.source_provider,
            confidence_score=profile.confidence_score,
            collected_at=profile.collected_at,
        )
        session.merge(row)
        session.flush()

    def get_by_profile_id(self, session: Session, profile_id: str) -> OsintProfile | None:
        stmt = select(OsintProfileRecord).where(OsintProfileRecord.profile_id == profile_id)
        row = session.scalars(stmt).first()
        if row is None:
            return None

        plaintext = self._encryptor.decrypt_from_b64(row.encrypted_sensitive_blob_b64)
        payload = SensitiveOsintPayload.model_validate_json(plaintext.decode("utf-8"))

        return OsintProfile(
            profile_id=row.profile_id,
            email=payload.email,
            source_provider=row.source_provider,
            confidence_score=row.confidence_score,
            full_name=payload.full_name,
            first_name=payload.first_name,
            last_name=payload.last_name,
            linkedin_url=payload.linkedin_url,
            company=payload.company,
            employment=payload.employment,
            collected_at=row.collected_at,
            tags=payload.tags,
        )
