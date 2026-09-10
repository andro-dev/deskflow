from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(32), unique=True)
    label: Mapped[str] = mapped_column(String(80))

    users: Mapped[list["User"]] = relationship(
        secondary="user_roles", back_populates="roles"
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow
    )

    roles: Mapped[list[Role]] = relationship(
        secondary="user_roles", back_populates="users"
    )


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (UniqueConstraint("user_id", "role_id"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )


class Vertical(Base):
    __tablename__ = "verticals"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    jobs: Mapped[list[Job]] = relationship(back_populates="vertical")


class PlacementType(Base):
    __tablename__ = "placement_types"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    jobs: Mapped[list[Job]] = relationship(back_populates="placement_type")


class PipelineStage(Base):
    __tablename__ = "pipeline_stages"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    account: Mapped[str] = mapped_column(String(200))
    vertical_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("verticals.id"))
    placement_type_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("placement_types.id")
    )
    location: Mapped[str] = mapped_column(String(120), default="Remote")
    status: Mapped[str] = mapped_column(String(32), default="pending")
    summary: Mapped[str] = mapped_column(String(280), default="")
    description: Mapped[str] = mapped_column(String(8000), default="")
    slate_sent: Mapped[bool] = mapped_column(Boolean, default=False)

    vertical: Mapped[Vertical] = relationship(back_populates="jobs")
    placement_type: Mapped[PlacementType] = relationship(back_populates="jobs")
    applications: Mapped[list[Application]] = relationship(back_populates="job")
    slate_items: Mapped[list[SlateItem]] = relationship(back_populates="job")


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    job_id: Mapped[str] = mapped_column(String(64), ForeignKey("jobs.id"))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid, ForeignKey("users.id"), nullable=True
    )
    candidate_name: Mapped[str] = mapped_column(String(120))
    headline: Mapped[str] = mapped_column(String(200), default="")
    stage: Mapped[str] = mapped_column(String(80), default="Applied")
    fit_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    recommendation: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    owner: Mapped[str] = mapped_column(String(32), default="candidate")

    job: Mapped[Job] = relationship(back_populates="applications")


class SlateItem(Base):
    __tablename__ = "slate_items"
    __table_args__ = (UniqueConstraint("job_id", "application_id"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    job_id: Mapped[str] = mapped_column(String(64), ForeignKey("jobs.id"))
    application_id: Mapped[str] = mapped_column(String(64), ForeignKey("applications.id"))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    job: Mapped[Job] = relationship(back_populates="slate_items")
