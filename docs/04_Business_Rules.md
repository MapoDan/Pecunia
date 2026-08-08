# Pecunia — Business Rules

**Versione:** 1.0  
**Scope:** V1  
**Stato:** base normativa per sviluppo e test

Questo documento contiene le regole di dominio che determinano come Pecunia deve interpretare, registrare, modificare e aggregare i dati finanziari. In caso di dubbio sull'implementazione, le regole di questo documento prevalgono su comportamenti impliciti del frontend o del provider bancario.

---

# 1. Principio fondamentale: movimento ≠ spesa

## BR-001
Un movimento bancario PSD2 **non è automaticamente una spesa Pecunia**.

Un movimento PSD2 è una fonte di informazione che può generare una spesa solo dopo una decisione esplicita dell'utente.

## BR-002
Una spesa Pecunia rappresenta una spesa effettivamente sostenuta dall'utente o dal contesto condiviso a cui appartiene.

## BR-003
Una spesa può essere creata esclusivamente tramite:
- inserimento manuale;
- contabilizzazione esplicita di un'operazione PSD2;
- import storico autorizzato dall'utente.

Le sincronizzazioni automatiche non possono creare autonomamente una spesa contabilizzata.

---

# 2. Stati di un'operazione PSD2

Un'operazione PSD2 deve poter assumere almeno gli stati:

1. `PENDING` — rilevata ma non ancora valutata;
2. `ACCEPTED` — contabilizzata come spesa;
3. `IGNORED` — esplicitamente ignorata;
4. `ERROR` — acquisizione/elaborazione fallita e da gestire.

## BR-010
Solo `ACCEPTED` genera o completa una spesa contabilizzata.

## BR-011
Un'operazione `IGNORED` non deve comparire come spesa nelle dashboard.

## BR-012
Un'operazione `PENDING` deve essere visibile nel Centro Attività e non deve incidere sulle statistiche di spesa contabilizzata.

---

# 3. Origine PSD2

## BR-020
Ogni operazione PSD2 deve conservare il riferimento al collegamento/conto da cui è stata acquisita.

## BR-021
Se l'utente possiede più conti collegati, l'origine deve essere distinguibile almeno tramite un nome leggibile e un identificativo tecnico interno.

Esempio UI:
> Identificata da conto Fineco

## BR-022
Il riferimento all'origine PSD2 non deve essere perso quando l'operazione viene contabilizzata.

---

# 4. Data di inizio sincronizzazione

## BR-030
Per ogni collegamento Open Banking, la data di collegamento costituisce il punto di partenza della sincronizzazione automatica V1.

## BR-031
Pecunia non deve scaricare automaticamente anni di storico precedenti alla data di collegamento.

## BR-032
CSV e inserimenti manuali non sono soggetti a questa limitazione e possono contenere date precedenti.

---

# 5. Importo della spesa

## BR-040
Una spesa ha un `total_amount` che rappresenta il valore complessivo della spesa contabilizzata.

## BR-041
L'importo inizialmente rilevato da PSD2 può essere diverso dal `total_amount` definitivo della spesa.

### Esempio obbligatorio
Movimento PSD2:
- Coop: 5 €

Spesa reale:
- Totale: 15 €
- Carta: 5 €
- Buono pasto: 10 €

La spesa contabilizzata deve avere:
- `total_amount = 15 €`;
- riferimento al movimento PSD2 originale di 5 €;
- split carta 5 €;
- split buono pasto 10 €.

## BR-042
La modifica dell'importo non deve alterare il valore storico del movimento PSD2 originario.

Il sistema deve mantenere distinti:
- importo originario rilevato;
- importo della spesa contabilizzata.

---

# 6. Split dei metodi di pagamento

## BR-050
Una spesa può essere pagata tramite uno o più metodi.

## BR-051
Il totale degli split deve essere uguale al totale della spesa contabilizzata.

Formula:

