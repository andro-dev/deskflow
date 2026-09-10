"""identity, catalog, and staffing loop tables

Revision ID: 001_identity
Revises:
Create Date: 2026-09-10
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001_identity"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("label", sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("role_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
        sa.UniqueConstraint("user_id", "role_id"),
    )
    op.create_table(
        "verticals",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "placement_types",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "pipeline_stages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "jobs",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("account", sa.String(length=200), nullable=False),
        sa.Column("vertical_id", sa.Uuid(), nullable=False),
        sa.Column("placement_type_id", sa.Uuid(), nullable=False),
        sa.Column("location", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("summary", sa.String(length=280), nullable=False),
        sa.Column("description", sa.String(length=8000), nullable=False),
        sa.Column("slate_sent", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["placement_type_id"], ["placement_types.id"]),
        sa.ForeignKeyConstraint(["vertical_id"], ["verticals.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "applications",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("job_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("candidate_name", sa.String(length=120), nullable=False),
        sa.Column("headline", sa.String(length=200), nullable=False),
        sa.Column("stage", sa.String(length=80), nullable=False),
        sa.Column("fit_score", sa.Integer(), nullable=True),
        sa.Column("recommendation", sa.String(length=32), nullable=True),
        sa.Column("owner", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "slate_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("job_id", sa.String(length=64), nullable=False),
        sa.Column("application_id", sa.String(length=64), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["application_id"], ["applications.id"]),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("job_id", "application_id"),
    )


def downgrade() -> None:
    op.drop_table("slate_items")
    op.drop_table("applications")
    op.drop_table("jobs")
    op.drop_table("pipeline_stages")
    op.drop_table("placement_types")
    op.drop_table("verticals")
    op.drop_table("user_roles")
    op.drop_table("users")
    op.drop_table("roles")
