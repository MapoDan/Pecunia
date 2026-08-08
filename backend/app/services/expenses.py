import re
import uuid
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

from app.models.expense import Category, Expense, ExpenseAllocation, ExpensePayment, ExpenseSource, Merchant, PaymentMethodType, Tag
from app.models.identity import AuditEvent, User, utcnow
from app.schemas.expense import ExpenseCreate, ExpenseUpdate

DEFAULT_PAYMENT_METHODS = [
    ("card", "Carta"),
    ("cash", "Contanti"),
    ("bank_transfer", "Bonifico"),
    ("meal_voucher", "Buono pasto"),
    ("satispay", "Satispay"),
    ("splitwise", "Splitwise"),
    ("other", "Altro"),
]

DEFAULT_CATEGORIES = {
    "Da classificare": ["Da classificare"],
    "Alimentari": ["Supermercato", "Ristorante", "Bar"],
    "Casa": ["Affitto e mutuo", "Utenze", "Arredi"],
    "Trasporti": ["Carburante", "Mezzi pubblici", "Taxi"],
    "Salute": ["Farmacia", "Visite mediche"],
    "Tempo libero": ["Intrattenimento", "Sport"],
}


def normalize_name(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().casefold())


def quantize_money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def ensure_catalog(db: Session) -> None:
    for code, name in DEFAULT_PAYMENT_METHODS:
        if db.scalar(select(PaymentMethodType).where(PaymentMethodType.code == code)) is None:
            db.add(PaymentMethodType(code=code, name=name))
    for category_name, children in DEFAULT_CATEGORIES.items():
        parent = db.scalar(select(Category).where(Category.parent_id.is_(None), Category.name == category_name))
        if parent is None:
            parent = Category(name=category_name)
            db.add(parent)
            db.flush()
        for child_name in children:
            child = db.scalar(select(Category).where(Category.parent_id == parent.id, Category.name == child_name))
            if child is None:
                db.add(Category(name=child_name, parent_id=parent.id))


def get_or_create_merchant(db: Session, user: User, name: str | None) -> Merchant | None:
    if not name:
        return None
    normalized = normalize_name(name)
    merchant = db.scalar(select(Merchant).where(Merchant.owner_user_id == user.id, Merchant.normalized_name == normalized))
    if merchant is None:
        merchant = Merchant(owner_user_id=user.id, name=name.strip(), normalized_name=normalized)
        db.add(merchant)
        db.flush()
    return merchant


def get_or_create_tags(db: Session, user: User, names: list[str]) -> list[Tag]:
    tags: list[Tag] = []
    for raw_name in names:
        name = raw_name.strip()
        if not name:
            continue
        normalized = normalize_name(name)
        tag = db.scalar(select(Tag).where(Tag.owner_user_id == user.id, Tag.normalized_name == normalized))
        if tag is None:
            tag = Tag(owner_user_id=user.id, name=name, normalized_name=normalized)
            db.add(tag)
            db.flush()
        tags.append(tag)
    return tags


def validate_payment_method(db: Session, payment_method_type_id: uuid.UUID | None) -> None:
    if payment_method_type_id is not None and db.get(PaymentMethodType, payment_method_type_id) is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Payment method not found")


def payment_total(amounts: list[Decimal]) -> Decimal:
    return sum((quantize_money(amount) for amount in amounts), Decimal("0.00"))


def validate_payment_split(db: Session, amount: Decimal, payment_method_type_id: uuid.UUID | None, payments: list) -> list[ExpensePayment]:
    if not payments:
        if payment_method_type_id is None:
            return []
        validate_payment_method(db, payment_method_type_id)
        return [ExpensePayment(payment_method_type_id=payment_method_type_id, amount=amount)]
    split_total = payment_total([payment.amount for payment in payments])
    if split_total != amount:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Payment split total must equal expense amount")
    result: list[ExpensePayment] = []
    for payment in payments:
        validate_payment_method(db, payment.payment_method_type_id)
        result.append(ExpensePayment(payment_method_type_id=payment.payment_method_type_id, amount=quantize_money(payment.amount), note=payment.note))
    return result


