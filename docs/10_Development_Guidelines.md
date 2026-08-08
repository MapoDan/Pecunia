# Pecunia — Development Guidelines

**Versione:** 1.0  
**Scope:** V1  
**Obiettivo:** fornire a Codex regole tecniche operative per implementare Pecunia senza introdurre complessità non richiesta.

---

## 1. Principio generale

Pecunia deve essere sviluppata come una **PWA mobile-first con backend API containerizzato**, eseguita sul NAS tramite Docker.

La soluzione deve essere:

- leggera;
- veloce;
- facilmente manutenibile;
- testabile;
- ripristinabile;
- composta da servizi con responsabilità chiare;
- pronta a crescere senza partire da una piattaforma enterprise inutilmente complessa.

**Regola:** non introdurre una tecnologia solo perché è moderna. Ogni componente deve avere una motivazione concreta.

---

# 2. Stack di riferimento

Lo stack V1 raccomandato è:

### Frontend

- React + TypeScript;
- Vite;
- PWA tramite service worker;
- routing client-side;
- libreria componenti leggera o componenti proprietari basati su un design system;
- gestione server-state tramite una soluzione leggera e consolidata;
- chart library leggera e lazy-loaded.

### Backend

- Python;
- FastAPI;
- Pydantic;
- SQLAlchemy;
- Alembic.

### Database

Preferenza V1:

- PostgreSQL.

Motivazioni:

- robustezza;
- transazioni;
- constraint;
- locking;
- supporto JSON dove utile;
- ottimo supporto Docker;
- adatto a dataset finanziari;
- leggero per il carico previsto.

### Reverse proxy

Utilizzare il reverse proxy già presente nell'infrastruttura del NAS, evitando di introdurne uno aggiuntivo senza necessità.

### Container

Docker Compose.

Kubernetes non è necessario per V1.

---

# 3. Architettura logica

Struttura iniziale:

```text
                    Internet / LAN
                          |
                          v
                  Reverse Proxy
                          |
                +---------+---------+
                |                   |
                v                   v
             Frontend              API
              PWA             FastAPI Backend
                                    |
                   +----------------+----------------+
                   |                |                |
                   v                v                v
                PostgreSQL      Worker/Jobs       External APIs
                                   |
                                   +--> Open Banking
```

Il frontend non accede mai direttamente al database.

---

# 4. Microservizi: approccio pragmatico

L'obiettivo è avere una struttura predisposta ai microservizi, ma non creare una dozzina di container inutili.

V1 deve iniziare con pochi servizi:

```text
frontend
api
worker
postgres
```

Eventuale reverse proxy esterno già esistente.

### Responsabilità

**frontend**

- UI;
- PWA;
- chiamate API;
- stato UI.

**api**

- autenticazione/sessione;
- authorization;
- business logic sincrona;
- CRUD;
- dashboard query;
- import orchestration;
- API Open Banking.

**worker**

- sincronizzazioni PSD2;
- elaborazioni asincrone;
- import pesanti;
- task periodici;
- eventuali future notifiche.

**postgres**

- persistenza.

Se il worker necessita di una coda, scegliere inizialmente una soluzione minimale. Non introdurre Redis/Kafka/RabbitMQ solo per seguire un pattern.

Per V1 è preferibile valutare prima PostgreSQL + job table/locking o scheduler interno al worker.

---

# 5. Struttura repository

Struttura target:

```text
Pecunia/
├── docs/
│   ├── 01_...
│   ├── ...
│   ├── 09_Security_Specification.md
│   └── 10_Development_Guidelines.md
│
├── frontend/
│   ├── public/
│   │   └── branding/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── stores/
│   │   ├── styles/
│   │   ├── types/
│   │   └── utils/
│   ├── tests/
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── workers/
│   │   └── main.py
│   ├── migrations/
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
│
├── worker/
│   ├── app/
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
│
├── docker/
│   ├── compose.yml
│   ├── compose.dev.yml
│   └── compose.prod.yml
│
├── .github/
│   └── workflows/
│
├── .env.example
├── .gitignore
└── README.md
```

La struttura può essere adattata durante l'implementazione, ma non deve diventare un monolite indistinto.

---

