# Pecunia — Security Specification

**Versione:** 1.0  
**Scope:** V1  
**Classificazione:** dati finanziari personali — security by design

## 1. Obiettivo

Pecunia gestisce dati finanziari personali, collegamenti Open Banking/PSD2 e autenticazione degli utenti. La sicurezza deve quindi essere una caratteristica architetturale e non una funzione aggiunta successivamente.

Obiettivi prioritari:

1. impedire accessi non autorizzati;
2. minimizzare i dati sensibili conservati;
3. proteggere credenziali e token;
4. cifrare il database e i backup;
5. separare frontend, API e dati;
6. mantenere audit delle operazioni sensibili;
7. impedire contaminazioni tra utenti e gruppi;
8. rendere recuperabile il sistema in caso di fault;
9. mantenere l'implementazione leggera per il NAS.

---

# 2. Threat model minimo

Pecunia deve considerare almeno:

- account Google compromesso;
- sessione rubata;
- token/session cookie rubato;
- accesso non autorizzato a un gruppo;
- IDOR/BOLA tramite modifica di UUID nelle API;
- SQL injection;
- XSS;
- CSRF dove applicabile;
- upload CSV malevolo;
- webhook PSD2 falsificati;
- replay di richieste PSD2;
- doppia contabilizzazione;
- esposizione accidentale di token bancari nei log;
- accesso al NAS da un altro dispositivo della rete;
- compromissione di un container;
- backup rubato;
- secret presente nel repository Git;
- errore applicativo che espone dati di un altro utente.

La sicurezza non deve basarsi sull'assunzione che la rete domestica sia completamente affidabile.

---

# 3. Principio fondamentale: backend trusted boundary

Il browser/PWA è un ambiente non affidabile.

Il backend deve considerare ogni valore ricevuto dal client come non attendibile.

Il frontend non può decidere autonomamente:

- quale utente può leggere una spesa;
- quale gruppo può leggere;
- se una PSD2Transaction può essere accettata;
- se un utente è admin;
- se un importo è contabilmente valido;
- se una banca appartiene a un gruppo.

Tutte queste decisioni devono essere prese dal backend.

---

# 4. Google Login

La V1 utilizza esclusivamente **Google OAuth/OIDC** per il login iniziale.

Il backend deve:

- validare correttamente il flusso OIDC;
- verificare issuer;
- verificare audience/client ID;
- verificare firma e validità dei token;
- utilizzare il subject (`sub`) come identificatore stabile;
- non fidarsi dell'email come unica identità tecnica;
- non registrare access token nei log.

Il client secret Google deve risiedere esclusivamente nel backend/secret store.

Non deve essere presente:

- nel repository;
- nel bundle frontend;
- nelle variabili pubbliche del frontend.

---

# 5. Session management

La sessione deve essere gestita dal backend.

Per una PWA browser-based è preferibile una sessione server-side o cookie HTTP-only con token di sessione non esposto al JavaScript applicativo.

Cookie consigliato:

```text
HttpOnly
Secure
SameSite=Lax/Strict secondo il flusso OAuth
```

Il valore esatto deve essere verificato in base al deployment HTTPS e al flusso di login.

La PWA non deve salvare token di autenticazione sensibili in `localStorage`.

---

# 6. Passkey / WebAuthn

La V1 deve predisporre l'architettura per Passkey.

Il backend deve utilizzare WebAuthn con challenge server-generated.

Principi:

- challenge monouso;
- scadenza breve;
- verifica origin;
- verifica RP ID;
- verifica attestation/assertion secondo policy;
- protezione replay;
- credential ID unique;
- chiave privata sempre sul device/autenticatore;
- il server conserva esclusivamente la public key e i metadata necessari.

La passkey non deve sostituire arbitrariamente il controllo di sessione server-side.

---

# 7. Autorizzazione

Pecunia deve implementare almeno RBAC + ownership/context checks.

Ogni richiesta deve essere verificata rispetto a:

```text
Authenticated user
        ↓
Global role
        ↓
Resource ownership
        ↓
Group membership
        ↓
Group role/permission
```

Esempio:

```http
GET /api/v1/expenses/{uuid}
```

Non è sufficiente verificare che l'UUID esista.

