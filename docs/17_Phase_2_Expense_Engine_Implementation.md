# Pecunia — Phase 2 Expense Engine Implementation Notes

## Scope implemented

Phase 2 introduces the manual expense engine vertical slice:

- standard application category/subcategory catalog seeded on first catalog request;
- generic payment method type catalog covering card, cash, bank transfer, meal voucher, Satispay, Splitwise and other;
- personal merchants with normalized names per user;
- personal tags created during expense entry;
- authenticated CRUD endpoints for manual expenses;
- soft delete for expenses;
- server-side ownership checks for every expense read/write;
- Decimal-backed monetary fields with database check constraints for positive gross amount and personal amount bounds;
- ordinary/extraordinary flag;
- lightweight deterministic classification suggestion based on exact merchant history with fallback to `Da classificare`.

## Deferred by roadmap

- Multiple payment components and explicit allocation rows are Phase 3.
- Dashboard aggregations are Phase 4.
- PSD2 provenance, pending transactions and CSV import flows remain later phases.
- Group-global tag promotion remains Phase 8; current tags are personal only.