`sum(payment_splits) = expense.total_amount`

## BR-052
Esempio:

Spesa 50 €:
- Buono pasto 20 €;
- Carta 30 €.

Totale = 50 €.

## BR-053
Il sistema deve distinguere il **tipo di metodo** dalla singola carta/conto fisico quando questa distinzione non è utile alle analisi.

Metodi V1 tipici:
- carta;
- contanti;
- bonifico;
- Satispay;
- buono pasto;
- Splitwise;
- altri metodi configurabili.

## BR-054
L'origine bancaria PSD2 è un attributo distinto dal metodo di pagamento.

Esempio:
- Pagato con: Carta 5 €;
- Identificata da: conto Fineco.

---

# 7. Quota personale

## BR-060
Una spesa può avere un importo originario superiore alla quota effettivamente sostenuta dall'utente.

## BR-061
Il valore utilizzato nelle dashboard personali deve essere la quota personale contabilizzata, non necessariamente l'importo lordo della transazione.

### Esempio
Transazione: 10 €  
Quota personale: 5 €  
Quota altra persona: 5 €

La dashboard personale deve contabilizzare 5 €.

## BR-062
L'importo lordo deve rimanere disponibile per tracciabilità e analisi appropriate.

## BR-063
La quota personale deve essere coerente con la struttura della spesa e non può generare valori negativi o superiori al totale pertinente.

---

# 8. Commissioni bancarie

## BR-070
Una commissione bancaria è distinta dall'importo principale del movimento/spesa.

## BR-071
La commissione può essere associata alla relativa operazione bancaria quando tecnicamente possibile.

## BR-072
La commissione effettivamente sostenuta deve poter essere inclusa nelle analisi economiche secondo una regola di visualizzazione configurabile/definita dall'implementazione finale, senza alterare retroattivamente l'importo originale del movimento.

---

# 9. Prelievi

## BR-080
Un prelievo di contante non è automaticamente una spesa.

## BR-081
Un prelievo PSD2 deve arrivare nello stato `PENDING` come ogni altra operazione rilevata.

## BR-082
L'utente può:
- ignorarlo, se registrerà successivamente le singole spese in contanti;
- contabilizzarlo, se il prelievo stesso deve rappresentare una voce di spesa secondo il suo utilizzo.

## BR-083
Pecunia non deve presumere che il prelievo sia stato speso immediatamente.

---

# 10. Spese straordinarie

## BR-090
Una spesa può essere marcata come `extraordinary`/straordinaria.

## BR-091
Una spesa straordinaria rimane nello storico e non viene cancellata dalle statistiche globali.

## BR-092
Le dashboard devono poter includere o escludere le spese straordinarie nelle analisi appropriate.

## BR-093
L'esclusione dalle dashboard non modifica la spesa registrata.

---

# 11. Categorie e sottocategorie

## BR-100
Ogni spesa deve avere una categoria coerente con le regole minime della V1.

## BR-101
La sottocategoria è valorizzabile quando pertinente.

## BR-102
Categorie e sottocategorie possono essere suggerite automaticamente.

## BR-103
Un suggerimento automatico non equivale a una decisione irrevocabile: l'utente può correggerlo.

## BR-104
Il sistema deve privilegiare regole leggere e dati storici rispetto a elaborazioni computazionalmente pesanti.

---

# 12. Suggerimenti automatici

## BR-110
I suggerimenti possono derivare da:
- esercente/negozio;
- descrizione/casuale;
- metodo di pagamento;
- storico dell'utente;
- contesto del gruppo;
- dati PSD2 disponibili.

## BR-111
I suggerimenti devono essere spiegabili almeno a livello funzionale quando utile.

## BR-112
L'utente deve poter correggere un suggerimento senza dover modificare configurazioni tecniche.

## BR-113
Le regole di suggerimento non devono essere implementate tramite un modello AI pesante nella V1.

---

