# Expense Service

## Responsibility
Authoritative expense domain: expense lifecycle, classification references, payment split, personal share, extraordinary flag and provenance.

## Invariants
- payment components reconcile to gross total;
- personal amount cannot exceed gross amount;
- every booked PSD2 transaction maps to at most one expense;
- source/origin is traceable.

## Inputs
Manual entry, accepted PSD2 operation, committed CSV import.

## Outputs
Expense records, aggregate-ready data and domain events/activity updates where required.

## Performance
Use indexed relational queries and avoid loading complete histories unnecessarily.