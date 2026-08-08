# Pecunia — Technology Decisions

## TD-001 — PWA

**Decision:** PWA rather than native iOS/Android for V1.

**Reason:** one codebase, installable on devices, no Apple developer subscription or Mac requirement, excellent fit for a self-hosted NAS backend.

## TD-002 — Frontend

**Decision:** React + TypeScript + Vite as the preferred stack.

**Reason:** mature ecosystem, good PWA support, strong typing and low operational complexity. A materially lighter equivalent is acceptable only with documented evidence.

## TD-003 — Backend

**Decision:** Python + FastAPI.

**Reason:** lightweight, fast for I/O-heavy workloads, strong validation/OpenAPI, good Docker fit.

## TD-004 — Database

**Decision:** PostgreSQL.

**Reason:** transactional integrity, relational constraints, analytical queries, mature backup/restore tooling and modest resource requirements.

## TD-005 — Container orchestration

**Decision:** Docker Compose.

**Reason:** appropriate for a personal NAS. Kubernetes is unnecessary complexity for V1.

## TD-006 — Async jobs

**Decision:** lightweight worker + persistent job state. Avoid a dedicated broker until justified by real load or reliability requirements.

## TD-007 — PSD2

**Decision:** provider adapter abstraction. Core domain is provider-agnostic.

**Reason:** provider changes must not force domain rewrites.

## TD-008 — Authentication

**Decision:** Google login for V1; WebAuthn/passkeys as a supported follow-on capability.

## TD-009 — Search

**Decision:** PostgreSQL indexes/search capabilities for V1; no Elasticsearch/OpenSearch.

## TD-010 — Analytics

**Decision:** SQL aggregation in PostgreSQL and compact API responses; no data warehouse.

## TD-011 — Offline behavior

**Decision:** PWA app-shell/offline-readiness only in V1. Financial writes require server confirmation.

## TD-012 — Backups

**Decision:** backup and restore are backend/infrastructure responsibilities. The PWA never performs backups.

## TD-013 — Scope

**Decision:** V1 tracks expenses and related analytics only. Budgets are explicitly deferred to V2.