# Pecunia — User Stories

**Versione:** 1.0  
**Scope:** V1

Questo documento traduce i requisiti funzionali in scenari dal punto di vista dell'utilizzatore. Le User Story sono pensate anche come base per acceptance test e backlog di sviluppo.

## Convenzioni

Formato:

> **Come** [attore] **voglio** [azione] **così da** [valore].

Ogni story contiene criteri di accettazione sintetici. I dettagli tecnici appartengono agli altri documenti.

---

# EPIC A — Accesso e onboarding

## US-001 — Primo accesso con Google
**Come** nuovo utente  
**voglio** accedere con Google  
**così da** non dover creare e ricordare una password Pecunia.

**Acceptance criteria**
- Posso completare il login tramite Google.
- Al primo accesso viene creato il mio profilo.
- Un accesso successivo riconosce lo stesso account.
- Non viene creata una seconda identità per la stessa identità Google.

## US-002 — Configurazione iniziale minima
**Come** nuovo utente  
**voglio** trovare impostazioni predefinite già pronte  
**così da** poter iniziare rapidamente.

**Acceptance criteria**
- Le categorie standard sono disponibili.
- I metodi di pagamento standard sono disponibili.
- Non sono obbligato a configurare manualmente ogni elemento prima della prima spesa.

## US-003 — Registrare una passkey
**Come** utente autenticato  
**voglio** registrare una passkey sul mio dispositivo  
**così da** poter accedere rapidamente in futuro.

**Acceptance criteria**
- Posso avviare la registrazione WebAuthn.
- La passkey viene associata al mio account.
- Posso revocarla.

---

# EPIC B — Inserimento quotidiano

## US-010 — Registrare rapidamente una spesa
**Come** utente  
**voglio** inserire una spesa con il minimo numero di informazioni  
**così da** non perdere tempo ogni volta che pago qualcosa.

**Acceptance criteria**
- Il flusso rapido è facilmente raggiungibile.
- Posso inserire almeno importo e descrizione/esercente.
- I dati secondari possono essere suggeriti.
- Posso salvare senza compilare un modulo lungo.

## US-011 — Suggerimenti automatici
**Come** utente  
**voglio** che Pecunia suggerisca categoria, sottocategoria e metodo di pagamento  
**così da** ridurre il lavoro manuale.

**Acceptance criteria**
- I suggerimenti utilizzano lo storico quando disponibile.
- La causale bancaria può contribuire al suggerimento.
- Posso correggere ogni suggerimento.
- Le correzioni possono migliorare suggerimenti futuri.

## US-012 — Inserire una spesa con più metodi
**Come** utente  
**voglio** dividere il pagamento di una spesa tra più modalità  
**così da** rappresentare correttamente ciò che ho realmente pagato.

**Scenario**

Spesa: 50 €
- Buono pasto: 20 €
- Carta: 30 €

**Acceptance criteria**
- Il totale visualizzato è 50 €.
- Gli split sono visibili.
- La somma degli split è coerente con il totale.

## US-013 — Spesa con quota personale diversa dal totale
**Come** utente  
**voglio** indicare quanto della spesa è effettivamente a mio carico  
**così da** non gonfiare il mio bilancio quando una parte è di un'altra persona.

**Scenario**

Spesa rilevata: 10 €  
Quota personale: 5 €  
Quota altra persona: 5 €

**Acceptance criteria**
- Posso registrare la quota personale di 5 €.
- Le dashboard personali considerano 5 € come mia spesa.
- Il dato originario rimane disponibile per la tracciabilità.

## US-014 — Commissione bancaria
**Come** utente  
**voglio** registrare una commissione bancaria associata a un'operazione  
**così da** non perdere costi effettivamente sostenuti.

**Acceptance criteria**
- La commissione può essere memorizzata separatamente dall'importo principale.
- La rappresentazione nelle dashboard segue le regole di business definite.

## US-015 — Spesa straordinaria
**Come** utente  
**voglio** contrassegnare una spesa come straordinaria  
**così da** poter analizzare le mie spese ordinarie senza essere falsato da grandi eventi eccezionali.

**Scenario**

Acquisto arredi da 8.000 €.

**Acceptance criteria**
- Posso applicare il flag straordinaria.
- Posso includere o escludere le straordinarie dalle dashboard.
- L'operazione rimane comunque nello storico.