Il backend deve verificare che la spesa sia accessibile all'utente nel relativo contesto.

Questo protegge dagli attacchi IDOR/BOLA.

---

# 8. Separazione personale/gruppo

Una spesa personale non deve essere leggibile da un altro utente solo perché l'altro utente conosce il relativo UUID.

Una spesa di gruppo è accessibile esclusivamente ai membri autorizzati del gruppo.

Il conto cointestato associato a un gruppo segue la stessa regola.

La visibilità genitore/figlio deve essere esplicitamente autorizzata dal permission model.

---

# 9. Admin

Il ruolo `ADMIN` è globale e deve essere verificato lato backend.

L'admin può accedere alle dashboard di:

- utilizzo;
- performance;
- stato applicativo.

L'accesso admin non deve automaticamente significare accesso indiscriminato ai dettagli finanziari personali degli utenti.

Le API amministrative devono essere separate e protette.

---

# 10. Password

Pecunia V1 non gestisce password locali.

Il sistema deve evitare completamente:

- password database utente;
- password reset custom;
- password recovery custom.

La gestione dell'identità primaria è delegata a Google e, quando abilitato, alle passkey.

---

# 11. Secret management

Nessun secret deve essere committato nel repository.

Secret potenziali:

- Google OAuth client secret;
- session secret;
- JWT signing key se eventualmente utilizzata;
- PSD2 provider credentials;
- encryption key database;
- webhook secret;
- SMTP/API secret futuri.

In sviluppo utilizzare `.env` locale non versionato.

In produzione utilizzare Docker secrets o un secret mechanism equivalente.

Il file `.env.example` deve contenere esclusivamente placeholder.

---

# 12. Database encryption

Il database deve essere cifrato a livello backend/storage secondo l'architettura scelta.

Requisito funzionale dell'utente:

- il DB deve essere cifrato;
- il backup deve poter essere ripristinato dal backend;
- la PWA non deve effettuare backup;
- la chiave di cifratura deve essere mostrata una sola volta al momento della creazione/configurazione iniziale;
- la chiave è necessaria per il ripristino.

### Nota architetturale importante

La chiave non deve essere salvata nella PWA né restituita dalle API dopo la creazione.

Il backend deve prevedere un meccanismo di inizializzazione in cui:

```text
Create encryption key
        ↓
Show/export once
        ↓
User stores key securely
        ↓
Backend uses key to access encrypted data
```

Il dettaglio tecnico della cifratura deve essere scelto in base al database/stack effettivamente adottato.

Non implementare una cifratura custom fatta in casa.

---

# 13. Backup e restore

La PWA non esegue backup.

Backup e restore sono responsabilità del backend/infrastruttura NAS.

Devono essere previste procedure documentate per:

1. backup DB;
2. backup configurazione necessaria;
3. protezione dei backup;
4. verifica integrità;
5. restore su istanza pulita;
6. verifica post-restore.

Il backup deve essere cifrato quando contiene dati finanziari.

La chiave necessaria al restore non deve essere inclusa nello stesso backup in forma recuperabile automaticamente.

---

# 14. PSD2 / Open Banking

Le credenziali e i token del provider PSD2 sono estremamente sensibili.

Devono essere:

- cifrati at rest;
- non presenti nel frontend;
- non presenti nei log;
- non inclusi nelle response API se non indispensabili;
- ruotabili/revocabili.

Pecunia deve conservare il minimo necessario per mantenere il collegamento.

---

# 15. PSD2 consent

Il consent deve essere ottenuto tramite il provider Open Banking.

Pecunia non deve chiedere all'utente le credenziali bancarie e non deve conservarle.

Il frontend deve reindirizzare/seguire il flusso previsto dal provider.

---

# 16. Webhook PSD2

Se il provider utilizza webhook:

- verificare firma/autenticità;
- utilizzare HTTPS;
- gestire replay;
- utilizzare ID evento univoco;
- rendere l'elaborazione idempotente;
- non fidarsi del contenuto senza verifica.

Un webhook ripetuto non deve creare una seconda `PSD2Transaction`.

---

# 17. PSD2 data minimization

Non salvare indiscriminatamente il payload completo del provider se non necessario.

Conservare soltanto i campi utili al dominio e al debug controllato.

Se è necessario conservare dati raw per compatibilità provider, devono essere:

