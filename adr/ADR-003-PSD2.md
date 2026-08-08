# ADR-003 — PSD2/Open Banking

**Status:** Accepted

## Decision
Use a provider-agnostic PSD2 adapter. Bank operations are imported as PENDING and require explicit user decision before becoming expenses.

## Key rules
- initial sync starts from connection date;
- multiple connections must remain distinguishable;
- user can change the amount during booking;
- user can add other payment components;
- ignore means no expense;
- acceptance is idempotent.

## Rationale
Automatic booking would create false financial records, especially for cash withdrawals, shared expenses and mixed payment methods.