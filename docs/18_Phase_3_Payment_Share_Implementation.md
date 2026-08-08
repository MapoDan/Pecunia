# Pecunia — Phase 3 Payment and Personal Share Implementation Notes

## Scope implemented

Phase 3 separates payment mechanics from economic attribution:

- `ExpensePayment` rows represent how the gross expense was paid;
- `ExpenseAllocation` rows represent who economically owns the expense share;
- create/update expense requests can submit multiple payment components;
- backend validates `sum(payments) = expense.amount` for provided splits;
- backend validates personal/effective amount is never negative and never greater than gross amount;
- when no allocation is supplied, the owner receives a default personal allocation equal to the gross amount;
- frontend exposes optional second payment component and optional personal share inputs for the mandatory examples.

## Deferred by roadmap

- Full group-member allocation semantics remain Phase 8.
- PSD2-origin payment components and bank-fee handling remain PSD2/dashboard phases.
- Dashboard consumption of `personal_amount` is implemented in Phase 4.
