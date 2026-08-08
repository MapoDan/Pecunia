# Pecunia — System Architecture

**Versione:** 1.0  
**Scope:** V1  
**Target:** PWA + backend containerizzato sul NAS

## 1. Obiettivi architetturali

Pecunia deve essere:

- leggera e veloce su hardware NAS con risorse limitate;
- installabile e gestibile tramite Docker Compose;
- utilizzabile da smartphone, tablet e desktop tramite PWA;
- separata in componenti con responsabilità chiare;
- facilmente aggiornabile senza modificare i dati persistenti;
- predisposta a crescere verso V2 senza introdurre complessità prematura;
- sicura per dati finanziari personali;
- osservabile e diagnosticabile dal backend.

### Principio guida

**Microservizi dove esiste un confine funzionale reale, non un container per ogni classe o funzione.**

La V1 deve privilegiare pochi servizi efficienti rispetto a una proliferazione di microservizi.

---

# 2. Architettura logica

```text
                    Internet / LAN
                          |
                    Reverse Proxy
                 HTTPS + Security Headers
                          |
                 +--------+--------+
                 |                 |
               PWA              API Backend
                 |                 |
                 |          +------+------+
                 |          |             |
                 |       Auth/RBAC     Core Domain
                 |                         |
                 |              +----------+----------+
                 |              |          |           |
                 |            PSD2      Import      Notifications
                 |              |          |           |
                 +--------------+----------+-----------+
                                |
                         PostgreSQL DB
                                |
                         Backend Backup
```

Questa rappresentazione è logica: alcuni moduli possono inizialmente risiedere nello stesso servizio/container se la separazione fisica non porta vantaggi concreti.

---

# 3. Componenti principali

## 3.1 Frontend PWA

Responsabilità:

- UI responsive mobile-first;
- dashboard;
- inserimento spese;
- Centro Attività;
- gestione gruppi;
- configurazione account;
- gestione collegamenti PSD2;
- import CSV;
- autenticazione lato client;
- gestione installazione PWA;
- chiamate API al backend.

Il frontend **non deve contenere regole contabili autorevoli**.

Il backend rimane la fonte di verità.

### Tecnologia proposta

Frontend TypeScript con framework moderno e leggero, preferibilmente **React + Vite** oppure equivalente se i benchmark dimostrano un vantaggio concreto.

La scelta definitiva deve privilegiare:
- bundle contenuto;
- ottima UX mobile;
- facilità di manutenzione;
- compatibilità PWA;
- ecosistema maturo.

---

# 4. Backend API

Il backend espone le API utilizzate dalla PWA.

Responsabilità:

- autenticazione/autorizzazione applicativa;
- gestione utenti;
- spese;
- categorie;
- tag;
- gruppi;
- metodi di pagamento;
- split;
- quote personali;
- operazioni PSD2;
- import CSV;
- notifiche;
- dashboard/aggregazioni;
- configurazioni;
- audit tecnico/funzionale;
- health/readiness endpoint.

### Tecnologia proposta

**Python + FastAPI** come prima scelta per la V1.

Motivazioni:
- leggero;
- ottimo supporto async per I/O;
- tipizzazione con Pydantic;
- OpenAPI automatico;
- ottimo fit con container piccoli;
- facile sviluppo e manutenzione.

Alternative possono essere valutate solo se portano un vantaggio concreto.

---

# 5. Database

## 5.1 Scelta

**PostgreSQL**.

Motivazioni:

- robustezza;
- transazioni;
- vincoli relazionali;
- query analitiche;
- supporto JSONB dove utile senza trasformare il modello in NoSQL;
- strumenti di backup/restore maturi;
- ottimo supporto Docker.

## 5.2 Principi

- schema relazionale normalizzato;
- foreign key;
- unique constraint per idempotenza;
- indici sulle query frequenti;
- migrazioni versionate;
- nessuna logica critica affidata esclusivamente al frontend.

## 5.3 Cifratura

Il database e/o i suoi backup devono essere protetti secondo la strategia di cifratura definita nei requisiti di sicurezza.

La chiave di cifratura necessaria al restore deve essere consegnata all'amministratore nella fase prevista e non deve essere recuperabile successivamente dalla normale UI.

La soluzione tecnica definitiva dovrà essere scelta in modo da non rendere inutilmente complesso il deployment sul NAS.

---

# 6. Autenticazione

## 6.1 Google Login

V1:

- login tramite Google;
- identità Google associata a un account Pecunia;
- sessione gestita in modo sicuro;
- token/session secrets solo backend.

## 6.2 Passkey

Pecunia deve supportare WebAuthn/passkey come metodo di accesso successivo.

Le passkey non sostituiscono necessariamente il primo onboarding tramite Google: la registrazione avviene dopo l'autenticazione iniziale.

## 6.3 Autorizzazione

Il backend determina sempre:

- utente autenticato;
- ruolo;
- gruppo;
- permessi;
- accesso ai dati.

Il frontend non può elevare autonomamente i propri privilegi.

---

# 7. PSD2 / Open Banking

Il provider PSD2 deve essere isolato tramite un adapter/interface.

```text
Core Pecunia
     |
 PSD2 Adapter Interface
     |
 +---+------------------+
 |                      |
Provider A          Provider B
```

Il dominio Pecunia non deve dipendere direttamente dal formato proprietario del provider.

## Responsabilità adapter

- autenticazione verso provider;
- gestione consent;
- sincronizzazione;
- mapping delle transazioni;
- normalizzazione;
- gestione errori provider;
- rate limit;
- refresh consent dove previsto.

## Regola fondamentale

Il servizio PSD2 può **acquisire** movimenti, ma non può decidere autonomamente di contabilizzarli come spese.

Il passaggio a spesa avviene nel Core Domain dopo decisione dell'utente.

---

# 8. Scheduler / Background jobs

Serve un componente per attività asincrone e pianificate:

- sincronizzazione PSD2;
- aggiornamento stato consent;
- elaborazioni di import;
- rilevamento potenziali aggiornamenti;
- aggregazioni eventualmente costose;
- pulizia tecnica.

### Strategia V1

Evitare inizialmente un message broker dedicato come RabbitMQ/Kafka se non necessario.

Preferire:
- job runner integrato nel backend;
- PostgreSQL come persistence dei job quando appropriato;
- worker leggero separato solo se necessario.

Questo riduce RAM e complessità sul NAS.

---

# 9. Import CSV

L'import CSV deve essere un modulo backend dedicato, non una funzionalità che esegue direttamente query dal browser.

Flusso:

```text
PWA
 |
 | upload CSV
 v
API
 |
 v
CSV Parser/Validator
 |
 +--> valid rows --> staging/import
 |
 +--> invalid rows --> report
 |
 v
Domain Import Service
 |
 v
PostgreSQL
```

L'import deve supportare:

- mapping colonne;
- validazione;
- date storiche;
- import parziale;
- rilevazione duplicati;
- report degli errori.

---

# 10. Notifiche / Centro Attività

Il Centro Attività è una vista sullo stato delle attività che richiedono intervento.

Non è necessario un sistema push complesso per la V1.

Il backend mantiene gli elementi di attività e la PWA li interroga tramite API.

Possibili evoluzioni future:
- Web Push;
- notifiche native wrapper;
- email selettive.

---

# 11. Dashboard e reporting

Le dashboard devono essere costruite tramite API di aggregazione.

Non devono scaricare tutto lo storico nel browser per poi calcolare i grafici lato client.

Esempio:

```text
PWA --> GET /dashboard/summary
              |
              v
       Query aggregate DB
              |
              v
          JSON compatto
```

Questo riduce:
- traffico;
- RAM browser;
- CPU smartphone;
- tempi di rendering;
- carico sul NAS.

Per dataset piccoli/medi si preferiscono query PostgreSQL ben indicizzate rispetto a un data warehouse separato.

---

# 12. Cache

V1: evitare Redis salvo necessità dimostrata.

PostgreSQL può essere utilizzato come source of truth e, dove opportuno, alcune informazioni possono essere cached lato frontend/PWA.

Una cache server-side deve essere introdotta solo quando:
- esiste un problema misurato;
- la cache produce un beneficio concreto;
- invalidazione e consistenza sono definite.

---

# 13. Reverse proxy

Il deployment previsto utilizza un reverse proxy già compatibile con l'infrastruttura NAS.

Responsabilità:

- HTTPS;
- certificati;
- routing verso frontend/API;
- eventuali security headers;
- rate limiting dove opportuno.

La PWA non deve esporre direttamente le porte interne dei container.

---

# 14. Docker

La V1 deve essere distribuibile con Docker Compose.

Servizi iniziali consigliati:

```text
pecunia-frontend
pecunia-api
pecunia-worker
pecunia-db
```