- minimizzati;
- protetti;
- esclusi dalle normali response API;
- esclusi dai log applicativi standard.

---

# 18. Logging

I log devono essere utili per il troubleshooting senza diventare un archivio di dati finanziari.

Non loggare:

- token;
- cookie;
- authorization header;
- OAuth secrets;
- PSD2 access tokens;
- encryption keys;
- PAN completi;
- payload bancari completi;
- dati finanziari completi se non necessari.

Utilizzare `request_id`/correlation ID per seguire una richiesta.

---

# 19. Audit

Le operazioni sensibili devono generare `AuditEvent`.

Almeno:

- login riuscito/fallito quando utile;
- collegamento/disconnessione banca;
- accettazione PSD2;
- ignoramento PSD2;
- modifica di una spesa;
- eliminazione/archiviazione;
- modifica permessi gruppo;
- modifica tag globali;
- azioni admin sensibili.

L'audit non deve contenere segreti.

---

# 20. API security

Ogni endpoint deve:

- validare input;
- applicare authorization;
- utilizzare query parametrizzate/ORM sicuro;
- limitare payload;
- applicare rate limiting dove necessario;
- non restituire dati non richiesti.

Gli endpoint di autenticazione e Open Banking devono avere rate limit più restrittivi.

---

# 21. SQL injection

Vietato costruire SQL concatenando input utente.

Preferire:

- ORM;
- query parametrizzate;
- query builder sicuro.

Le query dinamiche di ricerca/ordinamento devono utilizzare allow-list dei campi disponibili.

---

# 22. XSS

Il frontend deve:

- evitare `innerHTML` non sanitizzato;
- usare escaping di default del framework;
- sanitizzare HTML solo quando realmente necessario;
- non rendere HTML arbitrario proveniente da merchant/causali bancarie.

La causale PSD2 deve essere considerata input non attendibile.

---

# 23. CSRF

Se l'autenticazione utilizza cookie, implementare una protezione CSRF adeguata per le richieste state-changing.

SameSite non deve essere considerato automaticamente sufficiente in ogni scenario.

---

# 24. CORS

Consentire esclusivamente origin configurati.

In produzione evitare:

```text
Access-Control-Allow-Origin: *
```

per API autenticate.

---

# 25. HTTPS

Tutto il traffico autenticato deve utilizzare HTTPS.

Anche in ambiente domestico, se l'app è raggiungibile dall'esterno tramite reverse proxy, il traffico pubblico deve terminare su HTTPS.

HTTP deve essere limitato al necessario redirect/health locale secondo configurazione.

---

# 26. Reverse proxy

Il deployment previsto sul NAS deve utilizzare un reverse proxy, coerente con l'infrastruttura già presente.

Il reverse proxy deve gestire:

- TLS;
- routing;
- eventuali security headers;
- rate limiting di base quando opportuno.

Il backend non deve essere esposto direttamente a Internet se non necessario.

---

# 27. Security headers

Il deployment deve considerare almeno:

- Content-Security-Policy;
- X-Content-Type-Options;
- Referrer-Policy;
- Permissions-Policy;
- frame-ancestors tramite CSP;
- HSTS quando il deployment HTTPS è stabile.

I valori devono essere compatibili con OAuth, PWA e WebAuthn.

---

# 28. Upload CSV security

Gli upload devono avere:

- limite dimensionale;
- validazione MIME/estensione;
- parsing sicuro;
- timeout;
- limite righe;
- protezione da CSV injection;
- nessuna esecuzione del contenuto;
- cleanup dei file temporanei.

### CSV injection

Valori che iniziano con caratteri come `=`, `+`, `-`, `@` devono essere trattati con attenzione quando successivamente vengono esportati in CSV.

Pecunia non deve eseguire formule provenienti dai dati importati.

---

# 29. Rate limiting

Applicare rate limiting almeno a:

- login/callback sensibili;
- passkey endpoints;
- API Open Banking;
- upload CSV;
- endpoint di ricerca potenzialmente abusabili;
- admin endpoints.

I limiti devono essere configurabili.

---

# 30. Input validation

Validation layer obbligatorio.

Esempi:

