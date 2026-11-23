
import enum
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class AgentStatus(str, enum.Enum):
    ACTIF = "ACTIF"
    ARRETE = "ARRETE"


class PlanTier(str, enum.Enum):
    DECOUVERTE = "Découverte"
    ACCELERATEUR = "Accélérateur"
    GARANTI = "Garanti"


PLAN_QUOTAS: dict[PlanTier, tuple[int | None, int | None]] = {
    PlanTier.DECOUVERTE: (5, 5),
    PlanTier.ACCELERATEUR: (25, 30),
    PlanTier.GARANTI: (None, None),
}


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    agent_status = Column(Enum(AgentStatus), default=AgentStatus.ACTIF, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    consent = relationship("Consent", back_populates="user", uselist=False, cascade="all, delete-orphan")
    subscription = relationship(
        "Subscription", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    profile = relationship(
        "CandidateProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class Consent(Base):
    __tablename__ = "consents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    law_09_08_accepted = Column(Boolean, nullable=False, default=False)
    gdpr_accepted = Column(Boolean, nullable=False, default=False)
    ai_processing_accepted = Column(Boolean, nullable=False, default=False)
    policy_version = Column(String(64), nullable=False)
    consented_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    user = relationship("User", back_populates="consent")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    plan = Column(Enum(PlanTier), default=PlanTier.DECOUVERTE, nullable=False)
    max_applications = Column(Integer, nullable=True)
    max_ai_generations = Column(Integer, nullable=True)
    applications_used = Column(Integer, default=0, nullable=False)
    ai_generations_used = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    user = relationship("User", back_populates="subscription")