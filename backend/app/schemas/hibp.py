from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BreachSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=128)
    breach_date: date | None = None
    data_classes: list[str] = Field(default_factory=list, max_length=32)


class LeakCheckResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    email: EmailStr
    breached: bool
    breaches: list[BreachSummary] = Field(default_factory=list, max_length=64)
    checked_at: datetime
    source: str = Field(default="hibp-api-mock", max_length=64)
