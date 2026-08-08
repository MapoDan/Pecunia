# Pecunia — Frontend & UX Specification

**Versione:** 1.0  
**Scope:** V1  
**Nome applicazione:** Pecunia

## 1. Obiettivo UX

Pecunia deve permettere di registrare una spesa in pochi secondi e, contemporaneamente, offrire strumenti avanzati per capire come vengono spesi i soldi.

Principi prioritari:

1. velocità di inserimento;
2. minimo numero di campi obbligatori;
3. suggerimenti automatici;
4. chiarezza del dato finanziario;
5. dashboard leggibili;
6. mobile-first;
7. responsive desktop;
8. accessibilità;
9. nessuna funzione complessa deve essere obbligatoria per utilizzare l'app.

Il design deve essere moderno e comparabile, come qualità d'esperienza, alle migliori applicazioni finanziarie consumer contemporanee, senza copiare un prodotto specifico.

---

# 2. Struttura generale

La PWA deve utilizzare una struttura di navigazione semplice.

Navigazione primaria consigliata:

- **Home / Dashboard**
- **Spese**
- **Attività**
- **Gruppi**
- **Configurazione**

Su mobile, l'azione primaria "Nuova spesa" deve essere sempre facilmente raggiungibile tramite **Speed Dial / Floating Action Button**.

Il menu secondario può contenere:

- profilo;
- metodi di pagamento;
- categorie;
- tag;
- collegamenti bancari;
- import CSV;
- impostazioni;
- sicurezza/passkey;
- logout.

---

# 3. Dashboard Home

La Home è il punto di ingresso principale dopo il login.

Deve essere configurabile dall'utente.

Widget iniziali:

- spesa totale nel periodo;
- spesa personale;
- andamento temporale;
- distribuzione per categoria;
- distribuzione per metodo di pagamento;
- top merchant;
- confronto con periodo precedente;
- spese straordinarie;
- tag principali;
- eventuali insight statistici leggeri.

L'utente deve poter:

- mostrare/nascondere widget;
- riordinare i widget;
- scegliere il periodo predefinito;
- applicare filtri.

Il layout viene salvato dal backend.

---

# 4. Dashboard: principio delle spese straordinarie

Le spese marcate come `straordinarie` non devono sparire dai dati.

Devono essere facilmente distinguibili e filtrabili.

Esempio:

```text
Spese agosto
€ 4.850

Spese ordinarie
€ 1.850

Spese straordinarie
€ 3.000
```

L'utente deve poter confrontare:

- totale reale;
- totale ordinario;
- totale straordinario.

Questo è un requisito centrale di Pecunia.

---

# 5. Speed Dial — Nuova spesa

Il pulsante principale deve consentire di iniziare immediatamente una nuova spesa.

La prima schermata deve essere estremamente rapida.

Campi prioritari:

1. **Importo**;
2. **Categoria**;
3. **Metodo di pagamento**;
4. data, precompilata con oggi;
5. merchant, se riconosciuto.

Campi secondari:

- sottocategoria;
- split pagamento;
- quota personale;
- tag;
- straordinaria;
- note.

L'ordine deve favorire l'inserimento rapido.

---

# 6. Inserimento rapido

Scenario ideale:

```text
+ Nuova spesa
       ↓
10,00 €
       ↓
Coop
       ↓
Categoria suggerita: Alimentari
       ↓
Carta 8 € + Buono pasto 2 €
       ↓
Salva
```

L'utente non deve essere costretto a compilare manualmente tutti i campi.

Se il merchant è già conosciuto, il sistema deve proporre automaticamente:

- categoria;
- sottocategoria;
- eventuale tag;
- metodo di pagamento usato frequentemente.

---

# 7. Smart Suggestions

I suggerimenti devono essere leggeri e deterministici dove possibile.

Priorità:

1. storico dello stesso merchant;
2. merchant normalizzato;
3. descrizione/causale PSD2;
4. combinazione merchant + metodo;
5. frequenza personale;
6. categoria globale;
7. eventuale motore statistico leggero.

Non è necessario introdurre un modello AI pesante nella V1.

Il sistema deve poter suggerire, ad esempio:

```text
COOP
→ Alimentari
→ Spesa
→ Carta
```

L'utente deve poter correggere il suggerimento.

La correzione può diventare un dato utile per migliorare i suggerimenti futuri.

---

# 8. Form spesa completo

La schermata completa deve consentire di modificare:

### Informazioni principali

