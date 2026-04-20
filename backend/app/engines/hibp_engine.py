from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Protocol

from pydantic import EmailStr

from app.schemas.hibp import BreachSummary, LeakCheckResult


class HibpLeakCheckClient(Protocol):
    async def check_breaches(self, email: EmailStr) -> LeakCheckResult:
        """Return breach exposure for an email (mock or real HIBP-style API)."""


class MockHibpLeakCheckClient:
    """
    Deterministic mock of Have I Been Pwned-style breach enumeration.

    No external HTTP call; safe for CI and local development.
    """

    async def check_breaches(self, email: EmailStr) -> LeakCheckResult:
        now = datetime.now(timezone.utc)
        normalized = str(email).lower()

        if "pwned" in normalized or normalized.startswith("breached."):
            breaches = [
                BreachSummary(
                    name="MockBreach2024",
                    breach_date=date(2024, 6, 1),
                    data_classes=["Email addresses", "Names", "Passwords"],
                ),
                BreachSummary(
                    name="LegacyAggregator",
                    breach_date=date(2019, 3, 15),
                    data_classes=["Email addresses", "IP addresses"],
                ),
            ]
            return LeakCheckResult(
                email=email,
                breached=True,
                breaches=breaches,
                checked_at=now,
                source="hibp-api-mock",
            )

        return LeakCheckResult(
            email=email,
            breached=False,
            breaches=[],
            checked_at=now,
            source="hibp-api-mock",
        )
