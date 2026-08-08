# Pecunia — Phase 1 Identity Implementation Notes

## Scope implemented

Phase 1 introduces the backend identity foundation required before financial features:

- Google OIDC login endpoint accepting an ID token and verifying it server-side against Google tokeninfo;
- first-login user creation with default settings;
- application role model with `USER` and `ADMIN`;
- active/disabled account status;
- server-side session persistence with opaque HttpOnly cookie tokens stored only as HMAC hashes;
- CSRF token issued to the client for state-changing authenticated commands;
- logout/session revocation;
- `GET /api/v1/auth/me` protected profile endpoint;
- audit events for user creation, session creation and session revocation;
- personal context UUID distinct from shared groups, preparing FR-006 without modeling shared groups yet.

## Deferred by roadmap

- Passkeys/WebAuthn remain in Phase 11.
- Groups and group memberships remain in Phase 8.
- Financial authorization checks will be added together with the first financial resources; the current foundation exposes no financial writes.