Il reverse proxy può essere esterno allo stack Pecunia se già gestito dall'infrastruttura NAS.

PSD2 può inizialmente essere un modulo dell'API o del worker; deve diventare un container separato solo se necessario per isolamento/scalabilità.

### Principio

Non creare container separati per:
- categorie;
- dashboard;
- notifiche;
- tag;
- utenti;
- spese.

Sono moduli del dominio, non microservizi autonomi.

---

# 15. Networking Docker

I container devono comunicare tramite una rete privata Docker.

Solo i servizi necessari devono essere raggiungibili dall'esterno.

Esempio:

```text
Internet
   |
Reverse Proxy
   |
Frontend/API
   |
Private Docker Network
   |
+-------+-------+
|       |       |
DB    Worker   Internal services
```

Il database non deve essere pubblicato direttamente su Internet.

---

# 16. Persistenza

I dati persistenti devono essere esterni al lifecycle del container.

Persistono almeno:

- PostgreSQL data;
- eventuali file temporanei/import necessari;
- configurazioni persistenti strettamente necessarie.

Le immagini container devono poter essere sostituite senza perdita dei dati.

---

# 17. Backup e restore

Il backup non è responsabilità della PWA.

La strategia prevista è:

```text
PostgreSQL
    |
Backend / Infrastructure backup
    |
Encrypted backup
    |
NAS backup storage / external target
```

Il restore deve essere eseguibile a livello backend/infrastruttura.

La chiave necessaria al restore deve essere conservata dall'amministratore secondo la procedura definita.

---

# 18. Secrets

Non devono essere committati nel repository:

- Google OAuth secrets;
- PSD2 credentials;
- database password;
- encryption keys;
- session secrets;
- certificati privati.

In sviluppo si utilizza `.env.example` come template privo di valori sensibili.

In produzione i secrets devono essere iniettati tramite environment/secret management dell'host Docker.

---

# 19. API design

Le API devono essere versionate, ad esempio:

`/api/v1/...`

Devono utilizzare:

- HTTP semantico;
- JSON;
- validation lato backend;
- error response strutturate;
- pagination per liste;
- filtri server-side;
- sorting controllato;
- idempotency dove necessario.

L'OpenAPI generato dal backend costituisce parte del contratto tecnico.

---

# 20. Idempotenza

Particolare attenzione a:

- sincronizzazioni PSD2;
- webhook/eventi futuri;
- import CSV;
- retry dei job;
- richieste duplicate dal client.

Ogni operazione che può essere ritentata deve avere una strategia per evitare duplicazioni.

---

# 21. Audit e tracciabilità

Per operazioni finanziarie sensibili devono essere conservati almeno i riferimenti necessari a sapere:

- origine della spesa;
- chi l'ha creata;
- quando è stata creata;
- eventuale fonte PSD2;
- eventuale import;
- modifiche rilevanti.

L'audit deve essere leggero e non deve trasformare ogni modifica UI in una quantità sproporzionata di dati.

---

# 22. Performance

Target progettuali iniziali:

- API semplici: p95 idealmente < 500 ms in condizioni normali;
- apertura dashboard: evitare query ripetitive e N+1;
- inserimento spesa: risposta immediata;
- sincronizzazioni PSD2 eseguite in background;
- nessun calcolo pesante sul browser per dataset completi;
- nessun componente AI pesante nella V1.

I target devono essere verificati tramite benchmark sul NAS reale prima di essere considerati SLO definitivi.

---

# 23. Scalabilità

La scalabilità V1 è principalmente verticale e orientata a un'installazione personale/familiare.

Non sono richiesti inizialmente:

- Kubernetes;
- service mesh;
- distributed tracing completo;
- Kafka;
- data warehouse;
- cluster PostgreSQL.

L'architettura deve però mantenere confini sufficientemente puliti da permettere una futura separazione di servizi senza riscrivere il dominio.

---

# 24. Observability

Ogni servizio deve produrre:

- log strutturati;
- livello INFO/WARN/ERROR;
- correlation/request ID;
- health check;
- readiness check dove applicabile.

Metriche utili:

- richieste API;
- latenza;
- error rate;
- job falliti;
- sincronizzazioni PSD2;
- import CSV;
- utilizzo CPU/RAM/container.

Non devono essere loggati dati finanziari sensibili inutilmente.

---

# 25. Sicurezza applicativa

Obblighi minimi:

- HTTPS in produzione;
- validazione input;
- ORM/query parametrizzate;
- protezione CSRF dove applicabile alla strategia auth;
- cookie sicuri se utilizzati;
- rate limiting sugli endpoint sensibili;
- controllo autorizzazioni server-side;
- headers di sicurezza;
- gestione sicura dei token OAuth;
- nessun secret nel frontend.

---

# 26. Struttura logica del codice backend

Proposta:

```text
backend/
├── app/
│   ├── api/
│   ├── auth/
│   ├── domain/
│   │   ├── expenses/
│   │   ├── payments/
│   │   ├── categories/
│   │   ├── tags/
│   │   ├── groups/
│   │   ├── psd2/
│   │   ├── imports/
│   │   ├── activities/
│   │   └── dashboards/
│   ├── infrastructure/
│   ├── db/
│   └── workers/
├── migrations/
└── tests/
```

Il dominio non deve dipendere direttamente dal framework web quando evitabile.

---

# 27. Struttura repository proposta

```text
Pecunia/
├── docs/
├── frontend/
├── backend/
├── docker/
├── scripts/
├── tests/
├── .env.example
├── docker-compose.yml
└── README.md
```

La struttura può essere adattata durante l'implementazione se emerge una motivazione tecnica documentata.

---

# 28. Flusso: inserimento manuale

```text
Utente
  |
  v
PWA
  |
  v
POST /expenses
  |
  v
API validation
  |
  v
Domain rules
  |
  v
PostgreSQL transaction
  |
  v
Response
```

La transazione deve validare almeno:
- importo;
- split;
- quota personale;
- categoria;
- autorizzazioni;
- gruppo;
- data.

---

# 29. Flusso: PSD2

```text
Provider PSD2
      |
      v
PSD2 Worker
      |
      v
Normalize transaction
      |
      v
PENDING operation
      |
      v
Centro Attività
      |
      v
Decisione utente
   /          \
ACCEPT       IGNORE
  |             |
  v             v
Expense       IGNORED
```

La sincronizzazione non deve saltare il passaggio `PENDING`.

---

# 30. Flusso: contabilizzazione PSD2 modificata

```text
PSD2 5 €
   |
   v
Utente apre attività
   |
   v
Modifica totale → 15 €
   |
   +-- Carta 5 €
   +-- Buono pasto 10 €
   |
   v
ACCEPT
   |
   v
Expense 15 €
   |
   +-- source transaction = PSD2 5 €
```

Il movimento PSD2 originario non viene riscritto.

---

# 31. Flusso: gruppo + conto condiviso

```text
Conto cointestato
       |
       v
PSD2 connection
       |
       v
Shared Group
       |
       v
Group expenses

Conti personali
       |
       v
Personal space
```

Il collegamento del conto determina il contesto di destinazione secondo la configurazione autorizzata.

---

# 32. Decisioni architetturali da non anticipare

Non introdurre nella V1 senza requisito o benchmark:

- Kubernetes;
- Redis;
- RabbitMQ/Kafka;
- Elasticsearch/OpenSearch;
- microservizi separati per ogni dominio;
- LLM/AI server locale;
- data warehouse;
- GraphQL se REST è sufficiente;
- server-side rendering complesso se la PWA client-side è sufficiente.

La semplicità è un requisito tecnico di Pecunia.

---

# 33. Definition of Done architetturale

Prima di considerare pronta la base architetturale:

- [ ] Docker Compose avvia tutti i servizi;
- [ ] database persistente;
- [ ] migrazioni funzionanti;
- [ ] health check funzionanti;
- [ ] API documentate tramite OpenAPI;
- [ ] autenticazione Google predisposta;
- [ ] autorizzazione server-side;
- [ ] frontend collegato all'API;
- [ ] nessun secret nel repository;
- [ ] logging strutturato;
- [ ] test automatici di dominio;
- [ ] backup/restore documentato;
- [ ] configurazione NAS documentata;
- [ ] immagini Docker minimizzate e riproducibili.

---

# 34. Nota per Codex

Codex deve considerare questo documento come **architettura di riferimento**, non come autorizzazione a introdurre infrastruttura aggiuntiva.

Quando una scelta non è definita:

1. preferire la soluzione più semplice;
2. preferire componenti già presenti nello stack;
3. minimizzare CPU/RAM;
4. mantenere il dominio indipendente dai dettagli infrastrutturali;
5. documentare ogni deviazione architetturale significativa;
6. aggiungere un nuovo servizio solo quando esiste un confine di responsabilità o un requisito operativo reale.
