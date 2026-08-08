# Pecunia — API Design

## 1. Principles

- REST/JSON over HTTPS.
- Versioned base path: `/api/v1`.
- Backend is authoritative for authorization and business rules.
- Consistent error format and request/correlation ID.
- Pagination and server-side filtering for large lists.
- Idempotency for financial operations that can be retried.

## 2. Resource groups

Representative V1 resources:

```text
/auth
/users/me
/expenses
/categories
/subcategories
/merchants
/payment-methods
/tags
/activity
/psd2/connections
/psd2/transactions
/imports
/groups
/group-accounts
/dashboard
/admin
/settings
```

The exact endpoint list must be kept synchronized with the functional/data specifications.

## 3. Expense API

Required operations:

- create expense;
- read expense;
- update expense;
- delete/archive according to domain rules;
- list/filter/search;
- manage payment split;
- manage personal share;
- manage classification/tags.

Create/update requests must validate all monetary invariants server-side.

## 4. PSD2 API

Required operations:

- create/manage connection;
- list connections;
- start synchronization;
- list PENDING operations;
- accept/book a pending operation;
- ignore a pending operation;
- retrieve provenance/source account;
- refresh/sync status.

Accepting a PENDING operation must be one atomic domain operation capable of modifying the amount and payment split before creating the Expense.

## 5. Activity API

The activity center exposes:

- pending PSD2 operations;
- historical-update suggestions;
- actionable system items.

An activity item can be completed, dismissed or remain pending according to its type.

## 6. Dashboard API

Dashboard endpoints must return compact aggregates rather than raw expense history. Filters include date range, category, subcategory, tag, payment method, group/context and extraordinary-expense inclusion/exclusion.

## 7. Import API

Flow:

```text
upload -> validate -> preview -> map -> commit
```

The upload alone must not create financial records.

## 8. Group API

Required operations:

- create group;
- invite/remove members;
- assign roles/visibility;
- create/link shared account;
- list group expenses;
- manage global tags within group.

Authorization is evaluated for every request.

## 9. Error contract

Use a consistent shape:

```json
{
  "error": {
    "code": "DOMAIN_ERROR_CODE",
    "message": "Human-readable message",
    "request_id": "opaque-id",
    "details": {}
  }
}
```

Do not expose stack traces or secrets.

## 10. Idempotency

Financial commands should accept an idempotency key when a duplicate request could create duplicate accounting records. Provider transaction IDs must be unique within their PSD2 connection/provider namespace.

## 11. Authentication

V1 login uses Google. Session/token implementation must follow `09_Security_Specification.md`. Passkey registration/authentication is a planned supported capability and must not weaken the Google onboarding path.

## 12. API documentation

The implementation should generate OpenAPI from the authoritative backend contract. Changes to the API require updating this document and relevant user stories/business rules.