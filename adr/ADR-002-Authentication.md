# ADR-002 — Authentication

**Status:** Accepted

## Decision
V1 uses Google sign-in. Passkeys/WebAuthn are supported as a follow-on authentication method.

## Rationale
Google provides a low-friction identity flow. Passkeys can later simplify recurring access on supported devices without introducing passwords.

## Constraints
Secrets remain server-side. Authorization is always enforced by the backend.