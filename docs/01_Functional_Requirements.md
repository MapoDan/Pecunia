# Pecunia — Requisiti funzionali

**Versione:** 1.0  
**Stato:** Draft funzionale consolidato  
**Scope:** V1

## 1. Convenzioni

Ogni requisito è identificato da un codice `FR-XXX`.

Priorità:
- **MUST:** indispensabile per la V1.
- **SHOULD:** importante, ma può essere completato dopo il nucleo MVP senza modificare il modello fondamentale.
- **COULD:** utile ma non necessario al primo rilascio.

Quando un comportamento non è definito in questo documento, l'implementazione non deve inventare una regola contabile: deve essere trattato come decisione aperta.

---

# 2. Autenticazione e account

## FR-001 — Login Google
**Priorità:** MUST

Il sistema deve permettere l'accesso tramite Google OAuth/OpenID Connect.

Criteri di accettazione:
- l'utente può autenticarsi con il proprio account Google;
- il backend verifica l'identità ricevuta dal provider;
- non vengono memorizzate password Google;
- un nuovo utente viene creato al primo accesso;
- un utente esistente viene riconosciuto senza creare duplicati.

## FR-002 — Profilo utente
**Priorità:** MUST

Il sistema deve mantenere almeno:
- identificativo interno;
- identificativo Google;
- email;
- nome visualizzato;
- stato account;
- preferenze applicative necessarie.

## FR-003 — Passkey
**Priorità:** SHOULD

Dopo il primo login Google l'utente deve poter registrare una o più passkey WebAuthn.

La passkey deve essere un metodo alternativo di accesso e non un secondo fattore obbligatorio nella V1.

Deve essere possibile revocare una passkey.

## FR-004 — Logout e sessioni
**Priorità:** MUST

L'utente deve poter effettuare logout. Il backend deve gestire sessioni/token in modo sicuro e permettere la revoca delle sessioni secondo il modello di autenticazione scelto.

---

# 3. Onboarding

## FR-005 — Primo accesso
**Priorità:** MUST

Al primo accesso il sistema deve creare il profilo e applicare configurazioni predefinite per un nuovo utente.

La configurazione iniziale deve minimizzare le richieste manuali.

## FR-006 — Gruppo personale
**Priorità:** MUST

Ogni utente deve avere un contesto personale distinto dai gruppi condivisi. Il gruppo/contesto personale non deve essere trattato come un gruppo condiviso con gli stessi permessi.

---

# 4. Gestione spese

## FR-010 — Creazione manuale spesa
**Priorità:** MUST

L'utente deve poter creare una spesa manualmente.

Informazioni essenziali:
- importo;
- descrizione/negozio o informazione equivalente sufficiente a identificare la spesa.

Altri dati devono essere suggeriti o compilabili successivamente, evitando un form obbligatoriamente lungo.

## FR-011 — Inserimento rapido
**Priorità:** MUST

Il flusso principale deve consentire di registrare rapidamente almeno importo e descrizione.

Obiettivo UX: registrazione in pochi secondi.

## FR-012 — Parsing della descrizione
**Priorità:** SHOULD

L'utente può inserire una descrizione libera, ad esempio:

`30,50 Esselunga carta`

Il sistema deve poter estrarre/suggerire:
- importo;
- negozio;
- categoria;
- metodo di pagamento.

Il risultato deve essere verificabile e modificabile.

## FR-013 — Modifica spesa
**Priorità:** MUST

Una spesa registrata deve poter essere modificata manualmente, nel rispetto dei permessi del relativo contesto.

## FR-014 — Eliminazione spesa
**Priorità:** MUST

Una spesa deve poter essere eliminata secondo le autorizzazioni previste. L'eliminazione non deve lasciare riferimenti incoerenti a movimenti PSD2 collegati.

## FR-015 — Data della spesa
**Priorità:** MUST

Una spesa manuale/importata può avere una data nel passato.

La data deve essere distinta dalla data di rilevazione/importazione del dato.

---

# 5. Importi e pagamenti

## FR-020 — Importo totale
**Priorità:** MUST

Ogni spesa contabilizzata deve avere un importo totale coerente con i relativi pagamenti.

## FR-021 — Pagamento multiplo
**Priorità:** MUST

Una spesa può essere finanziata tramite più modalità.