# 6. Feature-based frontend

Nel frontend le funzionalità principali devono essere isolate.

Esempio:

```text
features/
├── expenses/
├── dashboard/
├── activity/
├── psd2/
├── groups/
├── tags/
├── payments/
├── imports/
├── banking/
├── auth/
└── settings/
```

Una feature deve contenere, quando opportuno:

- componenti;
- API client;
- tipi;
- hook;
- test;
- mapper.

Evitare componenti giganteschi da 1.000+ righe.

---

# 7. Backend layered architecture

Il backend deve separare almeno:

```text
API route
   ↓
Schema validation
   ↓
Service / business logic
   ↓
Repository
   ↓
Database
```

Le route non devono contenere tutta la business logic.

Esempio:

```python
@router.post("/expenses")
async def create_expense(...):
    return expense_service.create(...)
```

Il service applica le Business Rules.

---

# 8. Business logic centralizzata

Regole finanziarie importanti devono essere centralizzate.

Esempi:

- somma payment split = totale;
- personal amount ≤ totale;
- PSD2 PENDING → ACCEPTED;
- una PSD2 transaction può generare al massimo una expense;
- appartenenza a gruppo;
- permessi admin;
- conversione valutaria;
- gestione straordinaria.

Non duplicare queste regole in frontend e backend con implementazioni divergenti.

Il frontend può fare validation UX, ma il backend è la fonte di verità.

---

# 9. Money handling

Mai utilizzare floating point per la contabilità.

Preferire:

```text
Decimal
```

oppure una rappresentazione integer in minor units, secondo la scelta definitiva del modello dati.

La soluzione deve essere coerente in tutto il sistema.

Esempio concettuale:

```text
EUR 10.99
```

non deve diventare:

```text
10.989999999
```

---

# 10. Time/date handling

Salvare timestamp in UTC quando rappresentano un istante.

Le date contabili devono rispettare il timezone dell'utente/contesto.

Il cambio valuta richiesto dall'utente deve utilizzare il tasso valido per la giornata della spesa, non il tasso corrente al momento della visualizzazione.

Il valore utilizzato deve essere persistito o ricostruibile in modo deterministico.

---

# 11. API contract-first

Le API devono essere implementate in accordo con:

`docs/07_API_Specification.md`

FastAPI deve generare OpenAPI.

Il frontend deve utilizzare tipi generati o una definizione condivisa dove questo riduca il rischio di mismatch.

Non modificare silenziosamente il contratto API per adattarsi al frontend.

Se emerge una necessità reale di modifica:

1. aggiornare la specifica;
2. implementare backend;
3. aggiornare frontend;
4. aggiornare test.

---

# 12. API versioning

Utilizzare:

```text
/api/v1/...
```

Non introdurre versioni multiple finché non necessarie.

Breaking changes future richiederanno `v2`.

---

# 13. Error response standard

Le API devono restituire una struttura coerente.

Esempio:

```json
{
  "error": {
    "code": "PAYMENT_SPLIT_TOTAL_MISMATCH",
    "message": "La somma dei metodi di pagamento non corrisponde al totale.",
    "request_id": "...",
    "details": {}
  }
}
```

Non restituire stack trace al client.

---

# 14. Idempotency

Le operazioni che possono essere ripetute accidentalmente devono supportare idempotenza dove necessario.

Particolarmente importante per:

- accettazione PSD2;
- webhook;
- import commit;
- job di sincronizzazione.

Un retry non deve generare duplicati finanziari.

---

# 15. Database migrations

Usare Alembic.

Regole:

- ogni modifica schema deve avere migration;
- mai modificare manualmente il DB di produzione come metodo normale;
- migration forward-only salvo procedure esplicite di recovery;
- testare migration su DB pulito;
- testare upgrade da una versione precedente.

---

# 16. Seed e default configuration

Alla creazione di un nuovo utente devono essere disponibili configurazioni predefinite.

Esempi:

- categorie;
- sottocategorie;
- metodi di pagamento;
- preferenze dashboard.

I default devono essere versionati e modificabili senza sovrascrivere le personalizzazioni esistenti.

---

# 17. Suggested values

Il motore di suggerimenti V1 deve essere leggero.

