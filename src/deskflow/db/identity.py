from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from deskflow.db.engine import session_factory
from deskflow.db.models import Role, User, UserRole
from deskflow.db.passwords import hash_password, verify_password

ROLE_PRIORITY = ("exec", "admin", "recruiter", "client", "candidate")


def primary_role(codes: list[str]) -> str:
    for code in ROLE_PRIORITY:
        if code in codes:
            return code
    return codes[0] if codes else "visitor"


def authenticate(email: str, password: str) -> dict[str, Any] | None:
    db = session_factory()()
    try:
        user = db.scalar(
            select(User)
            .options(selectinload(User.roles))
            .where(User.email == email.strip().lower())
        )
        if user is None or not user.active:
            return None
        if not verify_password(password, user.password_hash):
            return None
        codes = [role.code for role in user.roles]
        return {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "roles": codes,
            "role": primary_role(codes),
        }
    finally:
        db.close()


def register_user(email: str, name: str, role_code: str, password: str) -> dict[str, Any] | None:
    db = session_factory()()
    try:
        email_n = email.strip().lower()
        if db.scalar(select(User.id).where(User.email == email_n)):
            return None
        role = db.scalar(select(Role).where(Role.code == role_code))
        if role is None:
            return None
        user = User(
            email=email_n,
            name=name.strip() or email_n,
            password_hash=hash_password(password),
            active=True,
        )
        db.add(user)
        db.flush()
        db.add(UserRole(user_id=user.id, role_id=role.id))
        db.commit()
        return {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "role": role_code,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def list_users() -> list[dict[str, Any]]:
    db = session_factory()()
    try:
        users = db.scalars(select(User).options(selectinload(User.roles)).order_by(User.email)).all()
        return [
            {
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "active": user.active,
                "roles": sorted(role.code for role in user.roles),
            }
            for user in users
        ]
    finally:
        db.close()


def list_role_rows() -> list[dict[str, str]]:
    db = session_factory()()
    try:
        rows = db.scalars(select(Role).order_by(Role.code)).all()
        return [{"id": str(row.id), "code": row.code, "label": row.label} for row in rows]
    finally:
        db.close()


def user_by_id(user_id: str) -> dict[str, Any] | None:
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        return None
    db = session_factory()()
    try:
        user = db.get(User, uid)
        if user is None or not user.active:
            return None
        return {"id": str(user.id), "email": user.email, "name": user.name}
    finally:
        db.close()


def set_user_roles(user_id: str, role_codes: list[str]) -> dict[str, Any] | None:
    db = session_factory()()
    try:
        user = db.get(User, uuid.UUID(user_id))
        if user is None:
            return None
        db.execute(delete(UserRole).where(UserRole.user_id == user.id))
        roles = db.scalars(select(Role).where(Role.code.in_(role_codes))).all()
        for role in roles:
            db.add(UserRole(user_id=user.id, role_id=role.id))
        db.commit()
        loaded = db.scalar(
            select(User).options(selectinload(User.roles)).where(User.id == user.id)
        )
        assert loaded is not None
        codes = [role.code for role in loaded.roles]
        return {
            "id": str(loaded.id),
            "email": loaded.email,
            "name": loaded.name,
            "roles": sorted(codes),
            "role": primary_role(codes),
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
