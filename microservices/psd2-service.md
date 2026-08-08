# PSD2 Service

## Responsibility
Open Banking connections, provider adapters, consent/synchronization and normalized bank transactions.

## Critical rule
PSD2 discovery is not accounting. A discovered operation is PENDING until the user explicitly accepts it.

## Initial synchronization
The connection creation date is the starting point for automatic retrieval. Historical CSV/manual imports are independent and may predate the connection.

## Acceptance
When accepting a PENDING operation the user can:
- confirm/change amount;
- add payment components;
- set classification/tags;
- set personal share;
- then commit one expense.

## Provenance
Every PSD2 operation displays its originating connection/bank account identity.

## Reliability
Provider transaction identifiers, connection ID and idempotency rules prevent duplicates. Provider-specific details stay behind an adapter interface.