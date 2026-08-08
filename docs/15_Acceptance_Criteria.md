# Pecunia — Acceptance Criteria

## Global

- [ ] All financial writes are authenticated and authorized server-side.
- [ ] Monetary calculations are deterministic and free of floating-point errors.
- [ ] Database migrations are reproducible.
- [ ] No secrets are present in repository or frontend bundle.
- [ ] Backup/restore can be performed without the PWA.

## Authentication

- [ ] User can sign in with Google.
- [ ] New user receives default configuration.
- [ ] Unauthorized user cannot access private data.
- [ ] Admin permissions are explicit.

## Expenses

- [ ] User can create an expense with minimal mandatory data.
- [ ] Category/subcategory and merchant can be suggested.
- [ ] User can use multiple payment methods for one expense.
- [ ] Payment components always reconcile to total.
- [ ] User can mark an expense extraordinary.
- [ ] User can assign tags.
- [ ] User's effective share can be lower than gross amount.

## PSD2

- [ ] Connection date defines the initial synchronization start date.
- [ ] Imported operations are PENDING and do not create expenses automatically.
- [ ] PENDING operation clearly shows originating connection/account.
- [ ] User can accept or ignore by opening the operation.
- [ ] User can change identified amount.
- [ ] User can add other payment components during booking.
- [ ] Accepted operation produces at most one expense.
- [ ] Ignored operation produces no expense.

## Activity

- [ ] Pending operations are visible in a central activity/notification area.
- [ ] Historical update suggestions require explicit user action.
- [ ] Dismissed notifications are not repeatedly shown unless a new event recreates them.

## Dashboard

- [ ] Default dashboard works for a new user.
- [ ] User can filter by period/category/payment method/merchant.
- [ ] Ordinary and extraordinary spending can be compared.
- [ ] Shared expenses use effective personal amount in personal analytics.
- [ ] Dashboard does not require full history download to the browser.

## CSV

- [ ] CSV upload does not immediately create expenses.
- [ ] User can map/validate columns and preview results.
- [ ] Historical dates are supported.
- [ ] Duplicate/error rows are reported.
- [ ] Commit is explicit.

## Groups

- [ ] User can create/join a group according to invitation rules.
- [ ] Shared/joint account can be associated with a group.
- [ ] Expenses from that shared account are scoped to the group.
- [ ] Child visibility is permission-based.
- [ ] Global tags are manageable by admin.

## Admin

- [ ] Admin can access application usage/performance dashboards.
- [ ] Admin role does not automatically expose personal financial data.

## V1 scope

- [ ] Budgets are not implemented.
- [ ] Attachments/OCR are not implemented.
- [ ] Heavy AI is not required.
- [ ] Native mobile applications are not required.