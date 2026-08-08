"""payment split and allocations

Revision ID: 20260808_0003
Revises: 20260808_0002
Create Date: 2026-08-08
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260808_0003"
down_revision: str | None = "20260808_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "expense_payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("expense_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("payment_method_type_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("payment_method_types.id"), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("note", sa.String(length=255), nullable=True),
        sa.CheckConstraint("amount > 0", name="ck_expense_payments_amount_positive"),
    )
    op.create_index("ix_expense_payments_expense", "expense_payments", ["expense_id"])
    op.create_table(
        "expense_allocations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("expense_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("participant_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("participant_label", sa.String(length=255), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("is_owner_share", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.CheckConstraint("amount >= 0", name="ck_expense_allocations_amount_non_negative"),
    )
    op.create_index("ix_expense_allocations_expense", "expense_allocations", ["expense_id"])


def downgrade() -> None:
    op.drop_index("ix_expense_allocations_expense", table_name="expense_allocations")
    op.drop_table("expense_allocations")
    op.drop_index("ix_expense_payments_expense", table_name="expense_payments")
    op.drop_table("expense_payments")
