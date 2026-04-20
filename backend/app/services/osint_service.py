from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.schemas.osint import OsintProfile
from app.use_cases.enrich_email_profile import EnrichEmailProfileUseCase
from app.use_cases.get_osint_profile import GetOsintProfileByIdUseCase


class OsintService:
    def __init__(self) -> None:
        self._use_case = EnrichEmailProfileUseCase()
        self._get_profile = GetOsintProfileByIdUseCase()

    async def lookup_by_email(
        self,
        email: EmailStr,
        *,
        persist: bool = False,
        db: Session | None = None,
    ):
        return await self._use_case.execute(
            email=email,
            persist=persist,
            db=db,
        )

    def get_persisted_profile(self, db: Session, profile_id: str) -> OsintProfile | None:
        return self._get_profile.run(session=db, profile_id=profile_id)
