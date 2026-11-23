from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from typing import Any
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.models import AgentStatus, PlanTier


class ConsentInput(BaseModel):
    law_09_08_accepted: bool = Field(default=True)
    gdpr_accepted: bool = Field(default=True)
    ai_processing_accepted: bool = Field(default=True)

    @field_validator("law_09_08_accepted", "gdpr_accepted", "ai_processing_accepted")
    @classmethod
    def must_be_accepted(cls, v: bool) -> bool:
        if not v:
            raise ValueError("Le consentement explicite est requis pour créer le compte.")
        return v


class UserRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    plan: PlanTier = Field(default=PlanTier.DECOUVERTE)
    consent: ConsentInput = Field(default_factory=ConsentInput)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class UserUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ConsentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    law_09_08_accepted: bool
    gdpr_accepted: bool
    ai_processing_accepted: bool
    policy_version: str
    consented_at: datetime


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    plan: PlanTier
    max_applications: int | None
    max_ai_generations: int | None
    applications_used: int
    ai_generations_used: int
    updated_at: datetime


class SubscriptionUpdateRequest(BaseModel):
    plan: PlanTier


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    agent_status: AgentStatus
    is_active: bool
    created_at: datetime
    consent: ConsentResponse | None = None
    subscription: SubscriptionResponse | None = None


class ErasureResponse(BaseModel):
    message: str
    deleted_user_id: int
class ExperienceItem(BaseModel):
    role: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    start_date: str | None = Field(default=None, max_length=50)
    end_date: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None, max_length=2000)


class EducationItem(BaseModel):
    degree: str = Field(..., min_length=1, max_length=200)
    institution: str = Field(..., min_length=1, max_length=200)
    year: str | None = Field(default=None, max_length=50)


class LanguageItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    level: str | None = Field(default=None, max_length=100)


class PreferencesInput(BaseModel):
    target_role: str | None = Field(default=None, max_length=200)
    city: str | None = Field(default=None, max_length=150)
    contract_type: str | None = Field(default=None, max_length=100)
    remote_allowed: bool = Field(default=False)


class CandidateProfileUpdateRequest(BaseModel):
    headline: str | None = Field(default=None, max_length=200)
    summary: str | None = Field(default=None, max_length=4000)
    skills: list[str] | None = None
    experiences: list[ExperienceItem] | None = None
    educations: list[EducationItem] | None = None
    languages: list[LanguageItem] | None = None
    preferences: PreferencesInput | None = None
    is_validated: bool | None = None


class CandidateProfileValidateRequest(BaseModel):
    is_validated: bool = Field(default=True)


class CandidateProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    headline: str | None = None
    summary: str | None = None
    skills: list[str]
    experiences: list[dict[str, Any]]
    educations: list[dict[str, Any]]
    languages: list[dict[str, Any]]
    preferences: dict[str, Any]
    is_validated: bool
    validated_at: datetime | None = None
    updated_at: datetime


class ProfileDeleteResponse(BaseModel):
    message: str
    user_id: int