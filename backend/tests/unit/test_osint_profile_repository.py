import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.crypto import FieldEncryptor
from app.db.base import Base
from app.engines.osint_engine import MockB2BEnrichmentClient, OsintEngine
from app.repositories.osint_profile_repository import OsintProfileRepository

import app.models  # noqa: F401


@pytest.fixture
def memory_session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    s = Session()
    try:
        yield s
    finally:
        s.close()


@pytest.mark.asyncio
async def test_repository_encrypts_and_roundtrips(memory_session) -> None:
    profile = await OsintEngine(MockB2BEnrichmentClient()).build_profile(
        email="carol.dupont@example.com"
    )
    key = bytes(range(32))
    repo = OsintProfileRepository(FieldEncryptor(key))
    repo.save(memory_session, profile)
    memory_session.commit()

    loaded = repo.get_by_profile_id(memory_session, profile.profile_id)
    assert loaded is not None
    assert loaded.email == profile.email
    assert loaded.full_name == profile.full_name
    assert loaded.company.name == profile.company.name