- amount > 0 quando richiesto;
- currency ISO 4217;
- date valida;
- UUID valido;
- string length limit;
- enum allow-list;
- numero massimo di payment split;
- numero massimo di tag;
- numero massimo righe import.

---

# 31. Financial integrity

Le regole monetarie devono essere protette sia dall'applicazione sia dal database dove possibile.

Esempi:

```text
sum(payments) = total_amount
```

```text
0 <= personal_amount <= total_amount
```

```text
PSD2 accepted -> max one linked Expense
```

Queste regole non possono essere affidate al frontend.

---

# 32. Concorrenza PSD2

Due richieste simultanee non devono poter trasformare la stessa transazione in due spese.

Utilizzare:

- transazione DB;
- row locking o optimistic concurrency;
- unique constraint sul collegamento PSD2;
- idempotency key quando appropriato.

---

# 33. PWA security

Il service worker non deve intercettare e memorizzare indiscriminatamente risposte finanziarie.

Cache strategy:

- asset statici: cache-first appropriato;
- dati finanziari: network-first/no-store secondo caso d'uso;
- dati autenticati sensibili: evitare caching persistente non necessario.

La PWA non deve conservare offline un database completo delle spese in V1.

---

# 34. Browser storage

Non conservare in `localStorage`:

- token di sessione sensibili;
- PSD2 token;
- encryption key;
- dati bancari completi.

IndexedDB può essere utilizzato per dati UI non sensibili/cache limitate, ma non deve diventare il database finanziario offline della V1.

---

# 35. Encryption in transit

Tutte le comunicazioni:

```text
Browser → Reverse Proxy → Backend
Backend → Database
Backend → PSD2 Provider
```

devono essere protette secondo il contesto di deployment.

Per traffico locale Docker, la cifratura interna può essere valutata in base al threat model; non deve però portare a esporre porte DB inutilmente.

---

# 36. Docker security

Ogni container deve:

- utilizzare immagini minimali e mantenute;
- evitare privilegi root quando possibile;
- esporre solo porte necessarie;
- avere filesystem read-only quando compatibile;
- utilizzare volumi solo necessari;
- non montare `/var/run/docker.sock` salvo assoluta necessità;
- utilizzare network Docker separate secondo architettura.

Il backend non deve poter amministrare Docker.

---

# 37. Network segmentation

Architettura minima consigliata:

```text
Internet
   ↓
Reverse Proxy
   ↓
Frontend / API
   ↓
Database
```

Il database non deve essere pubblicato su Internet.

I container devono comunicare tramite network Docker private.

---

# 38. Database credentials

Le credenziali DB devono essere separate dalle credenziali applicative.

Non utilizzare:

```text
postgres/postgres
```

in produzione.

Il database deve avere un utente applicativo con privilegi minimi necessari.

---

# 39. Least privilege

Principio generale:

> ogni componente deve avere solo i privilegi necessari.

Esempio:

- frontend: nessun accesso DB;
- API: accesso DB applicativo;
- worker PSD2: accesso alle sole risorse necessarie;
- reverse proxy: nessun accesso DB;
- monitoring: accesso read-only quando possibile.

---

# 40. Dependency security

Le dipendenze devono essere:

- versionate;
- aggiornabili;
- sottoposte a vulnerability scan;
- prive di dipendenze inutili.

Il progetto deve preferire poche dipendenze mature rispetto a molte librerie per funzionalità marginali.

Questo è particolarmente importante dato il vincolo di leggerezza sul NAS.

---

# 41. Secrets nel GitHub repository

Devono essere ignorati almeno:

```text
.env
.env.*
*.pem
*.key
*.p12
credentials.json
secrets/
```

con eventuali eccezioni esplicite per template/documentazione non sensibile.

Il repository non deve contenere dati reali di utenti o banche.

---

# 42. CI security

La pipeline CI deve eseguire almeno:

- lint;
- unit test;
- test API;
- dependency vulnerability check quando disponibile;
- secret scanning quando disponibile.

Le build devono fallire se vengono rilevati errori critici definiti dalla policy del progetto.

---

# 43. Error handling

Gli errori mostrati all'utente devono essere generici quando l'informazione tecnica potrebbe facilitare un attacco.

Esempio login:

Preferire un messaggio neutro quando appropriato, evitando di rivelare dettagli interni dell'identity flow.

