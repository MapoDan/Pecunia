# Pecunia — Data Model

## Purpose
Canonical logical data model for V1. The implementation may choose physical names/types, but must preserve the semantics and invariants below.

## Core entities

- **User** — Pecunia account linked to Google identity; may have role USER or ADMIN.
- **UserSettings** — user preferences and configurable defaults.
- **Category** — hierarchical expense classification (category/subcategory).
- **Merchant** — normalized merchant/store reference.
- **PaymentMethodType** — generic payment method such as card, cash, bank transfer, Satispay, meal voucher, Splitwise; it must not be tied to a specific card/account unless explicitly required for PSD2 provenance.
- **Tag** — personal tag that can become global according to group/admin rules.
- **Expense** — a financially sustained expense recorded manually or from an accepted PSD2 transaction/import.
- **ExpensePayment** — one component of the payment split of an expense.
- **ExpenseParticipant/Allocation** — records the user's effective share when an expense is shared with other people.
- **PSD2Connection** — an Open Banking connection, including provider, bank/account identity and connection start date.
- **PSD2Transaction** — imported bank operation, initially PENDING and never automatically booked as an expense.
- **ActivityItem** — actionable notification/activity, including pending PSD2 operations and historical update suggestions.
- **Group** — shared financial context.
- **GroupMembership** — user membership and permissions in a group.
- **GroupAccount** — account assigned to a group, including the shared/joint account use case.
- **ImportJob / ImportRow** — CSV import lifecycle and row-level validation/result.
- **ExchangeRate** — rate used for a transaction date/currency conversion; the applied rate must remain historically deterministic.
- **BankFee** — fee charged by the bank and associated with the relevant operation/expense where applicable.
- **AuditEvent** — security/domain events requiring traceability.

## Expense semantics

An expense has:

- transaction date;
- amount and currency;
- category/subcategory;
- merchant/store (optional but strongly suggested);
- one or more payment components;
- effective personal amount;
- optional tag(s);
- one-time/extraordinary flag;
- source metadata (manual, CSV, PSD2);
- optional PSD2 provenance;
- optional bank fee;
- notes only if useful.

### Required-data principle
Only information strictly necessary to record an expense is mandatory. The UI must prefill optional values through suggestions.

## Payment split

Example:

```text
Expense total = €50
Meal voucher  = €20
Card          = €30
```

The sum of payment components must equal the expense total.

For a PSD2 transaction of €5 where the real expense was €15:

```text
Expense total = €15
Card          = €5  (PSD2 provenance)
Meal voucher  = €10
```

The accepted PSD2 amount may therefore be changed during booking.

## Personal share

If the total expense is €10 and another person owes €5, the user's effective amount is €5. Dashboard personal-spending figures must use the effective personal amount, not blindly the gross expense amount.

## Extraordinary expenses

A boolean/domain classification identifies one-time/extraordinary expenses such as house purchase or furniture. They remain in the ledger but can be excluded from ordinary-spending analytics.

## PSD2 lifecycle

```text
PENDING -> ACCEPTED
PENDING -> IGNORED
```

PENDING operations are not expenses. ACCEPTED creates/updates one Expense. IGNORED creates no expense.

A unique provider transaction identifier plus connection identity must prevent duplicates.

## Groups

A group may contain multiple users and optionally one or more shared accounts. A joint bank account can be assigned to a group so its expenses are visible/recorded in that group only.

Parents may have visibility over children's expenses according to group permissions. This must be explicit authorization, not implicit global access.

## Tags

A user's personal tag can be promoted to global scope when used in a group. The administrator can keep, rename, merge/modify where supported, or delete global tags according to business rules.

## IDs and money

- Use opaque stable IDs (UUID or equivalent).
- Monetary values must never rely on binary floating point.
- Currency is ISO 4217.
- Timestamps representing instants are UTC; business dates retain the relevant user/account timezone semantics.

## Integrity constraints

At minimum:

- payment split sum equals expense total;
- personal amount is between zero and gross amount;
- accepted PSD2 transaction maps to at most one expense;
- PSD2 connection ownership/group access is enforced;
- foreign users cannot read or mutate another user's data;
- group-only data cannot leak into personal context;
- historical exchange rate used by an expense is immutable unless an explicit correction workflow exists.

## V1 exclusions

No budget entities, investments, receipts/attachments, OCR or wealth management entities are required in V1.