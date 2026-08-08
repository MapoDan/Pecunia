# Pecunia

Pecunia è una Progressive Web App (PWA) self-hosted per il tracciamento e l'analisi delle spese personali e condivise.

## Scopo di questo repository

**Questo repository contiene esclusivamente analisi, specifiche e decisioni progettuali. Non contiene l'implementazione dell'applicazione.**

Lo sviluppo software sarà eseguito successivamente da un'AI/engineering agent specializzato, utilizzando questa documentazione come fonte di verità.

## V1 in breve

- tracciamento delle spese;
- inserimento manuale;
- import storico CSV;
- PSD2/Open Banking con operazioni PENDING da confermare;
- pagamento con più modalità nella stessa spesa;
- quota personale per spese condivise;
- classificazione e suggerimenti automatici;
- spese straordinarie separabili dalle statistiche ordinarie;
- dashboard configurabile;
- Centro Attività/Notifiche;
- utenti multipli;
- login Google e predisposizione Passkey;
- gruppi e conto cointestato di gruppo;
- visibilità genitore/figlio secondo permessi;
- dashboard amministrativa di utilizzo/performance;
- database cifrato e backup/restore gestiti dal backend/infrastruttura.

**Budget, OCR, allegati e funzionalità patrimoniali non fanno parte della V1.**

## Struttura

```text
Pecunia/
├── README.md
├── LICENSE
├── docs/
├── Logo/
├── microservices/
└── adr/
```

## Documentazione canonica

- `00_Vision.md`
- `01_Functional_Requirements.md`
- `02_Non_Functional_Requirements.md`
- `03_User_Stories.md`
- `04_Business_Rules.md`
- `05_Data_Model.md`
- `06_System_Architecture.md`
- `07_API_Design.md`
- `08_UI_UX_Guidelines.md`
- `09_Dashboard_Specification.md`
- `10_Backlog.md`
- `11_AI_DEVELOPMENT_GUIDELINES.md`
- `12_Coding_Standards.md`
- `13_Technology_Decisions.md`
- `14_Implementation_Roadmap.md`
- `15_Acceptance_Criteria.md`
- `Security_Specification.md`

## Regola per l'AI sviluppatrice

Prima di scrivere codice, l'AI deve leggere l'intera documentazione canonica, verificare eventuali conflitti e seguire la roadmap. In caso di ambiguità deve privilegiare le decisioni funzionali e di sicurezza già documentate e non inventare comportamenti di dominio.

## Branding

`Logo/` è riservata al logo e all'icona ufficiale di Pecunia. Le immagini definitive verranno aggiunte separatamente.

## Stato

La fase di analisi e specifica è in consolidamento finale. L'implementazione non è ancora iniziata in questo repository.

## Implementazione — fondazione

La prima milestone implementativa stabilisce una struttura leggera coerente con la roadmap:

- `backend/`: API FastAPI versionata sotto `/api/v1` con endpoint health e contratto errori strutturato;
- `frontend/`: PWA React/TypeScript/Vite con manifest e token colore Pecunia;
- `docker-compose.yml`: stack self-hosted con `frontend`, `api` e `postgres` su rete privata e volume persistente;
- `.env.example`: esempio di configurazione senza segreti reali;
- `.github/workflows/ci.yml`: controlli automatici backend e frontend.

### Avvio locale backend

```bash
pip install -e 'backend[test]'
pytest backend
uvicorn app.main:app --app-dir backend --reload
```

### Avvio locale frontend

```bash
cd frontend
npm install
npm run dev
```

### Avvio Docker

```bash
cp .env.example .env
# modificare POSTGRES_PASSWORD in .env prima di un uso reale
docker compose up --build
```

L'API espone `GET /api/v1/health`; la PWA è servita su `http://localhost:8080` nello stack Docker.

## Phase 1 — Identity

La fondazione Identity aggiunge:

- `POST /api/v1/auth/google` per login Google OIDC con verifica backend del token;
- `GET /api/v1/auth/me` per leggere il profilo autenticato;
- `POST /api/v1/auth/logout` per revocare la sessione corrente;
- tabelle `users`, `user_settings`, `auth_sessions`, `audit_events` tramite Alembic;
- cookie di sessione HttpOnly, token sessione salvato solo come hash HMAC e token CSRF per comandi state-changing;
- ruolo applicativo `USER`/`ADMIN` distinto dai futuri ruoli di gruppo.

### Migration

```bash
cd backend
alembic upgrade head
```

### Configurazione OAuth

Backend:

```bash
PECUNIA_GOOGLE_CLIENT_ID=your-google-client-id
PECUNIA_SESSION_SECRET=replace-with-a-long-random-secret
```

Frontend:

```bash
VITE_GOOGLE_CLIENT_ID=your-google-client-id
```
