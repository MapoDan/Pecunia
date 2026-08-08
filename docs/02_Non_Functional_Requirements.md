# Pecunia — Requisiti non funzionali

**Versione:** 1.0  
**Stato:** V1 consolidata  
**Scope:** PWA + backend self-hosted su NAS

Questo documento definisce i requisiti di qualità e i vincoli tecnici trasversali di Pecunia. I requisiti funzionali sono in `01_Functional_Requirements.md`.

---

# 1. Obiettivi non funzionali

Pecunia deve essere:

- veloce nell'uso quotidiano;
- leggera sul NAS;
- affidabile nella gestione dei dati finanziari;
- sicura per dati personali e finanziari;
- facilmente ripristinabile a livello backend;
- installabile come PWA;
- mantenibile tramite container;
- osservabile senza introdurre una piattaforma di monitoring eccessivamente pesante;
- estendibile senza obbligare a una complessità prematura.

---

# 2. Performance

## NFR-001 — Risposta UI

Le operazioni interattive comuni devono dare un feedback immediato all'utente.

Target progettuale:
- azioni locali/UI: percezione immediata, idealmente <100 ms;
- richieste backend comuni: target p95 <= 500 ms in condizioni normali della LAN;
- operazioni di ricerca/lista: target p95 <= 700 ms con database di dimensioni realistiche;
- caricamento iniziale della PWA: minimizzare JavaScript e asset necessari al primo rendering.

Questi valori sono target di progetto e dovranno essere verificati con benchmark reali; non devono essere ottenuti sacrificando correttezza o sicurezza.

## NFR-002 — Inserimento spesa

Il percorso di inserimento rapido deve evitare chiamate di rete non necessarie prima della possibilità di salvare.

Se il suggerimento automatico richiede backend, la spesa deve comunque poter essere salvata senza attendere elaborazioni costose.

## NFR-003 — Dashboard

Le dashboard devono evitare di ricalcolare ogni volta l'intero storico quando una query aggregata o una cache mirata può ottenere lo stesso risultato.

Le query devono essere progettate con indici appropriati e con paginazione dove applicabile.

---

# 3. Vincoli hardware NAS

## NFR-010 — Resource efficiency

Il backend deve essere progettato per funzionare su un NAS domestico meno potente di un notebook commerciale.

Target iniziale:
- nessun servizio deve richiedere GPU;
- evitare processi AI residenti pesanti;
- evitare microservizi aggiunti solo per moda architetturale;
- consumo RAM prevedibile;
- CPU prevalentemente idle quando l'app non viene utilizzata intensivamente.

## NFR-011 — Architettura microservizi pragmatica

Pecunia deve essere predisposta a una struttura a microservizi, ma il termine microservizio non deve essere interpretato come obbligo di creare un container per ogni funzione minima.

Ogni servizio deve avere una responsabilità chiara e un costo operativo giustificato.

## NFR-012 — Background jobs

Le attività non interattive, come classificazione differita, sincronizzazione PSD2, rilevazione ricorrenze e backup, devono essere eseguite senza bloccare le richieste utente.

La tecnologia di scheduling/queue dovrà essere scelta in funzione del costo in RAM e complessità.

---

# 4. Scalabilità

## NFR-020 — Crescita storico

Il sistema deve poter gestire uno storico di molti anni senza degradare sensibilmente le operazioni quotidiane.

Le operazioni di ricerca, filtro e dashboard devono lavorare con query indicizzate e aggregazioni efficienti.

## NFR-021 — Multiutente

L'architettura deve supportare più utenti e gruppi senza assumere che esista un solo proprietario dei dati.

## NFR-022 — Separazione tenant/logica

I dati personali e quelli condivisi devono avere confini di autorizzazione espliciti.

La sicurezza non deve dipendere da filtri applicati solo dal frontend.

---

# 5. Affidabilità e integrità dati

## NFR-030 — Integrità transazionale

Le operazioni che modificano insieme spesa, split di pagamento e collegamenti PSD2 devono essere atomiche dove necessario.

Non deve essere possibile lasciare una spesa con split parziali o riferimenti PSD2 incoerenti a seguito di un errore.

## NFR-031 — Idempotenza

Le operazioni di import e sincronizzazione che possono essere ripetute devono essere progettate per evitare duplicazioni.

Questo è particolarmente importante per PSD2 e CSV.

## NFR-032 — Errori parziali

Un errore durante una sincronizzazione o un import non deve corrompere i dati già validati.

Il sistema deve poter indicare quali elementi sono riusciti e quali richiedono intervento.

## NFR-033 — Date e timezone

Il backend deve usare una gestione esplicita e coerente di date, orari e timezone.

Le spese devono essere rappresentate nella timezone dell'utente/gruppo appropriato, mentre timestamp tecnici e sincronizzazioni devono essere conservati in formato non ambiguo.

