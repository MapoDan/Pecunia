# Pecunia — Data Model

**Versione:** 1.0  
**Scope:** V1  
**Scopo:** definizione del modello dati persistente e delle relazioni di dominio

Questo documento definisce il modello dati di Pecunia. Il modello deve essere implementato nel database in modo coerente con le Business Rules e con l'architettura.

---

# 1. Principi del modello

1. Una **spesa** rappresenta un evento economico effettivamente sostenuto.
2. Un **movimento PSD2** rappresenta una rilevazione bancaria e non è automaticamente una spesa.
3. L'importo originale PSD2 e l'importo definitivo della spesa devono poter essere diversi.
4. Una spesa può avere più metodi di pagamento.
5. Una spesa può avere una quota personale inferiore al totale.
6. Le fonti devono essere tracciabili.
7. I dati personali e quelli di gruppo devono essere separabili logicamente.
8. Il modello deve essere relazionale e semplice da interrogare.
9. Le entità finanziarie non devono essere cancellate fisicamente quando questo compromette la tracciabilità.

---

# 2. Entità principali

Le entità V1 sono:

- `User`
- `UserSettings`
- `Group`
- `GroupMember`
- `BankConnection`
- `PaymentMethod`
- `Category`
- `Subcategory`
- `Merchant`
- `Tag`
- `Expense`
- `ExpensePayment`
- `ExpenseShare`
- `PSD2Transaction`
- `ImportBatch`
- `ImportRow`
- `Activity`
- `CurrencyRate`
- `AuditEvent`

---

# 3. User

## Scopo
Rappresenta l'identità applicativa dell'utente.

### Campi

| Campo | Tipo | Note |
|---|---|---|
| id | UUID | PK |
| google_subject | string | identificativo Google univoco |
| email | string | email autenticata |
| display_name | string | nome visualizzato |
| avatar_url | string/null | opzionale |
| role | enum | USER / ADMIN |
| status | enum | ACTIVE / DISABLED |
| created_at | timestamp | audit |
| updated_at | timestamp | audit |
| last_login_at | timestamp/null | opzionale |

### Regole

- `google_subject` deve essere unique.
- L'email non deve essere considerata l'identificatore tecnico primario.
- ADMIN è un ruolo applicativo globale.

---

# 4. UserSettings

Impostazioni personali dell'utente.

| Campo | Tipo |
|---|---|
| user_id | UUID PK/FK |
| default_currency | string(3) |
| locale | string |
| timezone | string |
| onboarding_completed | boolean |
| created_at | timestamp |
| updated_at | timestamp |

I valori di default devono essere preconfigurati per un nuovo utente.

---

# 5. Group

Rappresenta un contesto condiviso.

| Campo | Tipo | Note |
|---|---|---|
| id | UUID | PK |
| name | string | nome gruppo |
| description | string/null | opzionale |
| status | enum | ACTIVE / ARCHIVED |
| created_by | UUID FK User | creatore |
| created_at | timestamp | |
| updated_at | timestamp | |

Esempi:
- Casa
- Famiglia
- Figli
- Viaggio

---

# 6. GroupMember

Associazione utente-gruppo.

| Campo | Tipo |
|---|---|
| id | UUID PK |
| group_id | UUID FK |
| user_id | UUID FK |
| role | enum |
| status | enum |
| joined_at | timestamp |
| created_at | timestamp |

Ruoli iniziali consigliati:

- `OWNER`
- `ADMIN`
- `MEMBER`
- `CHILD`
- `VIEWER`

Il modello deve consentire permessi più granulari in futuro.

Vincolo: `(group_id, user_id)` unique.

---

# 7. BankConnection

Rappresenta un collegamento Open Banking/PSD2.

| Campo | Tipo | Note |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK | proprietario del collegamento |
| group_id | UUID FK/null | contesto condiviso, se presente |
| provider | string | provider PSD2 |
| provider_connection_id | string | ID presso provider |
| institution_name | string | es. Fineco |
| display_name | string | nome leggibile |
| status | enum | ACTIVE / EXPIRED / REVOKED / ERROR |
| connected_at | timestamp | fondamentale |
| sync_from | timestamp/date | normalmente derivata da connected_at |
| last_sync_at | timestamp/null | |
| created_at | timestamp | |
| updated_at | timestamp | |

### Regole

