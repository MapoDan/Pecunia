"""identity foundation

Revision ID: 20260808_0001
Revises:
Create Date: 2026-08-08
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260808_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    user_role = postgresql.ENUM("user", "admin", name="user_role")
    account_status = postgresql.ENUM("active", "disabled", name="account_status")
    session_status = postgresql.ENUM("active", "revoked", "expired", name="session_status")
    user_role.create(op.get_bind(), checkfirst=True)
    account_status.create(op.get_bind(), checkfirst=True)
    session_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("google_subject", sa.String(length=255), nullable=False, unique=True),
        sa.Column("email", sa.String(length=320), nullable=False, unique=True),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False, server_default="user"),
        sa.Column("status", account_status, nullable=False, server_default="active"),
        sa.Column("personal_context_id", postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "user_settings",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("default_currency", sa.String(length=3), nullable=False, server_default="EUR"),
        sa.Column("locale", sa.String(length=16), nullable=False, server_default="it-IT"),
        sa.Column("timezone", sa.String(length=64), nullable=False, server_default="Europe/Rome"),
        sa.Column("dashboard_config", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("notification_preferences", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
    )
    op.create_table(
        "auth_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False, unique=True),
        sa.Column("csrf_token_hash", sa.String(length=128), nullable=False),
        sa.Column("status", session_status, nullable=False, server_default="active"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_auth_sessions_user_status", "auth_sessions", ["user_id", "status"])
    op.create_table(
        "audit_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("actor_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("event_type", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
    )
    op.create_index("ix_audit_events_actor_created", "audit_events", ["actor_user_id", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_audit_events_actor_created", table_name="audit_events")
    op.drop_table("audit_events")
    op.drop_index("ix_auth_sessions_user_status", table_name="auth_sessions")
    op.drop_table("auth_sessions")
    op.drop_table("user_settings")
    op.drop_table("users")
    postgresql.ENUM(name="session_status").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="account_status").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="user_role").drop(op.get_bind(), checkfirst=True)
