from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl

from app.schemas.hibp import LeakCheckResult


class CompanyInfo(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=120)
    website: HttpUrl
    industry: str = Field(min_length=2, max_length=100)
    employee_count: int = Field(ge=1, le=1_000_000)
    country: str = Field(min_length=2, max_length=2, description="ISO country code")


class EmploymentInfo(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(min_length=2, max_length=120)
    seniority: Literal[
        "intern",
        "junior",
        "mid",
        "senior",
        "lead",
        "manager",
        "director",
        "vp",
        "cxo",
        "unknown",
    ]
    department: str = Field(min_length=2, max_length=120)


class B2BEnrichmentResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    provider: str = Field(min_length=2, max_length=60)
    confidence_score: float = Field(ge=0.0, le=1.0)
    full_name: str = Field(min_length=2, max_length=200)
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    linkedin_url: HttpUrl
    company: CompanyInfo
    employment: EmploymentInfo


class OsintProfile(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    profile_id: str = Field(min_length=36, max_length=36)
    email: EmailStr
    source_provider: str = Field(min_length=2, max_length=60)
    confidence_score: float = Field(ge=0.0, le=1.0)
    full_name: str = Field(min_length=2, max_length=200)
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    linkedin_url: HttpUrl
    company: CompanyInfo
    employment: EmploymentInfo
    collected_at: datetime
    tags: list[str] = Field(default_factory=list, max_length=20)


class SensitiveOsintPayload(BaseModel):
    """Subset of OSINT profile encrypted at rest (PII / high-sensitivity fields)."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    email: EmailStr
    full_name: str = Field(min_length=2, max_length=200)
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    linkedin_url: HttpUrl
    company: CompanyInfo
    employment: EmploymentInfo
    tags: list[str] = Field(default_factory=list, max_length=20)


class OsintEnrichmentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    profile: OsintProfile
    leak_check: LeakCheckResult
    persisted: bool = False