- importo totale;
- valuta;
- data;
- categoria;
- sottocategoria;
- merchant;
- descrizione.

### Pagamento

- uno o più metodi;
- importo per metodo.

Esempio:

```text
Totale: €50

Pagato con:
Buono pasto    €20
Carta          €30
```

La somma deve essere visivamente verificata.

### Condivisione

```text
Totale €10

La tua quota €5
Altra persona €5
```

### Classificazione

- tag;
- straordinaria.

---

# 9. Regola UX fondamentale: dati obbligatori

L'app deve evitare form lunghi.

Il minimo necessario per salvare una spesa manuale è:

- importo;
- categoria;
- almeno un metodo di pagamento;
- data.

Il metodo di pagamento deve coprire il totale.

Merchant, sottocategoria, tag e descrizione devono essere opzionali e suggeriti automaticamente quando possibile.

---

# 10. Spese

La sezione Spese deve offrire:

- lista cronologica;
- ricerca;
- filtri;
- ordinamento;
- raggruppamento opzionale;
- accesso rapido al dettaglio.

Ogni riga dovrebbe mostrare almeno:

```text
Coop
Alimentari · oggi
€ 15,00
Carta + Buono pasto
```

Per una spesa PSD2:

```text
Coop
Alimentari · oggi
€ 15,00
Carta + Buono pasto
Identificata da Conto Fineco
```

La provenienza PSD2 deve essere immediatamente riconoscibile senza occupare troppo spazio.

---

# 11. Ricerca

La ricerca deve essere globale sulle spese accessibili all'utente.

Esempi:

- `coop`;
- `amazon`;
- `ristorante`;
- testo della descrizione.

La ricerca deve essere server-side quando il dataset supera la soglia definita dal frontend.

---

# 12. Filtri

Filtri disponibili:

- periodo;
- categoria;
- sottocategoria;
- merchant;
- metodo pagamento;
- tag;
- gruppo;
- straordinaria sì/no;
- fonte manuale/PSD2/CSV;
- intervallo importo.

Su mobile i filtri devono aprirsi in una schermata/bottom sheet dedicata.

---

# 13. Dettaglio spesa

Il dettaglio deve mostrare in modo gerarchico:

1. totale;
2. data;
3. categoria;
4. merchant;
5. pagamento;
6. quota personale;
7. condivisione;
8. tag;
9. origine;
10. note.

Se PSD2:

```text
Origine
Conto Fineco
Importo identificato: €5,00
Importo contabilizzato: €15,00
```

Questo rende evidente la differenza tra dato bancario e dato contabile.

---

# 14. Centro Attività

Il Centro Attività è una parte fondamentale dell'applicazione.

Deve raccogliere principalmente ciò che richiede attenzione.

Esempio:

```text
⚠ 12 operazioni necessitano di aggiornamento

3 nuove operazioni da verificare
2 import completati
1 collegamento bancario richiede attenzione
```

La priorità è mostrare ciò che richiede una decisione dell'utente.

---

# 15. PSD2 — lista sospese

Quando vengono trovate nuove operazioni:

```text
Centro Attività
      ↓
12 operazioni da verificare
      ↓
Lista PSD2
```

Ogni elemento deve mostrare almeno:

- merchant/causale;
- data;
- importo bancario;
- conto di provenienza;
- tipo operazione;
- stato.

Esempio:

```text
Coop
08/08/2026
€5,00
Identificata da Conto Fineco
```

---

# 16. PSD2 — decisione con un tap

Toccando una transazione PSD2 l'utente deve entrare direttamente nella schermata decisionale.

Azioni principali:

### Registra spesa

Apre una form già precompilata.

### Ignora

Non crea alcuna spesa.

Il movimento rimane nello storico PSD2.

Non deve essere richiesto di attraversare menu intermedi inutili.

---

# 17. PSD2 — contabilizzazione modificabile

Caso:

```text
Banca identifica:
Coop €5
```

L'utente modifica:

```text
Totale spesa €15

Pagato con:
Carta €5
Buono pasto €10
```

Il frontend deve rendere questa modifica naturale e immediata.

La schermata deve evidenziare che:

```text
Importo bancario: €5
Totale spesa: €15
```

Il dato bancario originale non deve essere sovrascritto.

---

# 18. PSD2 — prelievo

Esempio:

```text
Prelievo ATM
€100
Conto Fineco
```

L'utente può:

- registrarlo come spesa, se appropriato;
- ignorarlo.

