# Pecunia — Coding Standards

## General

Code must prioritize correctness, readability and maintainability over cleverness. Avoid premature abstraction.

## Naming

Use descriptive names. Domain terminology must match the functional specification: `Expense`, `PSD2Transaction`, `PaymentMethod`, `PersonalAmount`, `Extraordinary` etc.

## Backend

- typed Python;
- clear separation API/service/repository/domain;
- validation at boundaries;
- business rules centralized in domain/service layer;
- database access through controlled repositories/query modules;
- no SQL/business logic embedded in route handlers;
- no secrets in source;
- monetary arithmetic with Decimal/fixed minor units, never binary floats.

## Frontend

- TypeScript strictness enabled;
- feature-oriented modules;
- reusable components for repeated UI patterns;
- no business-rule duplication that can diverge from backend;
- accessible controls and keyboard/touch support;
- avoid giant components and global mutable state.

## API

- `/api/v1` versioning;
- stable response/error shapes;
- explicit request/response schemas;
- pagination for potentially large lists;
- idempotency for retryable financial commands.

## Database

- migrations are mandatory for schema changes;
- foreign keys and constraints for financial invariants where practical;
- indexes based on actual access patterns;
- no destructive migration without an explicit migration/recovery plan.

## Testing

Every domain feature requires unit tests for business rules. Critical API workflows require integration tests. Critical user journeys require E2E tests.

## Logging

Structured logs with request/correlation ID. Never log tokens, encryption keys, full bank credentials or unnecessary financial payloads.

## Dependencies

Prefer a small, maintained dependency set. New dependencies require a concrete benefit and security/license review.

## Commits

Use small conventional-style commits, e.g. `feat(expenses): add payment split validation` or `fix(psd2): prevent duplicate booking`.

## Documentation

If code changes behavior defined in `docs/`, update the relevant specification in the same change.