"""Create osint_profile_records table.

Revision ID: 001_osint_profiles
Revises:
Create Date: 2026-04-19
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "001_osint_profiles"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "osint_profile_records",
        sa.Column("profile_id", sa.String(length=36), nullable=False),
        sa.Column("email_fingerprint", sa.String(length=64), nullable=False),
        sa.Column("encrypted_sensitive_blob_b64", sa.Text(), nullable=False),
        sa.Column("source_provider", sa.String(length=60), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("profile_id"),
    )
    op.create_index(
        "ix_osint_profile_records_email_fingerprint",
        "osint_profile_records",
        ["email_fingerprint"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_osint_profile_records_email_fingerprint",
        table_name="osint_profile_records",
    )
    op.drop_table("osint_profile_records")
