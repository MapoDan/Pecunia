from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    parent_id: UUID | None = None
    children: list["CategoryResponse"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class PaymentMethodTypeResponse(BaseModel):
    id: UUID
    code: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class ExpensePaymentInput(BaseModel):
    payment_method_type_id: UUID
    amount: Decimal = Field(gt=Decimal("0"), max_digits=14, decimal_places=2)
    note: str | None = Field(default=None, max_length=255)


class ExpensePaymentResponse(BaseModel):
    payment_method_type_id: UUID
    amount: Decimal
    note: str | None


class ExpenseAllocationInput(BaseModel):
    participant_label: str = Field(min_length=1, max_length=255)
    amount: Decimal = Field(ge=Decimal("0"), max_digits=14, decimal_places=2)
    is_owner_share: bool = False


class ExpenseAllocationResponse(BaseModel):
    participant_label: str
    amount: Decimal
    is_owner_share: bool


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(gt=Decimal("0"), max_digits=14, decimal_places=2)
    description: str = Field(min_length=1, max_length=500)
    transaction_date: date
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    extraordinary: bool = False
    category_id: UUID | None = None
    subcategory_id: UUID | None = None
    merchant_name: str | None = Field(default=None, max_length=255)
    payment_method_type_id: UUID | None = None
    payments: list[ExpensePaymentInput] = Field(default_factory=list)
    personal_amount: Decimal | None = Field(default=None, ge=Decimal("0"), max_digits=14, decimal_places=2)
    allocations: list[ExpenseAllocationInput] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    notes: str | None = None

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()


class ExpenseUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=Decimal("0"), max_digits=14, decimal_places=2)
    description: str | None = Field(default=None, min_length=1, max_length=500)
    transaction_date: date | None = None
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    extraordinary: bool | None = None
    category_id: UUID | None = None
    subcategory_id: UUID | None = None
    merchant_name: str | None = Field(default=None, max_length=255)
    payment_method_type_id: UUID | None = None
    payments: list[ExpensePaymentInput] | None = None
    personal_amount: Decimal | None = Field(default=None, ge=Decimal("0"), max_digits=14, decimal_places=2)
    allocations: list[ExpenseAllocationInput] | None = None
    tags: list[str] | None = None
    notes: str | None = None

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str | None) -> str | None:
        return value.upper() if value else value


class ExpenseResponse(BaseModel):
    id: UUID
    amount: Decimal
    currency: str
    description: str
    transaction_date: date
    extraordinary: bool
    source: str
    category_id: UUID | None
    subcategory_id: UUID | None
    merchant_name: str | None
    payment_method_type_id: UUID | None
    payments: list[ExpensePaymentResponse]
    personal_amount: Decimal
    allocations: list[ExpenseAllocationResponse]
    tags: list[str]
    notes: str | None


class SuggestionResponse(BaseModel):
    merchant_name: str | None = None
    category_id: UUID | None = None
    subcategory_id: UUID | None = None
    payment_method_type_id: UUID | None = None
    reason: str
