# Pecunia — Visione prodotto

**Versione:** 1.0  
**Stato:** Draft funzionale consolidato  
**Prodotto:** Pecunia

## 1. Visione

Pecunia è una PWA self-hosted per il tracciamento delle spese personali e condivise. Deve permettere all'utente di registrare rapidamente ciò che spende, riducendo al minimo il lavoro manuale grazie a suggerimenti automatici, import storico e integrazione PSD2.

Il valore principale non è la contabilità patrimoniale completa, ma la capacità di rispondere in modo affidabile a domande come:

- Dove finiscono i miei soldi?
- Quanto spendo per una determinata categoria?
- Quali spese si ripetono?
- Quali aree di spesa stanno aumentando?
- Dove posso realisticamente ridurre i consumi?
- Quanto spendo personalmente rispetto alle spese di un gruppo condiviso?

## 2. Perimetro V1

La V1 comprende il **solo tracciamento e analisi delle spese**.

Sono inclusi:

- inserimento manuale rapido;
- classificazione assistita;
- categorie standard;
- sottocategorie;
- negozi/esercenti;
- modalità di pagamento;
- ripartizione di una spesa su più modalità di pagamento;
- spese straordinarie tramite flag;
- tag personali/globali nei gruppi;
- gruppi condivisi;
- conti bancari personali e condivisi collegati tramite PSD2;
- operazioni PSD2 sospese da confermare manualmente;
- import CSV storico;
- dashboard e analisi;
- ricerca e filtri;
- rilevazione delle ricorrenze;
- centro attività;
- notifiche configurabili;
- multi-utente e ruoli;
- Google Login;
- backup e ripristino del database a livello backend.

## 3. Fuori perimetro V1

Non devono essere implementati salvo esplicita decisione successiva:

- budget;
- generazione automatica di spese future;
- gestione completa dei saldi dei wallet/portafogli;
- gestione patrimoniale/investimenti;
- allegati alle spese;
- autenticazione locale con password;
- Identity Provider self-hosted;
- categorie personalizzabili dall'utente;
- contabilità a partita doppia;
- funzionalità non necessarie al tracciamento delle spese.

## 4. Principi UX

### 4.1 Minimo attrito

L'inserimento quotidiano deve essere veloce. Il percorso principale deve richiedere pochi secondi e non obbligare l'utente a compilare informazioni non indispensabili.

### 4.2 Automazione assistita

Pecunia deve proporre valori per categoria, sottocategoria, negozio, metodo di pagamento e gruppo utilizzando storico, causali e regole leggere.

Le informazioni finanziarie sostanziali non devono essere inventate. Quando un'operazione PSD2 viene rilevata, deve restare sospesa finché l'utente non decide cosa farne.

### 4.3 Dati affidabili

Una spesa deve rappresentare una spesa realmente sostenuta. Prelievi, movimenti bancari informativi e suggerimenti non devono diventare automaticamente spese contabilizzate.

### 4.4 Analisi prima della complessità

Pecunia non deve trasformarsi nella V1 in un gestionale finanziario completo. Le funzionalità devono essere proporzionate all'obiettivo principale.

## 5. Modello concettuale

Pecunia distingue esplicitamente:

- **Spesa:** ciò che l'utente considera economicamente sostenuto e vuole analizzare.
- **Movimento finanziario:** operazione realmente rilevata da una fonte, ad esempio PSD2.
- **Metodo di pagamento:** come è stata finanziata la spesa, anche con più modalità.
- **Origine:** da quale fonte deriva l'informazione.
- **Gruppo:** contesto condiviso a cui appartiene la spesa.
- **Categoria:** classificazione standard di ciò che è stato acquistato.
- **Tag:** informazione trasversale e flessibile sul contesto della spesa.
- **Straordinaria:** flag che permette di escludere le spese eccezionali dalle analisi della vita quotidiana.

## 6. Scenario PSD2 di riferimento

Una banca può rilevare:

> Coop — 5 € — Conto Fineco

L'utente apre l'operazione dal Centro Attività e scopre che la spesa reale era 15 €:

- Buono pasto: 10 €
- Carta: 5 €

Pecunia deve quindi poter registrare una spesa totale di 15 €, mantenendo il collegamento con il movimento PSD2 originale di 5 € e rendendo evidente l'origine `Conto Fineco`.

## 7. Multi-utente

Ogni utente possiede uno spazio personale. Gli utenti possono partecipare a gruppi condivisi.

Un conto bancario cointestato può essere collegato direttamente a un gruppo; le operazioni importate da quel conto appartengono al contesto del gruppo e non devono finire automaticamente nelle spese personali di un singolo membro.

Per i figli deve essere possibile usare il ruolo di **Supervisionato**, consentendo ai genitori/amministratori di vedere lo stato delle loro spese.

## 8. Self-hosting

Il backend è destinato a un NAS domestico con risorse inferiori a quelle di un notebook commerciale. Il progetto deve quindi privilegiare:

- CPU e RAM contenute;
- servizi leggeri;
- algoritmi deterministici quando sufficienti;
- assenza di modelli AI locali pesanti nella V1;
- containerizzazione;
- semplicità di manutenzione.

## 9. Visione evolutiva

La V1 deve costruire una base dati affidabile e un'architettura estendibile. Budget, allegati, funzionalità finanziarie più avanzate e ulteriori provider di autenticazione potranno essere aggiunti successivamente senza compromettere il modello fondamentale.