def build_allocations(user: User, amount: Decimal, personal_amount: Decimal | None, allocations: list) -> tuple[Decimal, list[ExpenseAllocation]]:
    if allocations:
        owner_total = Decimal("0.00")
        built: list[ExpenseAllocation] = []
        for allocation in allocations:
            allocation_amount = quantize_money(allocation.amount)
            if allocation_amount > amount:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Allocation cannot exceed expense amount")
            if allocation.is_owner_share:
                owner_total += allocation_amount
            built.append(ExpenseAllocation(participant_user_id=user.id if allocation.is_owner_share else None, participant_label=allocation.participant_label.strip(), amount=allocation_amount, is_owner_share=allocation.is_owner_share))
        if owner_total > amount:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Personal amount cannot exceed expense amount")
        return owner_total, built
    effective_personal = quantize_money(personal_amount if personal_amount is not None else amount)
    if effective_personal > amount:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Personal amount cannot exceed expense amount")
    return effective_personal, [ExpenseAllocation(participant_user_id=user.id, participant_label="Personale", amount=effective_personal, is_owner_share=True)]


def validate_category_pair(db: Session, category_id: uuid.UUID | None, subcategory_id: uuid.UUID | None) -> None:
    if category_id is None and subcategory_id is not None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Subcategory requires a category")
    if category_id is not None and db.get(Category, category_id) is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Category not found")
    if subcategory_id is not None:
        subcategory = db.get(Category, subcategory_id)
        if subcategory is None or subcategory.parent_id != category_id:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Subcategory does not belong to category")


def serialize_expense(expense: Expense) -> dict[str, object]:
    return {
        "id": expense.id,
        "amount": expense.amount,
        "personal_amount": expense.personal_amount,
        "currency": expense.currency,
        "description": expense.description,
        "transaction_date": expense.transaction_date,
        "extraordinary": expense.extraordinary,
        "source": expense.source.value,
        "category_id": expense.category_id,
        "subcategory_id": expense.subcategory_id,
        "merchant_name": getattr(expense, "merchant", None).name if getattr(expense, "merchant", None) else None,
        "payment_method_type_id": expense.payment_method_type_id,
        "payments": [{"payment_method_type_id": payment.payment_method_type_id, "amount": payment.amount, "note": payment.note} for payment in expense.payments],
        "allocations": [{"participant_label": allocation.participant_label, "amount": allocation.amount, "is_owner_share": allocation.is_owner_share} for allocation in expense.allocations],
        "tags": [tag.name for tag in expense.tags],
        "notes": expense.notes,
    }


def create_expense(db: Session, user: User, payload: ExpenseCreate) -> Expense:
    validate_category_pair(db, payload.category_id, payload.subcategory_id)
    amount = quantize_money(payload.amount)
    payments = validate_payment_split(db, amount, payload.payment_method_type_id, payload.payments)
    personal_amount, allocations = build_allocations(user, amount, payload.personal_amount, payload.allocations)
    merchant = get_or_create_merchant(db, user, payload.merchant_name or payload.description)
    tags = get_or_create_tags(db, user, payload.tags)
    expense = Expense(
        owner_user_id=user.id,
        amount=amount,
        personal_amount=personal_amount,
        currency=payload.currency,
        transaction_date=payload.transaction_date,
        description=payload.description.strip(),
        extraordinary=payload.extraordinary,
        category_id=payload.category_id,
        subcategory_id=payload.subcategory_id,
        merchant_id=merchant.id if merchant else None,
        payment_method_type_id=payload.payment_method_type_id,
        source=ExpenseSource.manual,
        notes=payload.notes,
    )
    expense.payments = payments
    expense.allocations = allocations
    expense.tags = tags
    db.add(expense)
    db.flush()
    db.add(AuditEvent(actor_user_id=user.id, event_type="expenses.expense_created", metadata_json={"expense_id": str(expense.id), "source": "MANUAL"}))
    return expense


def owned_expense_query(user: User) -> Select[tuple[Expense]]:
    return select(Expense).where(Expense.owner_user_id == user.id, Expense.deleted_at.is_(None)).options(selectinload(Expense.tags), selectinload(Expense.payments), selectinload(Expense.allocations), selectinload(Expense.merchant))