Ordine consigliato:

```text
Merchant exact match
       ↓
Merchant normalized match
       ↓
Merchant + payment method
       ↓
PSD2 description
       ↓
User history
       ↓
Global defaults
```

Non introdurre ML pesante.

Il sistema deve poter funzionare efficientemente su un NAS con risorse limitate.

---

# 18. Background jobs

Le operazioni lente non devono bloccare le richieste HTTP.

Esempi:

- sincronizzazione PSD2;
- import CSV molto grandi;
- aggiornamento aggregati dashboard;
- future notifiche.

Il frontend deve poter vedere:

```text
queued
running
completed
failed
```

quando un job è asincrono.

---

# 19. PSD2 worker

Il worker deve:

1. individuare connessioni da sincronizzare;
2. rispettare rate limit provider;
3. recuperare solo il periodo necessario;
4. partire dalla data di collegamento iniziale;
5. deduplicare le operazioni;
6. creare/aggiornare `PSD2Transaction` in stato PENDING;
7. non creare automaticamente una Expense;
8. produrre una notifica nel Centro Attività.

Una sincronizzazione successiva deve recuperare solo il delta necessario secondo le regole del provider.

---

# 20. PSD2 state machine

Stato minimo:

```text
PENDING
  | \
  |  \
ACCEPTED  IGNORED
```

Una transazione `ACCEPTED` non può tornare arbitrariamente a `PENDING` senza un'azione esplicita supportata dal dominio.

La transizione deve essere transazionale.

---

# 21. CSV import pipeline

Pipeline:

```text
Upload
  ↓
Validate
  ↓
Preview
  ↓
Mapping
  ↓
Validation
  ↓
Commit
```

Non creare spese durante il semplice upload.

Il commit deve essere esplicito.

Importi storici possono avere date precedenti alla data di collegamento Open Banking.

---

# 22. Dashboard architecture

Non scaricare tutte le spese al browser per costruire grafici.

Il backend deve fornire aggregazioni mirate.

Esempio:

```text
GET /dashboard/summary
GET /dashboard/by-category
GET /dashboard/by-payment-method
GET /dashboard/timeline
```

Le query devono utilizzare aggregazioni SQL efficienti e indici appropriati.

---

# 23. Pagination

Le liste potenzialmente lunghe devono essere paginate.

In particolare:

- expenses;
- PSD2 pending;
- activity;
- audit;
- CSV preview.

Evitare `SELECT *` senza limiti su dataset potenzialmente grandi.

---

# 24. Search

La ricerca iniziale deve usare strumenti nativi PostgreSQL/indici appropriati.

Non introdurre Elasticsearch/OpenSearch nella V1.

Un motore di ricerca dedicato sarebbe sproporzionato rispetto al carico previsto.

---

# 25. Caching

Caching solo dove dimostrato utile.

Possibili candidati:

- configurazioni globali;
- categorie default;
- dati dashboard costosi ma non critici;
- metadata provider.

Non cacheare indiscriminatamente dati finanziari personali.

Prima misurare, poi ottimizzare.

---

# 26. Database indexes

Aggiungere indici sulle query realmente frequenti.

Probabili candidati:

- user_id;
- group_id;
- expense date;
- category_id;
- merchant_id;
- PSD2 connection ID;
- PSD2 status;
- external transaction ID.

Gli indici devono essere verificati con query plan quando il dataset cresce.

---

# 27. Testing strategy

Target minimo:

### Unit test

Business rules pure.

### Integration test

API + database.

### Security test

Authorization e access isolation.

### E2E

Flussi critici frontend.

Flussi V1 prioritari:

1. login;
2. nuova spesa;
3. split pagamento;
4. modifica quota personale;
5. PSD2 pending → accepted;
6. PSD2 pending → ignored;
7. modifica importo PSD2;
8. CSV preview → commit;
9. gruppo;
10. dashboard.

---

# 28. Test financial invariants

Test obbligatori:

```text
payment_split_sum == total
```

```text
personal_amount <= total
```

```text
accepted_psd2_count_for_transaction <= 1
```

```text
ignored_psd2 does not create expense
```

```text
foreign_user_cannot_read_expense
```

Questi test sono più importanti di test puramente cosmetici.