# 13. Ricorrenze

## BR-120
Pecunia può rilevare pattern di spesa ricorrenti per analisi e suggerimenti.

## BR-121
La rilevazione di una ricorrenza **non crea automaticamente una nuova spesa futura**.

## BR-122
Una spesa futura esiste solo quando effettivamente sostenuta e registrata manualmente o tramite successiva contabilizzazione PSD2.

---

# 14. Centro Attività

## BR-130
Il Centro Attività raccoglie elementi che richiedono un'azione dell'utente.

## BR-131
Le operazioni PSD2 `PENDING` devono essere presenti nel Centro Attività.

## BR-132
L'utente deve poter gestire un'operazione sospesa con un percorso diretto, preferibilmente tramite tap sulla voce.

## BR-133
Una notifica aggregata può rappresentare più operazioni.

Esempio:
> Individuate 5 operazioni che necessitano aggiornamenti.

## BR-134
Quando l'utente decide di ignorare una notifica di aggiornamento storico, quella specifica notifica non deve essere riproposta automaticamente.

---

# 15. Aggiornamenti dello storico

## BR-140
Lo storico non deve essere modificato automaticamente in seguito a una nuova informazione, salvo quando l'utente ha esplicitamente autorizzato l'aggiornamento.

## BR-141
Pecunia può rilevare che un'operazione storica potrebbe richiedere aggiornamento e notificare l'utente.

## BR-142
L'utente decide se applicare o meno l'aggiornamento.

## BR-143
Se accetta, l'aggiornamento può essere applicato automaticamente secondo le regole validate dal sistema.

---

# 16. Duplicati

## BR-150
Lo stesso movimento PSD2 non può generare più volte la stessa spesa a causa di sincronizzazioni ripetute.

## BR-151
L'import CSV deve effettuare un controllo di duplicazione almeno a livello di potenziale duplicato.

## BR-152
Un potenziale duplicato non deve essere eliminato silenziosamente senza una regola esplicita o una decisione dell'utente quando l'ambiguità è elevata.

---

# 17. Gruppi

## BR-160
Un gruppo è un contesto separato per la gestione delle spese condivise.

## BR-161
Un utente può appartenere a uno o più gruppi secondo i permessi definiti.

## BR-162
Le spese personali rimangono personali salvo esplicita condivisione.

## BR-163
Un conto cointestato può essere associato a uno specifico gruppo.

## BR-164
Le operazioni provenienti dal conto condiviso devono essere gestite nel contesto del gruppo associato e non devono essere automaticamente replicate nei bilanci personali dei membri.

## BR-165
La visibilità delle spese dei figli è subordinata a un rapporto/permesso di supervisione esplicito.

---

# 18. Tag

## BR-170
I tag usati nel contesto personale possono diventare disponibili come tag globali nel gruppo secondo la logica definita dall'applicazione.

## BR-171
I tag globali del gruppo possono essere amministrati dall'amministratore autorizzato.

## BR-172
L'amministratore può:
- mantenere;
- modificare;
- eliminare.

## BR-173
La cancellazione di un tag non deve cancellare la spesa a cui il tag era associato.

---

# 19. Dashboard e aggregazioni

## BR-180
Le dashboard devono poter filtrare almeno per:
- periodo;
- categoria;
- sottocategoria;
- negozio;
- metodo di pagamento;
- tag;
- gruppo/contesto;
- straordinaria sì/no.

## BR-181
Le aggregazioni personali devono usare la quota personale quando una spesa è condivisa.

## BR-182
Gli importi lordi possono essere mostrati separatamente quando servono per comprendere la transazione.

## BR-183
Il confronto tra periodi deve usare criteri coerenti e non deve mischiare automaticamente contesti personali e condivisi.

---

# 20. Valute

## BR-190
Quando una spesa è registrata in una valuta diversa dalla valuta di riferimento dell'utente/gruppo, la conversione deve utilizzare il cambio del giorno della spesa.