Esempio:

`Totale 50 €`

- Buono pasto: 20 €
- Carta: 30 €

La somma degli split deve corrispondere al totale della spesa.

## FR-022 — Metodi di pagamento
**Priorità:** MUST

Il sistema deve supportare almeno concetti equivalenti a:
- carta;
- contanti;
- bonifico;
- buono pasto;
- Satispay;
- Splitwise;
- altri metodi configurati dal catalogo applicativo.

Il modello non deve legare l'analisi principale alla singola carta 1/2/3: la dashboard deve poter aggregare per tipo di pagamento.

## FR-023 — Commissioni bancarie
**Priorità:** SHOULD

Il sistema deve poter rappresentare commissioni applicate dalla banca quando pertinenti a un'operazione/spesa, senza confonderle con l'importo principale.

La semantica precisa di aggregazione nelle dashboard deve essere definita nelle business rules.

## FR-024 — Ripartizione personale della spesa
**Priorità:** MUST

L'utente deve poter indicare che una spesa rilevata ha una quota effettivamente a proprio carico diversa dall'importo del movimento.

Esempio:

Movimento: 10 €  
Quota utente: 5 €  
Quota altra persona: 5 €

Nel bilancio personale deve risultare 5 €.

---

# 6. Categorie e classificazione

## FR-030 — Categorie standard
**Priorità:** MUST

Pecunia deve utilizzare un catalogo di categorie e sottocategorie standard predefinito dall'applicazione.

Nella V1 l'utente non crea liberamente nuove categorie.

## FR-031 — Sottocategorie
**Priorità:** MUST

Le categorie possono avere sottocategorie standard.

## FR-032 — Suggerimento categoria
**Priorità:** MUST

Il sistema deve proporre categoria e sottocategoria usando, quando disponibili:
- negozio/esercente;
- descrizione;
- causale bancaria;
- storico dell'utente;
- contesto/gruppo;
- regole di classificazione.

## FR-033 — Conferma classificazione
**Priorità:** MUST

I suggerimenti devono essere modificabili. Il sistema non deve considerare una classificazione incerta come verità senza un comportamento esplicitamente previsto dalle regole di business.

## FR-034 — Apprendimento leggero
**Priorità:** SHOULD

Il classificatore deve poter utilizzare le correzioni dell'utente per migliorare suggerimenti futuri senza richiedere modelli AI pesanti.

---

# 7. Negozi/esercenti

## FR-040 — Negozio
**Priorità:** MUST

Una spesa deve poter essere associata a un negozio/esercente.

## FR-041 — Normalizzazione esercente
**Priorità:** SHOULD

Il sistema dovrebbe riconoscere che descrizioni diverse possono riferirsi allo stesso esercente, soprattutto per operazioni PSD2.

## FR-042 — Suggerimento da causale PSD2
**Priorità:** SHOULD

La causale bancaria può essere utilizzata per suggerire esercente e classificazione.

---

# 8. Spese straordinarie

## FR-050 — Flag straordinaria
**Priorità:** MUST

Ogni spesa deve poter essere identificata come:
- ordinaria;
- straordinaria.

## FR-051 — Analisi con/escludendo straordinarie
**Priorità:** MUST

Le dashboard devono permettere di includere o escludere le spese straordinarie.

Esempi:
- acquisto casa;
- arredi;
- grandi acquisti eccezionali.

Lo scopo è permettere il confronto delle normali abitudini di spesa senza che eventi eccezionali distorcano le statistiche.

---

# 9. Tag

## FR-060 — Tag personali
**Priorità:** MUST

L'utente può applicare tag alle spese e creare tag personali.

## FR-061 — Tag globali nel gruppo
**Priorità:** MUST

Quando un tag personale viene utilizzato nel contesto di un gruppo, deve diventare disponibile come tag globale del gruppo.

## FR-062 — Amministrazione tag di gruppo
**Priorità:** MUST

L'amministratore del gruppo può:
- mantenere il tag;
- modificarne il nome;
- eliminarlo.

---

# 10. Gruppi condivisi

## FR-070 — Creazione gruppo
**Priorità:** MUST

Un utente autorizzato deve poter creare un gruppo condiviso.

## FR-071 — Invito membri
**Priorità:** MUST