- `sync_from` non deve essere antecedente al collegamento automatico iniziale salvo esplicita funzionalità amministrativa futura.
- Se `group_id` è valorizzato, il collegamento è associato al gruppo.
- Un conto cointestato destinato alle spese comuni deve essere collegato al relativo gruppo.
- I secret OAuth/PSD2 non sono salvati in chiaro in questa entità.

---

# 8. PaymentMethod

Rappresenta il metodo con cui una spesa è stata pagata.

| Campo | Tipo |
|---|---|
| id | UUID PK |
| owner_user_id | UUID FK/null |
| group_id | UUID FK/null |
| name | string |
| type | enum |
| is_active | boolean |
| is_default | boolean |
| created_at | timestamp |
| updated_at | timestamp |

Tipi V1:

- `CARD`
- `CASH`
- `BANK_TRANSFER`
- `SATISPAY`
- `MEAL_VOUCHER`
- `SPLITWISE`
- `OTHER`

Nota: il metodo `CARD` non deve obbligatoriamente identificare la singola carta. La distinzione tra carta 1/2/3 non è necessaria per le dashboard V1.

---

# 9. Category

Categoria della spesa.

| Campo | Tipo |
|---|---|
| id | UUID PK |
| name | string |
| description | string/null |
| scope | enum |
| owner_user_id | UUID FK/null |
| group_id | UUID FK/null |
| is_system | boolean |
| is_active | boolean |
| sort_order | integer |
| created_at | timestamp |
| updated_at | timestamp |

`scope`:
- `SYSTEM`
- `PERSONAL`
- `GROUP`

Le categorie predefinite devono essere installate automaticamente per un nuovo utente.

---

# 10. Subcategory

| Campo | Tipo |
|---|---|
| id | UUID PK |
| category_id | UUID FK |
| name | string |
| is_active | boolean |
| sort_order | integer |
| created_at | timestamp |
| updated_at | timestamp |

La sottocategoria è sempre figlia di una categoria.

---

# 11. Merchant

Rappresenta il negozio/esercente.

| Campo | Tipo |
|---|---|
| id | UUID PK |
| canonical_name | string |
| normalized_name | string |
| category_id | UUID FK/null |
| subcategory_id | UUID FK/null |
| created_at | timestamp |
| updated_at | timestamp |

Il merchant può essere utilizzato dal motore di suggerimento per proporre categoria e sottocategoria.

Non deve essere obbligatorio creare manualmente un merchant prima di registrare una spesa.

---

# 12. Tag

| Campo | Tipo |
|---|---|
| id | UUID PK |
| name | string |
| scope | enum |
| owner_user_id | UUID FK/null |
| group_id | UUID FK/null |
| status | enum |
| created_at | timestamp |
| updated_at | timestamp |

Scope:
- `PERSONAL`
- `GLOBAL_GROUP`

La trasformazione di un tag personale in tag globale deve essere gestita tramite una relazione/configurazione esplicita e non tramite duplicazione incontrollata.

---

# 13. Expense

È l'entità centrale del dominio.

| Campo | Tipo | Note |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK | proprietario/creatore |
| group_id | UUID FK/null | contesto condiviso |
| expense_date | date | data della spesa |
| total_amount | decimal(19,4) | totale definitivo |
| currency | string(3) | valuta originale |
| converted_amount | decimal(19,4)/null | valuta di riferimento |
| converted_currency | string(3)/null | |
| personal_amount | decimal(19,4) | quota personale |
| category_id | UUID FK | categoria |
| subcategory_id | UUID FK/null | sottocategoria |
| merchant_id | UUID FK/null | esercente |
| description | text/null | causale/note |
| is_extraordinary | boolean | flag straordinaria |
| source_type | enum | MANUAL / PSD2 / CSV |
| source_psd2_transaction_id | UUID FK/null | origine PSD2 |
| source_import_row_id | UUID FK/null | origine CSV |
| created_by | UUID FK | utente che ha creato |
| created_at | timestamp | |
| updated_at | timestamp | |
| deleted_at | timestamp/null | soft delete se necessario |

### Regole

- `total_amount >= 0`.
- `personal_amount >= 0`.
- `personal_amount <= total_amount`.
- `currency` obbligatoria.
- `expense_date` obbligatoria.
- `category_id` obbligatoria dopo il completamento della registrazione.
- `source_type` obbligatorio.

### Nota importante

`total_amount` è il totale reale della spesa contabilizzata.

`personal_amount` è quanto deve incidere sulle analisi personali.

Non devono essere usati come sinonimi.

---

# 14. ExpensePayment

Rappresenta uno split del pagamento.

