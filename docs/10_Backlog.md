# Pecunia — Product Backlog

## Priorities

- **P0**: required for a usable V1.
- **P1**: important V1 enhancement.
- **P2**: V2/future unless re-approved.

## P0 — Foundation

- P0.1 repository/documentation setup
- P0.2 Docker/NAS deployment architecture
- P0.3 Google authentication
- P0.4 user/role model
- P0.5 encrypted DB + backend restore procedure

## P0 — Expense engine

- P0.6 create/edit/list/delete expense according to domain rules
- P0.7 categories/subcategories
- P0.8 merchants
- P0.9 payment methods
- P0.10 payment split
- P0.11 effective personal share
- P0.12 extraordinary-expense flag
- P0.13 automatic suggestions/defaults

## P0 — Activity and PSD2

- P0.14 activity center
- P0.15 PSD2 connection management
- P0.16 synchronization from connection date onward
- P0.17 PENDING transaction list
- P0.18 accept/ignore workflow
- P0.19 edit PSD2 amount and add payment components
- P0.20 bank/account provenance display
- P0.21 PSD2 deduplication/idempotency

## P0 — Analytics

- P0.22 default dashboard
- P0.23 date/category/payment/merchant filters
- P0.24 ordinary vs extraordinary comparison
- P0.25 effective personal spending analytics
- P0.26 recurring behavior/merchant analysis

## P1

- P1.1 configurable dashboard sections
- P1.2 CSV historical import with preview/mapping
- P1.3 groups
- P1.4 shared/joint bank account restricted to group
- P1.5 child accounts and parental visibility
- P1.6 global tags with admin management
- P1.7 admin usage/performance dashboard
- P1.8 passkeys/WebAuthn
- P1.9 advanced notifications/activity

## P2 / V2 candidates

- budgets;
- receipts/attachments;
- OCR;
- advanced AI insights;
- native mobile wrapper;
- advanced push notifications;
- investments/wealth;
- richer offline writes.

## Implementation order

1. Foundation/authentication.
2. Expense engine.
3. Payment split/personal share.
4. Classification/suggestions.
5. Dashboard.
6. Activity center.
7. PSD2.
8. CSV import.
9. Groups/shared accounts.
10. Admin.
11. Passkeys/security hardening.

Each item is complete only when its acceptance criteria and tests are satisfied.