---

# EPIC C — Classificazione

## US-020 — Correggere una categoria
**Come** utente  
**voglio** modificare una categoria suggerita  
**così da** mantenere corretto il mio storico.

**Acceptance criteria**
- Posso cambiare categoria e sottocategoria prima o dopo il salvataggio secondo i permessi.
- La correzione viene conservata.

## US-021 — Suggerimento da causale bancaria
**Come** utente  
**voglio** che la causale PSD2 contribuisca alla classificazione  
**così da** ridurre l'inserimento manuale.

**Acceptance criteria**
- La causale può essere usata dal motore di suggerimento.
- Il suggerimento non contabilizza automaticamente la spesa.

## US-022 — Tag personale
**Come** utente  
**voglio** associare un tag a una spesa  
**così da** creare analisi trasversali alle categorie.

## US-023 — Rendere globale un tag nel gruppo
**Come** membro di un gruppo  
**voglio** che un tag usato in un gruppo sia disponibile nel gruppo  
**così da** poter analizzare coerentemente le spese condivise.

**Acceptance criteria**
- Il tag diventa disponibile a livello gruppo secondo la regola concordata.
- L'amministratore può modificarlo o eliminarlo.

---

# EPIC D — PSD2 / Open Banking

## US-030 — Collegare un conto
**Come** utente  
**voglio** collegare un conto tramite Open Banking  
**così da** ricevere le operazioni rilevate automaticamente.

**Acceptance criteria**
- Il collegamento viene registrato.
- Viene memorizzata la data di collegamento.
- La sincronizzazione automatica parte da quella data.

## US-031 — Vedere da quale conto arriva un'operazione
**Come** utente con più conti collegati  
**voglio** sapere da quale conto proviene ogni operazione PSD2  
**così da** poterla identificare correttamente.

**Acceptance criteria**
- L'operazione mostra il conto/collegamento di origine.
- L'origine resta associata anche dopo la contabilizzazione.

## US-032 — Decidere se contabilizzare un'operazione PSD2
**Come** utente  
**voglio** che un'operazione bancaria rimanga sospesa  
**così da** decidere personalmente se rappresenta una spesa da registrare.

**Acceptance criteria**
- Le operazioni rilevate entrano nel Centro Attività.
- Nessuna operazione PSD2 diventa spesa automaticamente.
- Posso confermare oppure ignorare.

## US-033 — Contabilizzare una spesa PSD2 con un tap
**Come** utente  
**voglio** aprire direttamente un'operazione sospesa  
**così da** poterla verificare senza navigare attraverso più schermate.

**Acceptance criteria**
- Toccando l'operazione apro il dettaglio/decisione.
- Posso verificare i dati.
- Posso completare la contabilizzazione dal flusso.

## US-034 — Modificare l'importo di una spesa PSD2
**Come** utente  
**voglio** poter correggere l'importo rilevato  
**così da** rappresentare la spesa reale quando il movimento bancario non coincide con il totale della spesa.

**Scenario**

PSD2: Coop 5 €  
Spesa reale: 15 €  
- Carta: 5 €
- Buono pasto: 10 €

**Acceptance criteria**
- Posso portare il totale a 15 €.
- Posso aggiungere lo split da 10 €.
- Il movimento bancario originale da 5 € rimane tracciato.

## US-035 — Ignorare un prelievo
**Come** utente  
**voglio** poter ignorare un prelievo PSD2  
**così da** evitare di registrare due volte le spese in contanti.

**Scenario**

Prelievo 100 € → ignoro il movimento e registro successivamente le singole spese in contanti.

**Acceptance criteria**
- Il prelievo non viene contabilizzato automaticamente.
- Posso ignorarlo dal Centro Attività.
- Posso invece contabilizzarlo se rappresenta effettivamente una spesa che voglio registrare.

## US-036 — Aggiornamento storico controllato
**Come** utente  
**voglio** essere informato quando Pecunia trova operazioni che richiedono aggiornamenti  
**così da** decidere io quando modificare lo storico.

**Acceptance criteria**
- Ricevo una notifica aggregata, ad esempio "Individuate 5 operazioni che necessitano aggiornamenti".
- Posso aprire l'elenco.
- Posso procedere con l'aggiornamento.
- Se ignoro/cancello la notifica, non viene riproposta per lo stesso evento.

---