| Campo | Tipo |
|---|---|
| id | UUID PK |
| expense_id | UUID FK |
| payment_method_id | UUID FK |
| amount | decimal(19,4) |
| currency | string(3) |
| created_at | timestamp |
| updated_at | timestamp |

Vincolo fondamentale:

La somma degli `ExpensePayment.amount` deve corrispondere a `Expense.total_amount` per una spesa contabilizzata completa.

### Esempio

Expense:

`total_amount = 50`

ExpensePayment:

- MEAL_VOUCHER = 20
- CARD = 30

---

# 15. ExpenseShare

Rappresenta la suddivisione della spesa tra persone.

| Campo | Tipo |
|---|---|
| id | UUID PK |
| expense_id | UUID FK |
| user_id | UUID FK/null |
| external_person_name | string/null |
| amount | decimal(19,4) |
| share_type | enum |
| created_at | timestamp |
| updated_at | timestamp |

`share_type` può essere:
- `PERSONAL`
- `OTHER_USER`
- `EXTERNAL_PERSON`

### Esempio

Spesa totale: 10 €

- Daniele: 5 €
- altra persona: 5 €

`personal_amount` = 5 €.

La struttura permette di gestire anche persone non registrate come utenti Pecunia.

---

# 16. ExpenseTag

Relazione molti-a-molti tra spese e tag.

| Campo | Tipo |
|---|---|
| expense_id | UUID FK |
| tag_id | UUID FK |
| created_at | timestamp |

PK composta: `(expense_id, tag_id)`.

---

# 17. PSD2Transaction

Rappresenta un movimento rilevato dalla banca.

| Campo | Tipo | Note |
|---|---|---|
| id | UUID PK | |
| bank_connection_id | UUID FK | origine |
| provider_transaction_id | string | ID provider |
| transaction_date | date | data banca |
| booking_date | date/null | data contabilizzazione bancaria |
| original_amount | decimal(19,4) | importo originale |
| currency | string(3) | |
| merchant_name | string/null | merchant banca |
| raw_description | text/null | causale |
| normalized_description | text/null | opzionale |
| transaction_type | enum | PURCHASE / WITHDRAWAL / TRANSFER / FEE / OTHER |
| status | enum | PENDING / ACCEPTED / IGNORED / ERROR |
| linked_expense_id | UUID FK/null | spesa generata |
| raw_reference | text/null | riferimento tecnico, se necessario |
| first_seen_at | timestamp | |
| last_seen_at | timestamp | |
| created_at | timestamp | |
| updated_at | timestamp | |

### Vincoli

`(bank_connection_id, provider_transaction_id)` unique quando il provider garantisce un identificativo stabile.

Se il provider non garantisce un ID stabile, deve essere implementata una chiave di idempotenza alternativa.

---

# 18. Relazione PSD2 → Expense

Relazione consigliata V1: **0..1 : 1**.

Una `PSD2Transaction` può avere:
- nessuna spesa (`PENDING`/`IGNORED`);
- una sola spesa contabilizzata.

Una `Expense` può avere al massimo una transazione PSD2 come fonte primaria.

Questo evita che la stessa transazione bancaria generi due volte la stessa spesa.

L'importo può però essere differente:

```text
PSD2Transaction.original_amount = 5 €
Expense.total_amount = 15 €
```

---

# 19. ImportBatch

Rappresenta una sessione di import CSV.

| Campo | Tipo |
|---|---|
| id | UUID PK |
| user_id | UUID FK |
| filename | string |
| status | enum |
| total_rows | integer |
| valid_rows | integer |
| invalid_rows | integer |
| imported_rows | integer |
| created_at | timestamp |
| completed_at | timestamp/null |

Stati:
- `UPLOADED`
- `VALIDATING`
- `READY`
- `PROCESSING`
- `COMPLETED`
- `PARTIAL`
- `FAILED`

---

# 20. ImportRow

Rappresenta una riga del CSV.

| Campo | Tipo |
|---|---|
| id | UUID PK |
| import_batch_id | UUID FK |
| row_number | integer |
| raw_data | JSONB |
| parsed_date | date/null |
| parsed_amount | decimal/null |
| parsed_description | text/null |
| status | enum |
| validation_errors | JSONB/null |
| linked_expense_id | UUID FK/null |
| created_at | timestamp |

`raw_data` permette di conservare il contenuto originale della riga senza vincolare il parser a uno schema unico.

---

# 21. Activity

Centro Attività / notifiche operative.