L'amministratore deve poter invitare membri al gruppo e rimuoverli secondo le regole di autorizzazione.

## FR-072 — Ruoli
**Priorità:** MUST

Devono esistere almeno i ruoli:
- Amministratore;
- Membro;
- Supervisionato;
- Solo lettura.

## FR-073 — Conto condiviso del gruppo
**Priorità:** MUST

Un conto bancario cointestato/ad hoc può essere associato direttamente a un gruppo.

Le operazioni importate da quel conto appartengono al contesto del gruppo.

## FR-074 — Isolamento conti personali
**Priorità:** MUST

Un conto personale non deve rendere automaticamente visibili le relative operazioni agli altri membri di un gruppo.

## FR-075 — Figli supervisionati
**Priorità:** MUST

I genitori/amministratori devono poter vedere lo stato delle spese degli utenti con ruolo Supervisionato, tipicamente figli.

---

# 11. PSD2 / Open Banking

## FR-080 — Collegamento conto
**Priorità:** MUST

L'utente deve poter collegare un conto tramite un'integrazione PSD2 supportata.

## FR-081 — Data iniziale sincronizzazione
**Priorità:** MUST

Quando un conto viene collegato per la prima volta, la sincronizzazione automatica deve partire dalla data di collegamento.

Non deve essere recuperato automaticamente uno storico pluriennale precedente.

## FR-082 — Origine del movimento
**Priorità:** MUST

Ogni operazione PSD2 deve conservare e mostrare chiaramente il collegamento/conto da cui deriva.

Esempio UI:

`Identificata da conto Fineco`

## FR-083 — Operazioni sospese
**Priorità:** MUST

Le operazioni PSD2 rilevate non vengono registrate automaticamente come spese.

Devono essere inserite in una lista di operazioni sospese in attesa di decisione.

## FR-084 — Decisione da Centro Attività
**Priorità:** MUST

Dal Centro Attività l'utente deve poter toccare una singola operazione sospesa e:
- registrarla;
- modificarne i dettagli;
- decidere di non registrarla.

Il flusso deve richiedere il minor numero possibile di passaggi.

## FR-085 — Prelievi
**Priorità:** MUST

Un prelievo rilevato via PSD2 non deve diventare automaticamente una spesa.

L'utente può decidere di registrarlo solo se rappresenta effettivamente una spesa sostenuta che vuole contabilizzare; in alternativa può ignorarlo e registrare successivamente le spese in contanti.

## FR-086 — Modifica importo PSD2
**Priorità:** MUST

Quando un'operazione PSD2 viene contabilizzata, l'utente deve poter modificare l'importo della spesa risultante.

Esempio:

Movimento PSD2: 5 €  
Spesa reale: 15 €

L'utente può aggiungere 10 € di buono pasto tramite gli split di pagamento e portare il totale della spesa a 15 €.

## FR-087 — Collegamento movimento/spesa
**Priorità:** MUST

La spesa derivata da PSD2 deve mantenere il riferimento al movimento originario, anche quando il totale della spesa viene modificato o ripartito.

## FR-088 — Commissioni PSD2
**Priorità:** SHOULD

Il sistema deve poter rappresentare eventuali commissioni bancarie associate al movimento.

## FR-089 — Aggiornamenti storico
**Priorità:** MUST

Lo storico non deve essere modificato automaticamente.

Quando vengono individuate operazioni che necessitano aggiornamenti, il sistema crea una notifica:

`Individuate X operazioni che necessitano aggiornamenti`

L'utente apre la lista e decide se procedere. Se procede, l'aggiornamento può essere applicato automaticamente secondo le regole definite.

Se l'utente elimina/ignora la notifica, essa non deve essere riproposta per lo stesso evento.

---

# 12. Import CSV

## FR-090 — Import storico
**Priorità:** MUST

L'utente deve poter importare spese storiche da CSV, inclusi dati derivati da un precedente Excel.

## FR-091 — Data import
**Priorità:** MUST

L'import CSV può contenere date precedenti alla creazione dell'account o al collegamento PSD2.

## FR-092 — Area configurazione
**Priorità:** MUST

L'import CSV deve essere accessibile dalla sezione di configurazione/gestione account, insieme alle funzioni di collegamento account e gestione plugin/integrations.

## FR-093 — Validazione import
**Priorità:** MUST

