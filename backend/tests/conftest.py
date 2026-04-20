from __future__ import annotations

import base64
import os

# Bootstrap env before any `app` imports (Settings is instantiated at import time).
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault(
    "EGIDE_FIELD_ENCRYPTION_KEY_B64",
    base64.b64encode(bytes(range(32))).decode("ascii"),
)
os.environ.setdefault("EGIDE_AUTH_DEV_BYPASS", "true")
os.environ.setdefault("SQLALCHEMY_AUTO_CREATE_TABLES", "true")
