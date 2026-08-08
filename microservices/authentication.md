# Authentication Service

## Responsibility
Identity, Google OAuth/OIDC onboarding, session lifecycle, roles and future WebAuthn/passkeys.

## Owns
- external identity mapping;
- Pecunia user identity;
- role assignment;
- session/security metadata.

## Does not own
Expenses, categories, dashboards or PSD2 transactions.

## Rules
- Google is V1 login provider.
- Authorization is enforced by backend services, not the frontend.
- Passkeys are a follow-on capability using WebAuthn standards.
- Secrets remain server-side.