Prima del salvataggio definitivo il sistema deve validare i dati importati e segnalare righe non valide.

## FR-094 — Duplicati
**Priorità:** SHOULD

Il sistema deve poter identificare potenziali duplicati durante l'import e permettere una decisione esplicita prima di creare doppie spese.

---

# 13. Ricorrenze

## FR-100 — Rilevazione ricorrenze
**Priorità:** SHOULD

Il sistema deve analizzare lo storico delle spese confermate per individuare pattern ricorrenti.

## FR-101 — Suggerimento ricorrenza
**Priorità:** SHOULD

Una possibile ricorrenza viene proposta all'utente e non creata automaticamente.

## FR-102 — Nessuna generazione futura
**Priorità:** MUST

La ricorrenza non genera automaticamente future spese nella V1.

---

# 14. Centro Attività

## FR-110 — Centro attività
**Priorità:** MUST

Deve esistere un centro attività unico che raccolga elementi che richiedono attenzione.

Almeno:
- operazioni PSD2 sospese;
- aggiornamenti storico disponibili;
- suggerimenti/attività rilevanti;
- notifiche operative.

## FR-111 — Badge attività
**Priorità:** SHOULD

La presenza di attività non lette/deferred deve essere evidenziata nell'interfaccia.

---

# 15. Notifiche

## FR-120 — Notification Center
**Priorità:** MUST

Ogni utente deve avere notifiche interne all'app.

## FR-121 — Push PWA
**Priorità:** SHOULD

Il sistema deve supportare notifiche push tramite capacità della PWA/browser compatibile.

## FR-122 — Email
**Priorità:** SHOULD

Il sistema deve essere predisposto per notifiche email.

## FR-123 — Preferenze notifiche
**Priorità:** SHOULD

L'utente deve poter configurare canale e tipologia delle notifiche.

## FR-124 — Priorità notifiche
**Priorità:** SHOULD

Le notifiche devono avere almeno un livello di priorità per evitare un'esperienza rumorosa.

---

# 16. Dashboard e analisi

## FR-130 — Dashboard personale
**Priorità:** MUST

L'utente deve avere una dashboard con tabelle, grafici e indicatori utili all'analisi delle spese.

## FR-131 — Dashboard configurabile
**Priorità:** MUST

La dashboard deve essere composta da sezioni/widget configurabili.

## FR-132 — Filtri temporali
**Priorità:** MUST

Devono essere disponibili filtri per periodi e confronti temporali.

## FR-133 — Filtri categoria
**Priorità:** MUST

Le analisi devono poter essere filtrate per categoria/sottocategoria.

## FR-134 — Filtri metodo pagamento
**Priorità:** MUST

Le analisi devono poter essere filtrate e aggregate per modalità di pagamento.

## FR-135 — Filtri ordinaria/straordinaria
**Priorità:** MUST

L'utente deve poter includere/escludere le spese straordinarie.

## FR-136 — Ricerca
**Priorità:** MUST

Deve essere disponibile una ricerca sulle spese, almeno per descrizione/negozio e campi indicizzati pertinenti.

## FR-137 — Confronto risultati
**Priorità:** MUST

Le dashboard devono permettere il confronto tra periodi e contesti in modo coerente.

## FR-138 — Dashboard gruppo
**Priorità:** MUST

I gruppi devono poter visualizzare analisi delle spese appartenenti al gruppo, nel rispetto dei ruoli.

## FR-139 — Dashboard amministratore applicazione
**Priorità:** SHOULD

L'utente amministratore dell'applicazione deve avere dashboard separate di utilizzo e performance dell'applicazione, non confuse con le dashboard finanziarie personali.

---

# 17. Backup e ripristino

## FR-150 — Backup backend
**Priorità:** MUST

Il backup del database deve essere gestito a livello backend/infrastrutturale.

La PWA non deve effettuare backup.

## FR-151 — Database cifrato
**Priorità:** MUST

Il database deve essere cifrato secondo una soluzione sicura compatibile con l'architettura scelta.

## FR-152 — Chiave di cifratura
**Priorità:** MUST

La chiave necessaria al ripristino deve essere mostrata all'amministratore solo durante la creazione iniziale.

Dopo la configurazione non deve essere nuovamente visualizzabile dall'applicazione.