# EPIC E — Import storico

## US-040 — Importare CSV
**Come** utente  
**voglio** importare un CSV con le mie spese storiche  
**così da** iniziare Pecunia con uno storico già disponibile.

**Acceptance criteria**
- Posso avviare l'import dalla sezione configurazione/account.
- Posso importare date precedenti al primo utilizzo.
- Le righe errate vengono segnalate.
- I dati validi non vengono persi a causa di una riga errata.

## US-041 — Evitare duplicati CSV
**Come** utente  
**voglio** essere avvisato dei potenziali duplicati  
**così da** non alterare artificialmente le mie statistiche.

---

# EPIC F — Gruppi e famiglia

## US-050 — Creare un gruppo condiviso
**Come** utente  
**voglio** creare un gruppo condiviso  
**così da** gestire le spese comuni con altre persone.

## US-051 — Conto condiviso dedicato
**Come** amministratore di un gruppo  
**voglio** associare un conto cointestato al gruppo  
**così da** mantenere separate le spese comuni da quelle personali.

**Acceptance criteria**
- Il conto può essere associato al gruppo.
- Le operazioni del conto sono trattate nel contesto del gruppo.
- Non vengono riversate automaticamente nello spazio personale di un membro.

## US-052 — Conti personali separati
**Come** membro di un gruppo  
**voglio** mantenere il mio conto personale separato  
**così da** non condividere automaticamente le mie spese private.

## US-053 — Visualizzare spese dei figli
**Come** genitore/amministratore  
**voglio** vedere le spese degli utenti supervisionati  
**così da** poter monitorare le spese dei miei figli.

**Acceptance criteria**
- Posso vedere solo gli utenti per i quali ho il relativo permesso.
- Le spese personali di altri membri non diventano visibili senza autorizzazione.

---

# EPIC G — Dashboard e analisi

## US-060 — Vedere dove spendo i soldi
**Come** utente  
**voglio** una dashboard delle mie spese  
**così da** capire dove finiscono i miei soldi.

## US-061 — Confrontare periodi
**Come** utente  
**voglio** confrontare due periodi  
**così da** capire se le mie abitudini stanno cambiando.

## US-062 — Escludere spese straordinarie
**Come** utente  
**voglio** escludere le spese straordinarie  
**così da** ottenere una fotografia più realistica delle spese ordinarie.

## US-063 — Analizzare categorie
**Come** utente  
**voglio** vedere la distribuzione per categoria e sottocategoria  
**così da** individuare le aree in cui spendo di più.

## US-064 — Analizzare metodi di pagamento
**Come** utente  
**voglio** vedere quanto spendo con carta, contanti, Satispay, buoni pasto ecc.  
**così da** capire come sostengo le mie spese.

L'analisi deve privilegiare il tipo di metodo rispetto alla singola carta fisica.

## US-065 — Cercare una spesa
**Come** utente  
**voglio** cercare per negozio/descrizione  
**così da** ritrovare rapidamente un'operazione.

## US-066 — Individuare comportamenti ripetitivi
**Come** utente  
**voglio** che Pecunia evidenzi pattern di spesa ricorrenti  
**così da** poter capire quali costi sono strutturali e quali occasionali.

## US-067 — Dashboard configurabile
**Come** utente  
**voglio** poter configurare le sezioni della dashboard  
**così da** dare più spazio alle analisi che mi interessano.

---

# EPIC H — Centro Attività e notifiche

## US-070 — Vedere tutto ciò che richiede attenzione
**Come** utente  
**voglio** un Centro Attività  
**così da** non perdere operazioni PSD2 o altri elementi che richiedono una decisione.

## US-071 — Contatore attività
**Come** utente  
**voglio** vedere che esistono attività non gestite  
**così da** sapere che devo intervenire.

## US-072 — Gestire una notifica
**Come** utente  
**voglio** poter aprire, completare o ignorare una notifica  
**così da** mantenere il Centro Attività pulito.

---

# EPIC I — Configurazione

## US-080 — Gestire integrazioni
**Come** utente  
**voglio** trovare import CSV, collegamenti bancari e integrazioni in una sezione coerente  
**così da** non avere funzioni tecniche sparse nell'app.

## US-081 — Gestire preferenze notifiche
**Come** utente  
**voglio** scegliere quali notifiche ricevere  
**così da** evitare rumore inutile.