## BR-191
Il valore convertito deve essere deterministico: riaprire l'app in un giorno successivo non deve cambiare retroattivamente l'importo convertito usando un nuovo cambio.

## BR-192
Il tasso utilizzato deve essere conservato con il dato convertito per consentire tracciabilità.

---

# 21. Import CSV

## BR-200
L'import CSV è un'operazione esplicita dell'utente.

## BR-201
Le date importate possono essere precedenti alla data di creazione dell'account.

## BR-202
L'import deve validare almeno:
- data;
- importo;
- formato numerico;
- eventuali campi richiesti dalla mappatura.

## BR-203
Le righe non valide devono essere segnalate senza invalidare necessariamente l'intero file.

---

# 22. Autorizzazioni

## BR-210
Il frontend non è una fonte di autorità per i permessi.

## BR-211
Ogni operazione sensibile deve essere autorizzata lato backend.

## BR-212
L'amministratore globale può accedere alle funzionalità amministrative previste, ma ciò non implica automaticamente accesso indiscriminato ai dati finanziari personali degli utenti, salvo esplicita regola di dominio.

## BR-213
I membri di un gruppo possono accedere solo ai dati condivisi secondo il ruolo assegnato.

---

# 23. Cifratura e ripristino

## BR-220
Il database deve essere protetto tramite cifratura secondo la strategia tecnica definita dall'architettura.

## BR-221
La PWA non esegue backup del database.

## BR-222
La chiave di cifratura necessaria al restore viene resa disponibile all'amministratore durante la creazione/configurazione iniziale.

## BR-223
Pecunia non deve presentare successivamente la chiave come dato recuperabile dall'interfaccia normale.

---

# 24. Regole di coerenza contabile

## BR-230
Una spesa non può avere un totale negativo.

## BR-231
Uno split di pagamento non può essere negativo.

## BR-232
La somma degli split deve coincidere con il totale della spesa quando la spesa è marcata come completamente contabilizzata.

## BR-233
La quota personale non può superare il totale della spesa.

## BR-234
Una spesa contabilizzata deve avere una data valida.

## BR-235
Una spesa contabilizzata deve avere una fonte identificabile: manuale, PSD2 o import.

---

# 25. Priorità delle fonti

Quando Pecunia dispone di più informazioni sulla stessa spesa, deve applicare una gerarchia logica:

1. decisione esplicita dell'utente;
2. dati già contabilizzati e confermati;
3. dati PSD2 originari;
4. suggerimenti derivati dallo storico/causale;
5. valori predefiniti.

Un suggerimento non deve sovrascrivere una decisione esplicita dell'utente.

---

# 26. Regola generale di conservazione della storia

## BR-240
Pecunia deve privilegiare la conservazione della storia rispetto alla semplificazione distruttiva dei dati.

Quando un dato viene corretto, il sistema deve mantenere le informazioni necessarie a ricostruire l'origine quando questo è importante per:
- PSD2;
- import;
- split;
- commissioni;
- operazioni condivise.

## BR-241
La modifica di una spesa non deve cancellare silenziosamente il riferimento alla fonte che l'ha originata.

---

# 27. Principi da applicare durante lo sviluppo

Codex deve rispettare questi principi:

- **non contabilizzare ciò che l'utente non ha effettivamente sostenuto**;
- **non confondere movimento bancario e spesa**;
- **non creare automaticamente spese future**;
- **non duplicare spese per effetto di sincronizzazioni**;
- **non perdere l'origine PSD2**;
- **non confondere importo lordo e quota personale**;
- **non confondere metodo di pagamento e conto bancario di origine**;
- **non usare l'esclusione dalle dashboard per cancellare dati**;
- **non affidare le regole contabili al solo frontend**.

Queste regole costituiscono la base per i test di dominio e devono essere trattate come invarianti del sistema.