---

# 6. Sicurezza

## NFR-040 — HTTPS

Tutte le comunicazioni remote con il backend devono avvenire tramite HTTPS quando l'applicazione è esposta oltre il perimetro locale.

## NFR-041 — OAuth

Le credenziali e i token Google non devono essere esposti al frontend oltre quanto necessario al protocollo di autenticazione.

Segreti OAuth esclusivamente lato backend/configurazione sicura.

## NFR-042 — Autorizzazione server-side

Ogni endpoint che accede a dati finanziari deve verificare:
- identità utente;
- appartenenza al contesto personale/gruppo;
- ruolo;
- eventuali permessi specifici.

## NFR-043 — Input validation

Tutti gli input provenienti da frontend, CSV, provider PSD2 o integrazioni devono essere validati e normalizzati lato backend.

## NFR-044 — Protezione da accessi indiretti

Non deve essere possibile ottenere dati di un altro utente modificando semplicemente un identificativo nell'URL o nel payload API.

## NFR-045 — Secrets

Nel repository non devono essere presenti:
- password;
- token OAuth;
- chiavi API;
- chiavi di cifratura;
- certificati privati;
- credenziali database.

Devono essere forniti tramite secrets/environment/configurazione sicura.

---

# 7. Privacy

## NFR-050 — Minimizzazione dati

Devono essere memorizzati solo i dati necessari alle funzionalità concordate.

## NFR-051 — Separazione personale/condiviso

Una spesa personale non deve essere visibile ai membri di un gruppo salvo esplicita condivisione.

## NFR-052 — Dati bancari

Le informazioni provenienti da PSD2 devono essere trattate come dati sensibili dell'applicazione.

Il sistema deve conservare il minimo necessario per identificare e tracciare il movimento e la relativa fonte.

## NFR-053 — Logging privacy-aware

I log applicativi non devono contenere indiscriminatamente:
- numeri completi di conto;
- token;
- chiavi;
- dati finanziari completi;
- informazioni personali non necessarie.

Quando necessario usare mascheramento/redazione.

---

# 8. Cifratura e backup

## NFR-060 — Database cifrato

Il database deve essere cifrato con una soluzione appropriata al database scelto e all'ambiente self-hosted.

La cifratura deve essere compatibile con backup e ripristino.

## NFR-061 — Backup cifrato

I backup devono essere cifrati e non devono dipendere dalla disponibilità della PWA.

## NFR-062 — Chiave di ripristino

La chiave necessaria per il ripristino deve essere mostrata solo durante la configurazione iniziale e non deve essere recuperabile dall'interfaccia applicativa in seguito.

La gestione pratica della chiave deve essere documentata come procedura operativa separata.

## NFR-063 — Verifica backup

Il sistema di backup dovrebbe poter verificare che il backup sia stato creato correttamente. Un backup dichiarato "OK" deve essere distinguibile da un file semplicemente generato senza verifica.

## NFR-064 — Restore test

La strategia operativa deve prevedere test periodici di ripristino, perché l'esistenza del backup non è di per sé prova della sua recuperabilità.

---

# 9. Disponibilità e resilienza

## NFR-070 — Graceful degradation

Se un'integrazione esterna, come PSD2, non è disponibile, le funzionalità locali dell'applicazione devono rimanere utilizzabili quando possibile.

## NFR-071 — PSD2 offline/error state

Un errore di sincronizzazione PSD2 deve essere mostrato come stato dell'integrazione e non deve impedire la consultazione dello storico già disponibile.

## NFR-072 — Database unavailable

Se il database non è raggiungibile, il backend deve restituire un errore controllato. Il frontend deve mostrare uno stato comprensibile senza tentare operazioni di scrittura indefinite.

---

# 10. PWA e compatibilità

## NFR-080 — PWA

Pecunia deve essere installabile come Progressive Web App sui browser compatibili.

## NFR-081 — Responsive

La UI deve essere mobile-first ma utilizzabile anche su desktop.

## NFR-082 — Touch

Le azioni principali devono essere ottimizzate per touch, inclusa la gestione delle operazioni PSD2 dal Centro Attività.

## NFR-083 — Passkey compatibility

L'implementazione futura delle passkey deve utilizzare WebAuthn standard e non dipendere da un singolo produttore di dispositivo.

## NFR-084 — Offline scope

La V1 non deve promettere un funzionamento offline completo. È ammesso il caching della shell PWA e di asset statici, ma le operazioni finanziarie devono essere confermate dal backend prima di essere considerate definitivamente registrate.

---

# 11. Accessibilità

## NFR-090 — WCAG-oriented