---

# 29. Frontend testing

Testare soprattutto comportamento, non dettagli interni dei componenti.

Esempio:

```text
utente inserisce 10€
→ seleziona 8€ carta
→ seleziona 2€ buono pasto
→ salva
→ spesa salvata correttamente
```

Non testare eccessivamente classi CSS o struttura DOM interna.

---

# 30. CI

Ogni push/PR deve idealmente eseguire:

```text
lint
↓
typecheck
↓
unit tests
↓
integration tests
↓
build
```

Security/dependency checks devono essere aggiunti senza rallentare inutilmente il ciclo di sviluppo.

---

# 31. Git workflow

Branch principali:

```text
main
```

Feature branch:

```text
feature/<nome>
```

Bugfix:

```text
fix/<nome>
```

Commit piccoli e descrittivi.

Esempi:

```text
feat(expenses): add payment split validation
fix(psd2): prevent duplicate acceptance
feat(dashboard): add category aggregation
```

---

# 32. Definition of Done

Una funzionalità è completa quando:

- implementata;
- testata;
- documentata se modifica il contratto;
- coperta da authorization;
- verificata con error path;
- compatibile con Docker;
- non introduce secret;
- non rompe migration esistenti;
- mantiene performance ragionevoli.

---

# 33. Docker development

Il progetto deve poter essere avviato con un comando documentato.

Target:

```bash
docker compose -f docker/compose.dev.yml up --build
```

Il comando effettivo può essere modificato durante l'implementazione, ma deve rimanere semplice.

---

# 34. Production deployment

Il deployment deve essere riproducibile.

Configurazione tramite:

- `.env`/secrets;
- Docker Compose;
- migration automatiche controllate;
- health checks.

Non hardcodare:

- dominio;
- porte pubbliche;
- credenziali;
- secret.

---

# 35. Health checks

Esporre almeno:

```text
/health/live
/health/ready
```

`live` indica che il processo è vivo.

`ready` indica che le dipendenze necessarie sono disponibili.

Non includere secret nei response.

---

# 36. Observability

Logging strutturato JSON dove utile.

Campi consigliati:

```text
timestamp
level
service
request_id
route
status_code
duration_ms
```

Non includere dati finanziari sensibili come default.

---

# 37. Performance targets

Target iniziali, da misurare e non da assumere come garanzia:

- API CRUD semplice: idealmente < 300 ms server-side in condizioni normali;
- dashboard aggregata: idealmente < 1 s;
- apertura PWA percepita: rapida anche su rete domestica;
- lista spese: paginata e caricamento progressivo.

Se un requisito richiede un'ottimizzazione prematura, misurare prima.

---

# 38. NAS resource constraints

Il NAS non deve essere trattato come un server cloud illimitato.

Evitare:

- AI locale pesante;
- Elasticsearch;
- Kubernetes;
- Kafka;
- cluster DB;
- microservizi estremamente frammentati;
- processi residenti inutilmente;
- polling aggressivo.

Preferire:

- PostgreSQL;
- FastAPI;
- worker singolo scalabile in futuro;
- query SQL efficienti;
- job scheduling semplice;
- frontend statico.

---

# 39. Configuration management

Configurazioni distinguere tra:

### Build-time

- frontend API base path se necessario;
- feature flags non sensibili.

### Runtime

- DB URL;
- OAuth secrets;
- PSD2 secrets;
- encryption settings;
- external provider config.

Nessun secret deve finire nel bundle frontend.

---

# 40. Feature flags

Le feature flags possono essere utilizzate per:

- Passkey;
- nuovi provider PSD2;
- funzioni sperimentali.

Non utilizzare feature flags per nascondere permanentemente codice incompleto.

---

# 41. V1 scope control

V1 NON deve includere senza nuova approvazione:

- budget;
- investimenti;
- gestione patrimonio;
- OCR scontrini;
- allegati/ricevute;
- AI generativa pesante;
- sincronizzazione offline completa;
- app native iOS/Android;
- notifiche push native complesse.

L'obiettivo è una V1 solida del tracking spese.

---

# 42. V2 readiness

Il codice deve permettere di aggiungere successivamente:

