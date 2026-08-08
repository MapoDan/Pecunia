# Pecunia — System Architecture

## 1. Target
PWA mobile-first + backend on the user's NAS, deployed with Docker Compose. The architecture is modular and microservice-ready but deliberately lightweight.

## 2. Logical topology

```text
Internet/LAN
    |
Reverse Proxy / HTTPS
    |
    +---- PWA (static frontend)
    |
    +---- API
             |
       +-----+------------------+
       |                        |
    PostgreSQL              Worker/Jobs
                                |
                         Open Banking/PSD2
```

The database is never publicly exposed.

## 3. Services

Initial deployable units:

- `frontend`: static PWA.
- `api`: authentication, authorization and synchronous domain API.
- `worker`: PSD2 synchronization and asynchronous jobs.
- `postgres`: persistent database.

The domain modules may initially live inside the API/worker. Physical microservice separation is introduced only where isolation or scaling justifies it.

## 4. Domain boundaries

- Authentication & identity
- Expense management
- Classification
- Dashboard/reporting
- Notifications/activity
- PSD2/Open Banking
- Import
- Backup/restore orchestration
- Groups and permissions

See `microservices/` for explicit boundaries and contracts.

## 5. Frontend

The frontend is responsible for presentation, navigation, local UI state, form validation for UX and API consumption. It is never the authoritative source for accounting rules, authorization or financial calculations.

## 6. Backend

The backend owns:

- business rules;
- authorization;
- persistence;
- money calculations;
- PSD2 state transitions;
- imports;
- dashboard aggregations;
- activity generation;
- audit.

Recommended implementation stack: TypeScript/React/Vite for frontend and Python/FastAPI for backend, subject to the Technology Decisions document.

## 7. Async processing

Long-running tasks must not block HTTP requests. Use a lightweight worker and persistent job state. Do not introduce Kafka/RabbitMQ/Redis merely for architectural fashion.

## 8. PSD2 adapter

Provider-specific formats are isolated behind an adapter interface. Core Pecunia deals with normalized transactions, connection identity, consent state and synchronization metadata.

## 9. Data and backups

PostgreSQL is the source of truth. Backup is an infrastructure/backend responsibility, never a PWA responsibility. Database/backup encryption and recovery-key handling follow the security specification.

## 10. Performance principles

- server-side aggregation for dashboards;
- indexed queries;
- pagination;
- no full-history download to the browser;
- no heavyweight search engine;
- no local heavyweight ML in V1;
- background PSD2 synchronization;
- minimal resident services.

## 11. Security boundaries

The reverse proxy terminates HTTPS. The API is the authorization boundary. Internal Docker services use private networking. Secrets never enter the frontend bundle or Git repository.

## 12. Scalability

V1 targets a personal/family deployment. Horizontal scaling is not a requirement. Clean module boundaries must nevertheless permit a future extraction of PSD2, notification or classification services without changing the core domain model.