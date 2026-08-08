# ADR-001 — PWA

**Status:** Accepted

## Context
Pecunia must run on phones without requiring a native iOS build, Mac or Apple Developer subscription, while the backend remains self-hosted on the NAS.

## Decision
Use a Progressive Web App as the V1 client.

## Consequences
+ One frontend codebase.
+ Installable on supported devices.
+ Easy NAS hosting.
+ No App Store dependency.
- Some native capabilities and offline behavior are more limited than a native app.

V1 financial writes require server confirmation.