La UI deve seguire le buone pratiche WCAG applicabili:
- contrasto adeguato;
- focus visibile;
- controlli con label semantiche;
- navigazione da tastiera dove pertinente;
- messaggi di errore comprensibili;
- dimensioni touch adeguate.

## NFR-091 — Non dipendere solo dal colore

Stati come "sospesa", "confermata", "errore" e "straordinaria" non devono essere identificati esclusivamente tramite colore.

---

# 12. Manutenibilità

## NFR-100 — Containerizzazione

I componenti backend devono essere eseguibili tramite container Docker e configurabili tramite environment/secrets.

## NFR-101 — Configurazione

La configurazione specifica dell'ambiente non deve essere hardcoded nel codice.

## NFR-102 — Versionamento database

Ogni modifica allo schema deve essere gestita tramite migration versionate.

## NFR-103 — Documentazione API

Le API devono avere uno schema documentato e aggiornato, preferibilmente OpenAPI.

## NFR-104 — Health checks

I servizi devono fornire health/readiness checks utili all'orchestrazione Docker e al monitoring.

---

# 13. Osservabilità

## NFR-110 — Logging strutturato

I servizi devono produrre log strutturati e facilmente filtrabili.

Devono essere distinguibili almeno:
- INFO;
- WARNING;
- ERROR.

## NFR-111 — Correlation ID

Le richieste distribuite tra servizi dovrebbero poter essere ricondotte tramite un correlation/request ID.

## NFR-112 — Metriche tecniche

Devono essere monitorabili almeno:
- stato servizi;
- error rate;
- latenza API;
- utilizzo CPU/RAM/container;
- stato database;
- stato sincronizzazioni PSD2;
- stato backup.

Le metriche tecniche devono essere separate dalle dashboard finanziarie degli utenti.

---

# 14. Evolvibilità

## NFR-120 — API versioning

Le API devono poter evolvere senza rompere immediatamente client già distribuiti.

## NFR-121 — Provider abstraction

Le integrazioni esterne, in particolare autenticazione Google e PSD2, devono essere isolate dietro interfacce/adapter per consentire l'aggiunta futura di provider senza riscrivere il dominio.

## NFR-122 — Feature boundaries

Le funzionalità future, come budget, allegati o ulteriori provider di login, non devono essere implementate in V1 solo per anticiparle. L'architettura deve semplicemente evitare di renderle impossibili.

---

# 15. Test e qualità

## NFR-130 — Automated tests

Il progetto deve avere test automatici per:
- business rules;
- API;
- autorizzazione;
- calcolo importi;
- split;
- PSD2;
- import CSV;
- migration;
- notifiche critiche.

## NFR-131 — Regression safety

Ogni modifica a una regola contabile deve avere test di regressione.

## NFR-132 — Static analysis

Il codice deve essere sottoposto agli strumenti di linting/type checking appropriati allo stack scelto.

---

# 16. Sicurezza operativa

## NFR-140 — Least privilege

I container e i servizi devono essere eseguiti con i privilegi minimi necessari.

## NFR-141 — Dipendenze

Le dipendenze devono essere versionate e aggiornate con processo controllato. Evitare dipendenze inutili.

## NFR-142 — Container security

I container dovrebbero:
- usare immagini minimali quando ragionevole;
- evitare root quando possibile;
- avere filesystem read-only dove compatibile;
- non contenere secrets statici;
- avere healthcheck.

---

# 17. Requisiti specifici per Codex

Codex deve trattare questi requisiti come vincoli di progetto, non come suggerimenti estetici.

In particolare non deve:

1. introdurre un LLM locale per classificare le spese se una soluzione a regole/storico è sufficiente;
2. introdurre un message broker solo per ottenere "microservizi";
3. salvare token o chiavi nel repository;
4. spostare il backup nella PWA;
5. fare affidamento sul frontend per l'autorizzazione;
6. registrare automaticamente operazioni PSD2;
7. creare spese future dalle ricorrenze;
8. trattare un prelievo come spesa automaticamente;
9. perdere il riferimento tra spesa e movimento PSD2 originario;
10. sacrificare l'integrità transazionale per ottenere prestazioni marginalmente migliori.

---

# 18. Target di qualità V1

Prima del rilascio devono essere verificati almeno:

- funzionamento su ambiente Docker del NAS;
- consumo di RAM/CPU sotto carico rappresentativo;
- tempi di risposta delle operazioni principali;
- correttezza delle aggregazioni dashboard;
- correttezza degli split;
- comportamento PSD2 in caso di duplicati/errori;
- autorizzazione tra utenti e gruppi;
- backup e restore reali;
- migrazione database da una versione all'altra;
- assenza di secrets nel repository;
- comportamento PWA su smartphone e desktop supportati.

I target numerici definitivi potranno essere raffinati dopo la scelta dello stack e la disponibilità di un ambiente benchmark reale.