| Campo | Tipo |
|---|---|
| id | UUID PK |
| user_id | UUID FK |
| group_id | UUID FK/null |
| type | enum |
| reference_type | string |
| reference_id | UUID |
| title | string |
| message | text |
| status | enum |
| created_at | timestamp |
| read_at | timestamp/null |
| dismissed_at | timestamp/null |
| resolved_at | timestamp/null |

Tipi iniziali:
- `PSD2_REVIEW`
- `HISTORICAL_UPDATE`
- `IMPORT_RESULT`
- `SYSTEM`

Stati:
- `OPEN`
- `READ`
- `DISMISSED`
- `RESOLVED`

---

# 22. CurrencyRate

Conserva il tasso utilizzato per una conversione.

| Campo | Tipo |
|---|---|
| id | UUID PK |
| rate_date | date |
| base_currency | string(3) |
| quote_currency | string(3) |
| rate | decimal(19,8) |
| provider | string |
| created_at | timestamp |

Vincolo consigliato:

`(rate_date, base_currency, quote_currency, provider)` unique.

La spesa deve conservare il riferimento/tasso effettivamente utilizzato per garantire stabilità storica.

---

# 23. AuditEvent

Traccia le operazioni sensibili senza duplicare inutilmente l'intero database.

| Campo | Tipo |
|---|---|
| id | UUID PK |
| actor_user_id | UUID FK/null |
| action | string |
| entity_type | string |
| entity_id | UUID |
| metadata | JSONB/null |
| created_at | timestamp |

Non inserire nei metadata:
- password;
- token;
- secret OAuth;
- chiavi di cifratura;
- dati bancari non necessari.

---

# 24. Relazioni principali

```text
User
 |\
 | \---- UserSettings
 |
 +----< Expense >---- Group
 |          |
 |          +----< ExpensePayment >---- PaymentMethod
 |          |
 |          +----< ExpenseShare >------- User
 |          |
 |          +----< ExpenseTag >--------- Tag
 |          |
 |          +---- Category
 |          +---- Subcategory
 |          +---- Merchant
 |          |
 |          +---- PSD2Transaction
 |
 +----< BankConnection >---- Group
 |
 +----< Activity
 |
 +----< ImportBatch
              |
              +----< ImportRow

Group
 |
 +----< GroupMember >---- User
```

---

# 25. Personal vs Group data

Una spesa deve appartenere a uno dei due contesti:

1. personale (`group_id = NULL`);
2. gruppo (`group_id != NULL`).

Non deve essere contemporaneamente personale e di gruppo come singola entità.

Se una spesa condivisa deve incidere su più utenti, la suddivisione viene rappresentata tramite `ExpenseShare` e/o le regole del gruppo.

---

# 26. Conto cointestato

Per un conto condiviso:

```text
BankConnection
    |
    +-- group_id = Gruppo Casa
```

Le operazioni PSD2 importate da quella connessione appartengono al contesto del gruppo secondo le regole definite.

Non devono essere automaticamente duplicate come spese personali per ogni membro.

---

# 27. Tags personali → globali

Quando un tag personale viene reso disponibile nel gruppo, il modello deve evitare di creare una copia semanticamente indistinguibile.

Approccio consigliato:

- mantenere un identificatore del tag;
- assegnargli scope globale di gruppo o creare una relazione di condivisione esplicita;
- mantenere l'associazione alle spese esistenti;
- consentire all'admin di modificarlo/eliminarlo secondo le Business Rules.

---

# 28. Soft delete

Per entità finanziarie si preferisce il soft delete o lo stato `ARCHIVED/INACTIVE` quando la cancellazione fisica potrebbe rompere:

- audit;
- riferimenti PSD2;
- dashboard storiche;
- import;
- relazioni di gruppo.

Una categoria eliminata, ad esempio, non deve rendere invalide le spese storiche.

---

# 29. Denaro e precisione

Non utilizzare `float`/`double` per gli importi monetari.

Usare `DECIMAL/NUMERIC`, con precisione sufficiente a gestire valute e conversioni.

La precisione applicativa deve essere definita centralmente.

---

# 30. Date e timezone

- Le date delle spese sono rappresentate come date locali quando non serve un istante temporale.
- Gli eventi tecnici (`created_at`, `updated_at`, sincronizzazioni) devono essere timestamp timezone-aware in UTC.
- La timezone dell'utente è conservata in `UserSettings`.

---

# 31. Indici principali

Il database deve indicizzare almeno:

