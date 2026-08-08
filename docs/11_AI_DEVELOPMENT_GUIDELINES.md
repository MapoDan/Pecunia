# Pecunia — AI Development Guidelines

Questo documento è vincolante per gli agenti AI che sviluppano Pecunia, incluso Codex.

## 1. Source of truth

La documentazione presente in `docs/` è la fonte primaria dei requisiti. Prima di implementare una funzionalità, l'agente deve verificare i requisiti e le regole di business pertinenti.

In caso di conflitto tra codice e documentazione, non assumere automaticamente che il codice sia corretto: identificare il conflitto e correggere la documentazione o il codice secondo la decisione più recente esplicitamente approvata.

## 2. Non inventare requisiti

L'agente non deve:

- aggiungere funzionalità non richieste;
- introdurre automaticamente budget, investimenti o gestione patrimoniale;
- creare dati finanziari che non rappresentano movimenti o spese reali;
- modificare una regola di business per semplificare l'implementazione.

Se un dettaglio necessario non è definito, deve essere marcato come decisione aperta oppure proporre una soluzione prima di applicarla a parti strutturali del sistema.

## 3. Priorità

Ordine di priorità:

1. correttezza dei dati finanziari;
2. sicurezza e privacy;
3. rispetto delle business rules;
4. semplicità e manutenibilità;
5. performance sul NAS;
6. UX;
7. ottimizzazioni premature solo se misurate.

## 4. PSD2

Le operazioni PSD2 rilevate sono sospese per definizione. Non devono diventare spese contabilizzate senza una decisione dell'utente.

Una spesa può avere un importo diverso da quello del movimento PSD2 collegato. Il collegamento deve essere preservato per la tracciabilità.

## 5. Separazione dei concetti

Non confondere:

- movimento bancario;
- spesa;
- split di pagamento;
- metodo di pagamento;
- gruppo;
- categoria;
- origine del dato.

Il modello dati deve mantenere queste responsabilità separate.

## 6. Automazione

Il sistema può suggerire classificazioni, gruppi, tag e ricorrenze. I suggerimenti devono essere spiegabili e, quando incidono sulla contabilizzazione, confermabili dall'utente.

Preferire regole leggere e deterministiche rispetto a modelli AI locali pesanti.

## 7. Performance

Ogni servizio deve essere progettato per un NAS domestico:

- evitare processi residenti inutili;
- limitare dipendenze pesanti;
- usare query indicizzate;
- paginare liste e ricerche;
- evitare elaborazioni O(n) non necessarie su grandi dataset;
- spostare i lavori non interattivi in job asincroni solo quando necessario.

## 8. Sicurezza

- Segreti e credenziali solo tramite configurazione sicura/secrets.
- Mai inserire chiavi nel repository.
- Validare input lato backend.
- Applicare autorizzazione server-side, non solo lato UI.
- Loggare eventi tecnici senza esporre dati finanziari non necessari.
- Non loggare token OAuth, chiavi database o dati sensibili completi.

## 9. Database

Le modifiche allo schema devono essere versionate tramite migration. Non usare modifiche manuali non riproducibili in produzione.

Le migration devono essere reversibili quando tecnicamente possibile e testate.

## 10. API

Le API devono avere contratti espliciti e versionati. Errori e validazioni devono avere formato coerente.

L'API deve applicare autorizzazione per utente e gruppo a ogni operazione sensibile.

## 11. Testing

Ogni nuova funzionalità significativa deve includere test automatici.

Priorità dei test:

- business rules;
- autorizzazione;
- calcolo importi e split;
- PSD2;
- import CSV;
- notifiche;
- migration;
- API contract.

## 12. UX

La UI non deve obbligare l'utente a compilare campi non indispensabili per registrare una spesa.

Le operazioni PSD2 sospese devono essere raggiungibili direttamente dal Centro Attività e apribili con un'interazione semplice.

## 13. Cambi architetturali

Prima di introdurre una nuova infrastruttura significativa, verificare se è realmente necessaria. Non aggiungere Redis, message broker, vector database, LLM locali o altri componenti solo perché sono tecnicamente disponibili.

Ogni decisione architetturale significativa deve essere documentata in un ADR.

## 14. Definition of Done

Una funzionalità è completata solo quando:

- requisiti implementati;
- business rules rispettate;
- autorizzazioni verificate;
- test presenti e superati;
- migration presenti se necessarie;
- documentazione aggiornata;
- logging e gestione errori adeguati;
- nessun segreto nel codice;
- comportamento verificato su Docker.
