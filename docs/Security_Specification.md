# Pecunia — Security Specification

## Security boundary
The backend is the authoritative security boundary. The PWA is an untrusted client.

## Authentication
V1 uses Google OAuth/OIDC. Session/token handling must follow secure server-side practices. Passkeys use WebAuthn when implemented.

## Authorization
Every protected resource is checked server-side for user, group, role and ownership. Protect against IDOR/BOLA. Admin role does not automatically grant access to personal financial content.

## Data protection
- HTTPS in production;
- database and backups encrypted;
- secrets outside Git and frontend bundle;
- recovery/encryption key is shown only during the specified initialization flow;
- PWA never performs backups.

## PSD2 security
Provider credentials/tokens remain server-side. Provider adapters isolate external formats. Connection ownership is mandatory. Provider transaction identifiers are treated as untrusted external input and are validated/deduplicated.

## Input security
Validate all input server-side. Use parameterized queries/ORM. Protect against XSS, CSRF as applicable to the chosen auth model, SSRF and malicious file uploads/CSV content.

## CSV security
Limit upload size, parse defensively, validate encoding/columns/rows, reject dangerous formula content if exported later, and never execute uploaded content.

## Logging
Use structured logs and correlation IDs. Never log passwords, OAuth secrets, PSD2 tokens, encryption keys or unnecessary full financial payloads.

## Rate limiting
Apply rate limits to login, authentication callbacks, sensitive commands, import and provider synchronization endpoints.

## Container/NAS security
- private Docker network;
- database not publicly exposed;
- least-privilege containers where practical;
- pinned/reviewed images and dependencies;
- health/readiness endpoints without sensitive output;
- persistent data separated from ephemeral containers.

## Audit
Record security-sensitive and financial provenance events sufficiently to establish who/what/when/source without collecting unnecessary data.

## GDPR readiness
Support data minimization, export/deletion workflows where legally required, retention rules and clear separation between personal data and operational telemetry.

## Recovery
Backups and restores must be tested. Loss of the encryption/recovery key must be treated as a potential inability to restore protected data; there is no hidden recovery key in the PWA.