---

# EPIC J — Amministrazione Pecunia

## US-090 — Dashboard utilizzo applicazione
**Come** amministratore globale  
**voglio** vedere metriche di utilizzo  
**così da** capire come viene utilizzata Pecunia.

Le metriche devono essere distinte dalle analisi finanziarie personali degli utenti.

## US-091 — Dashboard performance
**Come** amministratore globale  
**voglio** vedere stato, errori, latenze e consumo risorse  
**così da** individuare problemi dell'applicazione.

## US-092 — Amministrare tag di gruppo
**Come** amministratore autorizzato  
**voglio** modificare o eliminare tag globali del gruppo  
**così da** mantenere coerente la classificazione condivisa.

---

# EPIC K — Backup e ripristino

## US-100 — Backup senza coinvolgere la PWA
**Come** amministratore dell'infrastruttura  
**voglio** che il backup sia gestito dal backend/infrastruttura  
**così da** non affidare la protezione dei dati al dispositivo dell'utente.

## US-101 — Conservare la chiave di cifratura
**Come** amministratore  
**voglio** visualizzare la chiave di cifratura durante la creazione  
**così da** poterla conservare per un futuro ripristino.

**Acceptance criteria**
- La chiave è mostrata nel momento previsto.
- L'app non la rende nuovamente leggibile successivamente.
- La procedura di restore richiede la chiave.

## US-102 — Ripristinare un backup
**Come** amministratore  
**voglio** ripristinare un backup cifrato  
**così da** recuperare l'applicazione dopo un fault.

---

# EPIC L — PWA e UX

## US-110 — Installare Pecunia come app
**Come** utente smartphone  
**voglio** installare Pecunia come PWA  
**così da** usarla come un'app senza sviluppare un'app nativa iOS/Android separata.

## US-111 — Usare Pecunia da desktop
**Come** utente  
**voglio** utilizzare la stessa applicazione da browser desktop  
**così da** poter fare analisi e configurazioni comodamente anche su uno schermo grande.

## US-112 — Inserimento rapido da mobile
**Come** utente smartphone  
**voglio** avere un'azione di inserimento sempre facilmente raggiungibile  
**così da** registrare una spesa immediatamente dopo averla sostenuta.

---

# EPIC M — Qualità e affidabilità

## US-120 — Nessun doppio addebito logico
**Come** utente  
**voglio** che una sincronizzazione ripetuta non crei duplicati  
**così da** poter fidarmi delle dashboard.

## US-121 — Continuare a usare l'app senza PSD2
**Come** utente  
**voglio** poter usare inserimento manuale e storico anche se il provider PSD2 non è temporaneamente disponibile  
**così da** non perdere la funzionalità principale.

## US-122 — Errori comprensibili
**Come** utente  
**voglio** messaggi di errore chiari  
**così da** capire cosa devo fare senza conoscere i dettagli tecnici.

---

# Matrice sintetica di copertura

| Area | User stories principali | Requisiti funzionali |
|---|---|---|
| Login/onboarding | US-001..003 | FR-001..006 |
| Spese | US-010..015 | FR-010..024 |
| Classificazione/tag | US-020..023 | FR-030..042, FR-060..062 |
| PSD2 | US-030..036 | FR-080..089 |
| CSV | US-040..041 | FR-090..094 |
| Gruppi | US-050..053 | FR-070..075 |
| Dashboard | US-060..067 | FR-130..139 |
| Attività | US-070..072 | FR-110..124 |
| Configurazione | US-080..081 | FR-170..173 |
| Admin | US-090..092 | FR-160..162 |
| Backup | US-100..102 | FR-150..153 |
| PWA | US-110..112 | FR-170..173 |
| Affidabilità | US-120..122 | FR-180..183 |

# Note per lo sviluppo

Le User Story non autorizzano automaticamente implementazioni non presenti nei requisiti. In caso di conflitto, prevalgono le business rules e i requisiti funzionali.

Le story PSD2 devono essere utilizzate come casi di test obbligatori, soprattutto per:

1. movimento PSD2 di 5 € → spesa reale di 15 €;
2. split 5 € carta + 10 € buono pasto;
3. prelievo ignorato per evitare doppia contabilizzazione;
4. più conti collegati con origine sempre visibile;
5. conto cointestato associato a un gruppo e isolato dal personale.
