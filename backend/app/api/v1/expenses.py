import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.expense import Category, Expense, PaymentMethodType
from app.models.identity import User
from app.schemas.expense import CategoryResponse, ExpenseCreate, ExpenseResponse, ExpenseUpdate, PaymentMethodTypeResponse, SuggestionResponse
from app.services.auth import current_user
from app.services.expenses import create_expense, delete_expense, ensure_catalog, get_owned_expense, owned_expense_query, serialize_expense, suggest_for_text, update_expense

router = APIRouter(tags=["expenses"])


@router.get("/categories", response_model=list[CategoryResponse])
def categories(db: Session = Depends(get_db), user: User = Depends(current_user)) -> list[Category]:
    ensure_catalog(db)
    db.commit()
    return list(db.scalars(select(Category).where(Category.parent_id.is_(None), Category.is_active.is_(True)).options(selectinload(Category.children)).order_by(Category.name)))


@router.get("/payment-methods", response_model=list[PaymentMethodTypeResponse])
def payment_methods(db: Session = Depends(get_db), user: User = Depends(current_user)) -> list[PaymentMethodType]:
    ensure_catalog(db)
    db.commit()
    return list(db.scalars(select(PaymentMethodType).where(PaymentMethodType.is_active.is_(True)).order_by(PaymentMethodType.name)))


@router.get("/classification/suggestions", response_model=SuggestionResponse)
def suggestions(q: str = Query(min_length=1, max_length=255), db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    ensure_catalog(db)
    db.commit()
    return suggest_for_text(db, user, q)


@router.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create(payload: ExpenseCreate, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    ensure_catalog(db)
    expense = create_expense(db, user, payload)
    db.commit()
    db.refresh(expense)
    return serialize_expense(get_owned_expense(db, user, expense.id))


@router.get("/expenses", response_model=list[ExpenseResponse])
def list_expenses(
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
    date_from: date | None = None,
    date_to: date | None = None,
    extraordinary: bool | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[dict[str, object]]:
    query = owned_expense_query(user)
    if date_from is not None:
        query = query.where(Expense.transaction_date >= date_from)
    if date_to is not None:
        query = query.where(Expense.transaction_date <= date_to)
    if extraordinary is not None:
        query = query.where(Expense.extraordinary.is_(extraordinary))
    expenses = db.scalars(query.order_by(Expense.transaction_date.desc(), Expense.created_at.desc()).limit(limit).offset(offset)).all()
    return [serialize_expense(expense) for expense in expenses]


@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get(expense_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    return serialize_expense(get_owned_expense(db, user, expense_id))


@router.patch("/expenses/{expense_id}", response_model=ExpenseResponse)
def patch(expense_id: uuid.UUID, payload: ExpenseUpdate, db: Session = Depends(get_db), user: User = Depends(current_user)) -> dict[str, object]:
    expense = update_expense(db, user, expense_id, payload)
    db.commit()
    return serialize_expense(expense)


@router.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(expense_id: uuid.UUID, response: Response, db: Session = Depends(get_db), user: User = Depends(current_user)) -> Response:
    delete_expense(db, user, expense_id)
    db.commit()
    return response