def get_owned_expense(db: Session, user: User, expense_id: uuid.UUID) -> Expense:
    expense = db.scalar(owned_expense_query(user).where(Expense.id == expense_id))
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


def update_expense(db: Session, user: User, expense_id: uuid.UUID, payload: ExpenseUpdate) -> Expense:
    expense = get_owned_expense(db, user, expense_id)
    category_id = payload.category_id if payload.category_id is not None else expense.category_id
    subcategory_id = payload.subcategory_id if payload.subcategory_id is not None else expense.subcategory_id
    validate_category_pair(db, category_id, subcategory_id)
    effective_amount = quantize_money(payload.amount) if payload.amount is not None else expense.amount
    if payload.payments is not None:
        expense.payments = validate_payment_split(db, effective_amount, payload.payment_method_type_id, payload.payments)
    elif payload.payment_method_type_id is not None:
        expense.payments = validate_payment_split(db, effective_amount, payload.payment_method_type_id, [])
    elif payload.amount is not None:
        if len(expense.payments) == 1:
            expense.payments[0].amount = effective_amount
        elif expense.payments:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Updated amount requires a reconciled payment split")
    if payload.allocations is not None or payload.personal_amount is not None:
        expense.personal_amount, expense.allocations = build_allocations(user, effective_amount, payload.personal_amount, payload.allocations or [])
    elif payload.amount is not None and expense.personal_amount > effective_amount:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Personal amount cannot exceed expense amount")
    if payload.amount is not None:
        expense.amount = effective_amount
    if payload.description is not None:
        expense.description = payload.description.strip()
    if payload.transaction_date is not None:
        expense.transaction_date = payload.transaction_date
    if payload.currency is not None:
        expense.currency = payload.currency
    if payload.extraordinary is not None:
        expense.extraordinary = payload.extraordinary
    expense.category_id = category_id
    expense.subcategory_id = subcategory_id
    if payload.merchant_name is not None:
        merchant = get_or_create_merchant(db, user, payload.merchant_name)
        expense.merchant_id = merchant.id if merchant else None
    if payload.payment_method_type_id is not None:
        expense.payment_method_type_id = payload.payment_method_type_id
    if payload.tags is not None:
        expense.tags = get_or_create_tags(db, user, payload.tags)
    if payload.notes is not None:
        expense.notes = payload.notes
    db.add(AuditEvent(actor_user_id=user.id, event_type="expenses.expense_updated", metadata_json={"expense_id": str(expense.id)}))
    return expense


def delete_expense(db: Session, user: User, expense_id: uuid.UUID) -> None:
    expense = get_owned_expense(db, user, expense_id)
    expense.deleted_at = utcnow()
    db.add(AuditEvent(actor_user_id=user.id, event_type="expenses.expense_deleted", metadata_json={"expense_id": str(expense.id)}))


def suggest_for_text(db: Session, user: User, text: str) -> dict[str, object]:
    normalized = normalize_name(text)
    merchant = db.scalar(select(Merchant).where(Merchant.owner_user_id == user.id, Merchant.normalized_name == normalized))
    if merchant:
        latest = db.scalar(select(Expense).where(Expense.owner_user_id == user.id, Expense.merchant_id == merchant.id, Expense.deleted_at.is_(None)).order_by(Expense.transaction_date.desc()))
        if latest:
            return {"merchant_name": merchant.name, "category_id": latest.category_id, "subcategory_id": latest.subcategory_id, "payment_method_type_id": latest.payment_method_type_id, "reason": "exact merchant history"}
    fallback = db.scalar(select(Category).where(Category.name == "Da classificare", Category.parent_id.is_(None)))
    fallback_child = db.scalar(select(Category).where(Category.parent_id == fallback.id).limit(1)) if fallback else None
    return {"merchant_name": text.strip() or None, "category_id": fallback.id if fallback else None, "subcategory_id": fallback_child.id if fallback_child else None, "payment_method_type_id": None, "reason": "default unclassified"}
