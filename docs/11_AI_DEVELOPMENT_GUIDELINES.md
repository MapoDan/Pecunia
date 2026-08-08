# Pecunia — AI Development Guidelines

Questo documento è vincolante per l'agente AI che svilupperà Pecunia.

## 1. Source of truth

Prima di implementare qualsiasi funzionalità leggere almeno:

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
- `12_Coding_Standards.md`
- `13_Technology_Decisions.md`
- `14_Implementation_Roadmap.md`
- `15_Acceptance_Criteria.md`
- `Security_Specification.md`
- ADR pertinenti.

La documentazione è la fonte primaria. Questo repository di analisi non contiene l'implementazione dell'applicazione.

## 2. Non inventare requisiti

Non aggiungere funzionalità non richieste, non introdurre budget/investimenti nella V1 e non creare dati finanziari che non rappresentano una spesa reale o un movimento PSD2 effettivamente rilevato.

Se un dettaglio necessario non è definito, identificare l'ambiguità e proporre una decisione prima di introdurre un comportamento strutturale.

## 3. Priorità

1. correttezza finanziaria;
2. sicurezza/privacy;
3. business rules;
4. semplicità/manutenibilità;
5. performance sul NAS;
6. UX;
7. ottimizzazione solo se misurata.

## 4. PSD2

Le operazioni rilevate sono PENDING per definizione. Nessuna diventa spesa senza decisione esplicita dell'utente.

Durante l'accettazione l'importo può cambiare e possono essere aggiunti altri metodi di pagamento. Il collegamento alla transazione bancaria deve rimanere tracciabile.

La sincronizzazione iniziale parte dalla data di collegamento del conto; import CSV/manuali possono avere date storiche.

## 5. Separazione dei concetti

Non confondere movimento bancario, spesa, split di pagamento, metodo di pagamento, gruppo, categoria e origine del dato.

## 6. Automazione

Il sistema può suggerire classificazioni e metadati. I suggerimenti non devono sostituire silenziosamente una decisione contabile dell'utente. Preferire regole leggere e deterministiche.

## 7. Performance

Il NAS è un vincolo architetturale: evitare servizi residenti inutili, dipendenze pesanti, query non indicizzate, full-history downloads e sistemi distribuiti sproporzionati.

## 8. Sicurezza

Segreti solo tramite secret/configuration management. Autorizzazione sempre server-side. Validazione backend. Nessun token/chiave nei log o nel frontend.

## 9. Database

Ogni modifica schema richiede migration versionata e testabile. Le invarianti finanziarie devono essere protette sia dal dominio sia, dove utile, da constraint DB.

## 10. API

API versionate e con contratti espliciti. Errori coerenti, pagination, filtering e idempotenza per comandi finanziari retryable.

## 11. Testing

Priorità: business rules, authorization, importi/split, PSD2 state transitions, CSV import, activity center, migration, API contract e critical E2E journeys.

## 12. UX

Minimo numero di campi obbligatori. Suggerimenti automatici. Le PENDING PSD2 sono raggiungibili direttamente dal Centro Attività e possono essere elaborate toccando la voce.

## 13. Architettura

Non introdurre Redis, broker, vector DB, LLM locale, Kubernetes o altri componenti significativi senza un requisito concreto e un ADR.

## 14. Vertical slices

Seguire la roadmap. Ogni slice deve lasciare il progetto in uno stato coerente e testabile. Non costruire tutto il backend prima di collegare il frontend.

## 15. Definition of Done

Una funzionalità è completata solo quando requisiti, business rules, autorizzazioni, test, migration, error handling, documentazione e acceptance criteria risultano soddisfatti.
