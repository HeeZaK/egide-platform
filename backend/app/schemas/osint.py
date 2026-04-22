from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CompanyInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, max_length=120)
    domain: str | None = Field(default=None, max_length=120)
    employee_count: int | None = Field(default=None, ge=1)
    industry: str | None = Field(default=None, max_length=120)


class EmploymentInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, max_length=120)
    seniority: str | None = Field(default=None, max_length=60)
    department: str | None = Field(default=None, max_length=80)


class OsintProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile_id: str = Field(..., min_length=36, max_length=36)
    email: EmailStr
    full_name: str | None = Field(default=None, max_length=120)
    first_name: str | None = Field(default=None, max_length=60)
    last_name: str | None = Field(default=None, max_length=60)
    linkedin_url: str | None = Field(default=None, max_length=300)
    company: CompanyInfo | None = None
    employment: EmploymentInfo | None = None
    exposed_on_linkedin: bool = False
    breach_count: int = Field(0, ge=0, le=1000)
    breached: bool = False
    breach_includes_passwords: bool = False
    tags: list[str] = Field(default_factory=list)


class OsintEnrichmentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile: OsintProfile
    persisted: bool = False


class OsintProfileResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile: OsintProfile


class HIBPBreachSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    breached: bool
    breach_count: int = Field(ge=0, le=1000)
    breach_includes_passwords: bool = False


class LinkedInSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    found: bool
    profile_url: str | None = Field(default=None, max_length=300)
    full_name: str | None = Field(default=None, max_length=120)
    current_company: str | None = Field(default=None, max_length=120)
    current_title: str | None = Field(default=None, max_length=120)
    seniority: Literal[
        "intern",
        "junior",
        "mid",
        "senior",
        "lead",
        "manager",
        "director",
        "vp",
        "c_level",
        "unknown",
    ] = "unknown"