Gli errori tecnici completi devono essere disponibili nei log protetti tramite `request_id`.

---

# 44. Privacy

Pecunia deve seguire il principio di minimizzazione.

Conservare solo ciò che serve per:

- contabilizzazione;
- dashboard;
- gruppi;
- audit;
- integrazioni;
- sicurezza.

Non raccogliere dati comportamentali estranei al funzionamento dell'app.

---

# 45. Retention

La V1 deve prevedere una politica documentata di retention per:

- audit;
- log tecnici;
- transazioni PSD2 ignorate;
- import CSV temporanei;
- dati di sincronizzazione.

I file temporanei CSV devono essere eliminati dopo il completamento o annullamento dell'import, salvo necessità documentata.

---

# 46. GDPR readiness

Il sistema deve essere predisposto per:

- esportazione dati utente;
- cancellazione account secondo policy;
- rettifica dati;
- minimizzazione;
- audit delle operazioni amministrative;
- gestione dei consensi Open Banking.

La conformità legale definitiva richiede valutazione specifica e non viene dichiarata automaticamente dalla semplice implementazione tecnica.

---

# 47. Account deletion

La V1 deve prevedere almeno un percorso amministrativo/backend per la futura cancellazione dell'account.

La cancellazione di dati finanziari deve considerare:

- gruppi;
- spese condivise;
- audit;
- riferimenti PSD2;
- requisiti legali di retention.

Non effettuare cascade delete indiscriminato.

---

# 48. Monitoring security

Monitorare almeno:

- error rate;
- authentication failures aggregate;
- PSD2 sync failures;
- anomalie di rate limiting;
- errori DB;
- container health.

Evitare di monitorare o salvare contenuti finanziari non necessari.

---

# 49. Incident response

In caso di sospetta compromissione devono essere possibili almeno:

1. revoca sessioni;
2. disabilitazione account;
3. revoca/disconnessione connessioni PSD2;
4. rotazione secret;
5. verifica audit;
6. restore da backup se necessario.

Queste procedure devono essere documentate per il deployment sul NAS.

---

# 50. Security checklist prima del rilascio V1

Prima di dichiarare Pecunia pronta:

- [ ] HTTPS attivo;
- [ ] Google OAuth configurato correttamente;
- [ ] session cookie sicuro;
- [ ] nessun secret nel repository;
- [ ] authorization verificata su tutte le API;
- [ ] protezione IDOR/BOLA testata;
- [ ] SQL injection testata;
- [ ] XSS testata;
- [ ] CSRF gestita dove applicabile;
- [ ] rate limiting attivo;
- [ ] upload CSV protetto;
- [ ] token PSD2 non loggati;
- [ ] webhook verificati;
- [ ] idempotenza PSD2 verificata;
- [ ] database non esposto pubblicamente;
- [ ] backup cifrato;
- [ ] restore testato;
- [ ] encryption key non recuperabile dalla PWA;
- [ ] audit attivo;
- [ ] dependency scan eseguito;
- [ ] container senza privilegi inutili;
- [ ] PWA non memorizza il ledger finanziario completo offline.

---

# 51. Regole per Codex

Codex deve considerare questo documento come vincolo architetturale.

Non deve:

- inventare un sistema di autenticazione locale;
- mettere secret nel frontend;
- salvare token sensibili in localStorage;
- esporre il database;
- affidare l'autorizzazione al frontend;
- salvare credenziali bancarie;
- creare cifratura custom;
- loggare payload sensibili;
- aggiungere dipendenze pesanti senza motivo;
- introdurre un sistema AI locale pesante per i suggerimenti V1.

In caso di dubbio tra semplicità e complessità, preferire la soluzione più semplice che mantenga il requisito di sicurezza.

---

# 52. Principio finale

La sicurezza di Pecunia deve essere proporzionata al fatto che si tratta di un'applicazione personale/self-hosted ma che tratta dati finanziari reali.

Non bisogna costruire un sistema bancario enterprise inutile per un NAS domestico, ma nemmeno considerare il self-hosting come una misura di sicurezza sufficiente.

Il target è:

**superficie d'attacco ridotta + privilegi minimi + dati minimizzati + cifratura + autenticazione robusta + authorization server-side + backup recuperabile + implementazione leggera.**