- budget;
- allegati;
- OCR;
- insight avanzati;
- ulteriori provider bancari;
- mobile native wrapper se necessario.

Non implementare però questi moduli in anticipo.

---

# 43. Codex execution rules

Quando Codex implementa una funzionalità deve procedere in questo ordine:

1. leggere documentazione pertinente;
2. verificare codice esistente;
3. definire il cambiamento minimo necessario;
4. implementare backend/domain;
5. implementare API;
6. implementare frontend;
7. aggiungere test;
8. eseguire lint/typecheck/test/build;
9. aggiornare documentazione se il comportamento è cambiato;
10. riportare chiaramente cosa è stato fatto e cosa resta.

Codex non deve riscrivere parti funzionanti senza motivo.

---

# 44. Regola contro le assunzioni

Quando una specifica è ambigua, Codex deve:

1. cercare una decisione già presente nei documenti;
2. verificare Business Rules;
3. verificare API contract;
4. scegliere la soluzione più semplice coerente;
5. documentare l'assunzione.

Non inventare funzionalità di dominio.

---

# 45. Priorità di autorità

In caso di conflitto utilizzare questo ordine:

```text
Business Rules / Functional Analysis
        ↓
Security Specification
        ↓
API Specification
        ↓
UX Specification
        ↓
Development Guidelines
        ↓
Implementation convenience
```

La comodità tecnica non può modificare un requisito funzionale.

---

# 46. Aggiornamento documentazione

Se l'implementazione dimostra che una specifica è errata o incompleta:

- non ignorare la specifica;
- correggere il documento interessato;
- aggiornare il codice;
- aggiungere/regolare i test.

La documentazione deve rimanere sincronizzata con il comportamento reale.

---

# 47. Anti-pattern da evitare

Non creare:

- God component;
- God service;
- repository generici inutili;
- `utils.ts` giganteschi;
- endpoint che fanno tutto;
- SQL sparso nelle route;
- business rules nel JSX;
- variabili globali per stato finanziario;
- chiamate API duplicate;
- polling continuo senza necessità.

---

# 48. Code quality

Preferire codice:

- esplicito;
- tipizzato;
- piccolo;
- testabile;
- leggibile.

Non ottimizzare per numero minimo di righe.

La priorità è mantenibilità.

---

# 49. Dependency policy

Prima di introdurre una dipendenza chiedersi:

1. serve davvero?
2. esiste già una funzionalità nello stack?
3. aumenta significativamente il peso dell'app?
4. è mantenuta?
5. introduce rischi di sicurezza?
6. è compatibile con self-hosting/NAS?

Se la risposta non è convincente, non aggiungerla.

---

# 50. Primo milestone tecnico

La prima milestone di sviluppo deve produrre un sistema realmente avviabile, anche se ancora povero di funzionalità:

```text
Docker Compose
    ↓
PostgreSQL
    ↓
FastAPI
    ↓
React PWA
    ↓
Reverse proxy-ready
```

Con:

- health checks;
- migration iniziale;
- struttura progetto;
- CI base;
- test base;
- login predisposto;
- README di avvio.

Dopo questa milestone si procede per vertical slices, non costruendo prima tutto il backend e solo alla fine il frontend.

---

# 51. Vertical slice strategy

Ordine consigliato:

### Slice 1

Infrastructure + authentication skeleton.

### Slice 2

Expense creation + expense list.

### Slice 3

Payment split + personal amount.

### Slice 4

Categories/merchant suggestions.

### Slice 5

Dashboard base.

### Slice 6

PSD2 connection + pending operations.

### Slice 7

PSD2 acceptance/ignore + activity center.

### Slice 8

CSV import.

### Slice 9

Groups + shared account.

### Slice 10

Admin dashboard + performance.

### Slice 11

Security hardening + deployment.

Questo permette di avere progressivamente un'app funzionante invece di aspettare la fine del progetto.

---

# 52. Criterio finale

Pecunia deve rimanere una soluzione **semplice da capire, semplice da eseguire e difficile da rompere**.

La complessità deve essere introdotta soltanto quando un requisito reale la giustifica.

Il vincolo NAS è un requisito architetturale, non un limite da aggirare con infrastruttura sproporzionata.