## FR-153 — Ripristino
**Priorità:** MUST

Il backend deve permettere di ripristinare un backup cifrato fornendo la chiave necessaria.

La perdita della chiave deve essere considerata una condizione che impedisce il ripristino del backup.

---

# 18. Amministrazione applicativa

## FR-160 — Amministratore globale
**Priorità:** MUST

Deve esistere un utente amministratore dell'applicazione distinto dal semplice amministratore di un gruppo.

## FR-161 — Dashboard utilizzo
**Priorità:** SHOULD

L'amministratore globale deve poter vedere metriche di utilizzo dell'applicazione.

## FR-162 — Dashboard performance
**Priorità:** SHOULD

L'amministratore globale deve poter vedere metriche tecniche e di performance, senza esporre inutilmente dati finanziari degli utenti.

---

# 19. Requisiti di interfaccia funzionale

## FR-170 — Mobile first
**Priorità:** MUST

Le principali operazioni devono essere ottimizzate per smartphone.

## FR-171 — Speed dial
**Priorità:** MUST

Il pulsante di inserimento rapido deve essere sempre facilmente raggiungibile dal contesto principale.

Le azioni rapide devono includere almeno la creazione di una nuova spesa.

## FR-172 — Navigazione
**Priorità:** MUST

La navigazione deve rendere immediatamente accessibili almeno:
- dashboard;
- spese;
- centro attività/notifiche;
- inserimento rapido;
- configurazione/account.

## FR-173 — Configurazione centralizzata
**Priorità:** MUST

La sezione configurazione/gestione account deve raccogliere funzioni quali:
- profilo;
- sicurezza;
- import CSV;
- collegamenti bancari;
- integrazioni/plugin;
- preferenze notifiche;
- impostazioni applicative pertinenti.

---

# 20. Requisiti di coerenza dati

## FR-180 — Nessun dato finanziario inventato
**Priorità:** MUST

Il sistema non deve generare una spesa contabilizzata senza una fonte valida:
- inserimento manuale;
- import esplicito;
- operazione PSD2 confermata dall'utente.

## FR-181 — Somma split
**Priorità:** MUST

Gli split di pagamento devono essere coerenti con il totale registrato.

## FR-182 — Tracciabilità PSD2
**Priorità:** MUST

Una spesa originata da PSD2 deve mantenere la relazione con il movimento originale e la fonte bancaria.

## FR-183 — Isolamento dati
**Priorità:** MUST

Ogni richiesta backend deve verificare che l'utente abbia diritto di accedere alla spesa, al gruppo, al conto o al movimento richiesto.

---

# 21. Criteri generali di accettazione V1

La V1 è funzionalmente accettabile quando:

1. un nuovo utente può autenticarsi con Google e accedere al proprio spazio;
2. può registrare una spesa in pochi secondi;
3. il sistema può suggerire dati senza compromettere la correttezza contabile;
4. una spesa può essere divisa su più metodi di pagamento;
5. una quota personale può essere diversa dall'importo del movimento originario;
6. le spese straordinarie possono essere escluse dalle analisi;
7. è possibile creare e utilizzare gruppi condivisi;
8. un conto condiviso può appartenere a un gruppo;
9. le operazioni PSD2 vengono sempre presentate come sospese prima della registrazione;
10. l'utente può modificare importo e dettagli di un'operazione PSD2 prima della contabilizzazione;
11. è possibile importare storico CSV;
12. dashboard, filtri e ricerca permettono di analizzare le spese;
13. il Centro Attività rende visibili le operazioni che richiedono attenzione;
14. il backend supporta backup cifrati e ripristino tramite chiave;
15. il sistema resta utilizzabile con risorse limitate di un NAS domestico.

---

# 22. Decisioni ancora da definire

Questo documento non deve inventare dettagli che non sono stati ancora concordati. Restano da definire nei documenti successivi, tra gli altri:

- catalogo definitivo categorie/sottocategorie;
- provider PSD2/Open Banking concreto;
- formato CSV e procedura di mapping dettagliata;
- stack tecnologico definitivo;
- schema database dettagliato;
- contratti API;
- specifiche esatte dei widget dashboard;
- policy precise di commissioni;
- retention backup;
- provider email/push;
- browser/device support matrix;
- dettagli visuali del branding Pecunia.
