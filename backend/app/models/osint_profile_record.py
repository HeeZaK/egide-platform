from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class OsintProfileRecord(Base):
    __tablename__ = "osint_profile_records"

    profile_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email_fingerprint: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    encrypted_sensitive_blob_b64: Mapped[str] = mapped_column(Text, nullable=False)
    source_provider: Mapped[str] = mapped_column(String(60), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
