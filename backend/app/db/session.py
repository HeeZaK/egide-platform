from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings


def _create_engine():
    url = settings.database_url
    # SQLite in-memory uses a fresh DB per connection unless we pin one connection (e.g. TestClient threads).
    if "sqlite" in url and ":memory:" in url:
        return create_engine(
            url,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
            pool_pre_ping=True,
        )
    return create_engine(url, pool_pre_ping=True)


engine = _create_engine()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
