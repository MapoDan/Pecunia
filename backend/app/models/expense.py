import enum
import uuid
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, ForeignKey, Index, Numeric, String, Table, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ExpenseSource(str, enum.Enum):
    manual = "MANUAL"
    csv = "CSV"
    psd2 = "PSD2"


expense_tags = Table(
    "expense_tags",
    Base.metadata,
    Column("expense_id", UUID(as_uuid=True), ForeignKey("expenses.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("parent_id", "name", name="uq_categories_parent_name"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    parent: Mapped["Category | None"] = relationship(remote_side=[id], back_populates="children")
    children: Mapped[list["Category"]] = relationship(back_populates="parent")


class PaymentMethodType(Base):
    __tablename__ = "payment_method_types"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Merchant(Base):
    __tablename__ = "merchants"
    __table_args__ = (UniqueConstraint("owner_user_id", "normalized_name", name="uq_merchants_owner_normalized"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("owner_user_id", "normalized_name", name="uq_tags_owner_normalized"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)


class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = (
        Index("ix_expenses_owner_date", "owner_user_id", "transaction_date"),
        Index("ix_expenses_owner_merchant", "owner_user_id", "merchant_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="EUR")
    personal_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    source: Mapped[ExpenseSource] = mapped_column(Enum(ExpenseSource, name="expense_source"), nullable=False, default=ExpenseSource.manual)
    extraordinary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    category_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    subcategory_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    merchant_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("merchants.id"), nullable=True)
    payment_method_type_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("payment_method_types.id"), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    merchant: Mapped[Merchant | None] = relationship()
    tags: Mapped[list[Tag]] = relationship(secondary=expense_tags)