### Expense
- `(user_id, expense_date)`;
- `(group_id, expense_date)`;
- `(category_id, expense_date)`;
- `(merchant_id, expense_date)`;
- `source_type`;
- `is_extraordinary`.

### PSD2Transaction
- `(bank_connection_id, transaction_date)`;
- `(status, transaction_date)`;
- unique provider transaction identifier.

### Activity
- `(user_id, status, created_at)`.

### Import
- `(import_batch_id, row_number)`.

Gli indici finali devono essere verificati tramite query reali e non aggiunti indiscriminatamente.

---

# 32. Integrità referenziale

Dove appropriato utilizzare:

- foreign key;
- unique constraints;
- check constraints;
- not-null constraints.

Le regole contabili più complesse restano nel Domain Service/backend, mentre i vincoli semplici devono essere protetti anche dal database.

---

# 33. Transazioni

Le operazioni che modificano più entità devono essere atomiche.

Esempio contabilizzazione PSD2:

```text
BEGIN
  update PSD2Transaction -> ACCEPTED
  create Expense
  create ExpensePayment(s)
  create ExpenseShare(s)
  resolve Activity
COMMIT
```

Se una parte fallisce, l'intera operazione deve essere rollbackata.

---

# 34. Esempio completo: spesa PSD2 modificata

### Movimento bancario

`PSD2Transaction`

- provider: Fineco
- original_amount: 5 €
- merchant: Coop
- status: PENDING

### Decisione utente

L'utente apre l'attività e corregge il totale.

### Expense

- total_amount: 15 €
- personal_amount: 15 €
- source_type: PSD2
- source_psd2_transaction_id: movimento Fineco
- merchant: Coop

### ExpensePayment

- CARD: 5 €
- MEAL_VOUCHER: 10 €

Il dato bancario originale rimane 5 €.
La spesa contabilizzata è 15 €.

---

# 35. Esempio completo: spesa condivisa

Transazione totale: 10 €.

`Expense.total_amount = 10`

`ExpenseShare`:

- User A = 5 €
- User B = 5 €

Se la dashboard è personale per User A:

`personal_amount = 5 €`.

La spesa non deve risultare come 10 € nel totale personale di User A.

---

# 36. Esempio: prelievo

`PSD2Transaction`:

- type = WITHDRAWAL
- amount = 100 €
- status = PENDING

Se l'utente sceglie IGNORE:

- nessuna Expense;
- nessun impatto dashboard;
- Activity risolta/archiviata secondo il comportamento UI.

Se l'utente sceglie ACCEPT:

- viene creata una Expense secondo le regole applicabili.

---

# 37. Esempio: spesa straordinaria

Expense:

- total_amount = 500.000 €
- category = Casa
- is_extraordinary = true

La spesa resta nel database e nello storico.

Dashboard:

- `include_extraordinary = false` → esclusa dalle analisi ordinarie;
- `include_extraordinary = true` → inclusa.

---

# 38. Esempio: conversione valuta

Expense:

- expense_date = 2026-08-08
- currency = EUR/foreign currency
- rate = valore del giorno
- converted_amount = valore calcolato

Una successiva apertura dell'app non deve ricalcolare la spesa con il cambio del nuovo giorno.

---

# 39. Privacy by design

Il modello deve minimizzare i dati personali.

Non memorizzare dati bancari che non servono al funzionamento dell'applicazione.

In particolare, evitare di conservare:
- credenziali bancarie;
- password;
- PAN completi delle carte;
- dati non necessari provenienti dal provider PSD2.

Conservare solo i dati necessari per identificare l'origine e gestire correttamente il movimento.

---

# 40. Evoluzione V2

Il modello deve lasciare spazio a:

- budget;
- allegati/scontrini;
- notifiche push;
- regole automatiche avanzate;
- analytics più sofisticate;
- ulteriori provider PSD2;
- maggiore gestione familiare;
- obiettivi di risparmio.

Queste funzionalità non devono essere implementate nella V1 solo per predisporre il modello.

---

# 41. Regola per Codex

Codex deve utilizzare questo modello come riferimento per:

- SQLAlchemy models;
- migrazioni Alembic;
- Pydantic schemas;
- repository/query layer;
- domain services;
- test di integrità.

Non creare campi o relazioni per semplice comodità del frontend se non hanno una responsabilità di dominio.

Quando è necessario introdurre una nuova entità o relazione, documentarne il motivo e verificare la compatibilità con:

- `03_User_Stories.md`;
- `04_Business_Rules.md`;
- `05_System_Architecture.md`.