L'app non deve presumere automaticamente che un prelievo sia una spesa.

---

# 19. Onboarding

Primo accesso:

```text
Google Login
   ↓
Benvenuto in Pecunia
   ↓
Valuta predefinita
   ↓
Categorie preconfigurate
   ↓
Metodi di pagamento preconfigurati
   ↓
Dashboard iniziale
```

Il collegamento Open Banking deve essere opzionale.

L'utente deve poter utilizzare Pecunia immediatamente anche senza collegare una banca.

---

# 20. Collegamento banca

La sezione configurazione deve mostrare:

```text
Conti collegati

Fineco
Conto personale
Ultima sincronizzazione: oggi

[Gestisci]
```

Per ogni connessione:

- banca;
- nome personalizzato;
- stato;
- data collegamento;
- ultima sincronizzazione;
- eventuale gruppo associato.

---

# 21. Configurazione / Account

La configurazione deve essere organizzata per sezioni.

### Account

- profilo;
- sicurezza;
- passkey;
- logout.

### Dati

- import CSV;
- gestione categorie;
- gestione merchant;
- gestione tag.

### Pagamenti

- metodi di pagamento.

### Open Banking

- conti collegati;
- sincronizzazione;
- gestione consenso.

### Preferenze

- valuta;
- lingua;
- timezone;
- dashboard.

L'import CSV **non** deve essere esposto nello Speed Dial.

---

# 22. Gruppi

La sezione Gruppi deve mostrare i contesti disponibili.

Esempio:

```text
I miei dati

Casa
4 membri

Famiglia
3 membri
```

Il cambio di contesto deve essere evidente per evitare di registrare una spesa nel gruppo sbagliato.

---

# 23. Gruppo con conto cointestato

Nel gruppo Casa:

```text
Conto condiviso
Conto Casa
Fineco
```

Le operazioni provenienti da questo conto devono essere riconoscibili come appartenenti al gruppo.

Non devono comparire automaticamente nel personale di ciascun membro come duplicati.

---

# 24. Genitori e figli

La UI deve supportare ruoli con visibilità differenziata.

Un genitore autorizzato può vedere lo stato delle spese del figlio secondo i permessi del gruppo.

Il figlio non deve automaticamente vedere dati finanziari degli altri membri.

---

# 25. Tag

I tag devono essere semplici da applicare.

Esempio:

```text
#vacanza
#lavoro
#casa
#regalo
```

Un tag personale può essere reso globale nel gruppo.

L'amministratore del gruppo deve poter:

- mantenere;
- rinominare;
- eliminare;

un tag globale secondo le Business Rules.

---

# 26. Dashboard avanzata

La dashboard deve permettere di rispondere a domande pratiche:

- Dove spendo di più?
- Quali categorie stanno aumentando?
- Quanto spendo mediamente?
- Quali merchant ricorrono maggiormente?
- Quanto spendo in contanti?
- Quanto tramite carta?
- Quanto tramite buoni pasto?
- Quanto delle mie spese è straordinario?
- Come cambia la spesa rispetto al mese precedente?
- Ci sono comportamenti ripetitivi?

---

# 27. Visualizzazioni

V1 deve prevedere almeno:

### KPI cards

- totale;
- media;
- numero spese;
- quota straordinaria.

### Line chart

Andamento temporale.

### Bar chart

Confronto categorie/periodi.

### Donut/pie

Distribuzione categorie o metodi di pagamento quando leggibile.

### Tabelle

Top merchant e dettaglio categorie.

Non utilizzare grafici solo perché disponibili: ogni visualizzazione deve rispondere a una domanda utile.

---

# 28. Confronto periodi

La dashboard deve consentire confronti:

- mese vs mese precedente;
- mese vs stesso mese anno precedente;
- intervallo personalizzato vs intervallo precedente equivalente.

Esempio:

```text
Agosto 2026
€2.140

Agosto 2025
€1.870

+14,4%
```

La logica di confronto deve essere eseguita dal backend.

---

# 29. Responsive design

Breakpoint principali da definire nel design system, senza basarsi su un singolo dispositivo.

La UI deve essere ottimizzata prima per smartphone e poi adattata a tablet/desktop.

Su desktop può essere utilizzata una sidebar persistente.

Su mobile:

- bottom navigation o equivalente;
- bottom sheets;
- FAB/Speed Dial;
- form a step minimo;
- touch target adeguati.

---

# 30. Accessibilità

Target minimo:

- WCAG 2.2 AA dove tecnicamente applicabile;
- contrasto adeguato;
- focus visibile;
- navigazione tastiera desktop;
- label esplicite;
- aria semantics quando necessarie;
- non usare solo il colore per rappresentare stato o variazioni.

---

# 31. Loading states

Evitare schermate bianche.

Usare skeleton/loading state per:

- dashboard;
- liste;
- dettaglio;
- PSD2;
- import.

Per operazioni lunghe mostrare stato esplicito.

---

# 32. Offline e PWA

La V1 deve supportare almeno:

- installazione PWA;
- service worker;
- caching delle risorse statiche;
- app shell caricabile rapidamente.

Non implementare nella V1 un completo offline-first financial ledger con sincronizzazione conflittuale.

Le operazioni finanziarie richiedono connessione al backend per essere confermate.

Questo riduce drasticamente la complessità e il rischio di inconsistenze.

---

# 33. Performance UX

Obiettivo:

- avvio percepito rapido;
- bundle frontend contenuto;
- lazy loading delle sezioni non utilizzate;
- grafici caricati quando necessari;
- paginazione delle liste;
- nessun download dello storico completo per visualizzare una dashboard.

Il frontend deve essere compatibile con il deployment sul NAS senza richiedere elaborazione significativa lato server per ogni interazione.

---

# 34. Design system

Pecunia deve avere un design system centralizzato per:

- typography;
- spacing;
- cards;
- buttons;
- inputs;
- chips;
- badges;
- modals;
- bottom sheets;
- tables;
- charts;
- notifications;
- navigation.

Evitare stili duplicati per singola pagina.

---

# 35. Logo

Il logo dell'applicazione sarà **Pecunia**.

Riservare uno spazio nel progetto per l'asset ufficiale:

```text
public/branding/pecunia-logo.svg
public/branding/pecunia-icon.svg
```

Fino alla disponibilità dell'asset definitivo, utilizzare un placeholder coerente e facilmente sostituibile.

Non incorporare il logo direttamente nei componenti come SVG hardcoded.

---

# 36. Stati vuoti

Ogni sezione deve avere un empty state utile.

Esempio:

```text
Non hai ancora registrato spese.

Inizia registrando la tua prima spesa.

[+ Nuova spesa]
```

Per PSD2:

```text
Nessuna operazione da verificare.

Tutto aggiornato ✓
```

---

# 37. Error UX

Gli errori devono essere comprensibili.

Evitare:

```text
HTTP 422
```

Preferire:

```text
Non posso salvare la spesa:
la somma dei metodi di pagamento è €45,
ma il totale è €50.
```

Gli errori tecnici devono essere associati a un `request_id` per il supporto.

---

# 38. Conferme e operazioni distruttive

Per azioni irreversibili o potenzialmente distruttive:

- conferma esplicita;
- spiegazione dell'effetto;
- possibilità di annullare quando tecnicamente possibile.

Non chiedere conferme inutili per ogni salvataggio.

---

# 39. Principio di trasparenza finanziaria

Quando Pecunia modifica o arricchisce un dato derivato da una fonte esterna, deve essere chiaro cosa è:

- dato bancario originale;
- dato inserito dall'utente;
- dato suggerito dall'app;
- dato calcolato.

Questo principio è particolarmente importante per PSD2 e conversioni valutarie.

---

# 40. Regole per Codex

Codex deve:

1. implementare mobile-first;
2. mantenere il design system centralizzato;
3. non introdurre campi obbligatori non definiti nelle Business Rules;
4. usare suggerimenti per ridurre il lavoro dell'utente;
5. non implementare logica finanziaria esclusivamente nel frontend;
6. rispettare gli endpoint definiti in `07_API_Specification.md`;
7. mantenere il contesto personale/gruppo sempre evidente;
8. preservare la distinzione tra importo PSD2 e importo contabilizzato;
9. non aggiungere budget nella V1;
10. non implementare funzionalità V2 senza esplicita richiesta;
11. mantenere l'app leggera per l'esecuzione sul NAS;
12. utilizzare componenti riutilizzabili anziché duplicare pagine e form.

---

# 41. Priorità UX V1

In caso di conflitto tra funzionalità, la priorità è:

1. correttezza finanziaria;
2. velocità di inserimento;
3. chiarezza;
4. semplicità;
5. performance;
6. personalizzazione;
7. funzioni avanzate.

Una UI più bella non deve mai rendere più difficile registrare una spesa.
