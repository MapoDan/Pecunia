# Pecunia — API Specification

**Versione:** 1.0  
**Scope:** V1  
**Stato:** contratto funzionale/tecnico di riferimento per frontend e backend

## 1. Scopo

Questo documento definisce il contratto REST tra PWA e backend di Pecunia.

Le API devono essere:

- versionate;
- documentate tramite OpenAPI;
- validate lato server;
- autorizzate lato server;
- idempotenti dove necessario;
- indipendenti dai dettagli implementativi del database.

Base path:

```text
/api/v1
```

Formato predefinito: JSON.

---

# 2. Convenzioni

## 2.1 ID

Tutti gli identificativi applicativi sono UUID.

## 2.2 Date

Date di dominio: `YYYY-MM-DD`.

Timestamp tecnici: ISO 8601 con timezone, preferibilmente UTC.

## 2.3 Importi

Gli importi vengono trasmessi come stringhe decimal-safe oppure come numeri JSON solo se il client garantisce precisione sufficiente. La scelta definitiva deve essere uniforme in tutta l'API.

Esempio consigliato:

```json
{
  "amount": "15.00",
  "currency": "EUR"
}
```

## 2.4 Pagination

Le liste devono supportare almeno:

```text
?page=1&page_size=50
```

Limite massimo server-side obbligatorio.

Response standard:

```json
{
  "items": [],
  "page": 1,
  "page_size": 50,
  "total": 123
}
```

Per dataset molto grandi può essere introdotta cursor pagination senza modificare il dominio.

---

# 3. Autenticazione

## 3.1 Login Google

```http
GET /api/v1/auth/google/login
```

Avvia il flusso OAuth/OIDC.

Callback gestita dal backend:

```http
GET /api/v1/auth/google/callback
```

Il backend crea/recupera l'utente Pecunia e stabilisce la sessione.

La PWA non deve conoscere client secret OAuth.

## 3.2 Sessione

```http
GET /api/v1/auth/me
```

Response:

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "display_name": "Daniele",
  "role": "USER",
  "status": "ACTIVE"
}
```

Logout:

```http
POST /api/v1/auth/logout
```

## 3.3 Passkey

V1 deve predisporre il contratto per WebAuthn.

```http
POST /api/v1/auth/passkeys/register/options
POST /api/v1/auth/passkeys/register/verify
POST /api/v1/auth/passkeys/login/options
POST /api/v1/auth/passkeys/login/verify
GET  /api/v1/auth/passkeys
DELETE /api/v1/auth/passkeys/{passkey_id}
```

La registrazione della prima passkey richiede una sessione autenticata.

---

# 4. Error model

Tutti gli errori applicativi devono utilizzare un formato coerente.

Esempio:

```json
{
  "error": {
    "code": "EXPENSE_PAYMENT_SUM_MISMATCH",
    "message": "La somma dei metodi di pagamento deve corrispondere al totale della spesa.",
    "details": {}
  },
  "request_id": "uuid"
}
```

Codici HTTP principali:

- `400` richiesta non valida;
- `401` non autenticato;
- `403` non autorizzato;
- `404` risorsa inesistente/non accessibile;
- `409` conflitto/idempotenza/vincolo;
- `422` errore di validazione;
- `429` rate limit;
- `500` errore inatteso.

Il backend non deve esporre stack trace al client.

---

# 5. Profilo e configurazione

## 5.1 Profilo

```http
GET /api/v1/me
PATCH /api/v1/me
```

Modificabili:
- display name dove previsto;
- impostazioni personali;
- preferenze UI non sensibili.

## 5.2 Settings

```http
GET /api/v1/settings
PATCH /api/v1/settings
```

Campi iniziali:
- default currency;
- locale;
- timezone;
- onboarding status.

---

# 6. Categorie

```http
GET    /api/v1/categories
POST   /api/v1/categories
GET    /api/v1/categories/{category_id}
PATCH  /api/v1/categories/{category_id}
DELETE /api/v1/categories/{category_id}
```

Sottocategorie:

```http
GET    /api/v1/categories/{category_id}/subcategories
POST   /api/v1/categories/{category_id}/subcategories
PATCH  /api/v1/subcategories/{subcategory_id}
DELETE /api/v1/subcategories/{subcategory_id}
```

La cancellazione di una categoria usata storicamente deve produrre un'archiviazione/inattivazione, non invalidare le spese.

---

# 7. Merchant e suggerimenti

```http
GET /api/v1/merchants
GET /api/v1/merchants/search?q=coop
GET /api/v1/merchants/{merchant_id}
PATCH /api/v1/merchants/{merchant_id}
```

Suggerimenti contestuali:

```http
GET /api/v1/suggestions/expense
```

Parametri possibili:

- merchant;
- descrizione/causale;
- metodo di pagamento;
- data;
- importo.

Response esempio:

```json
{
  "category": {
    "id": "uuid",
    "confidence": 0.94
  },
  "subcategory": {
    "id": "uuid",
    "confidence": 0.81
  },
  "merchant": {
    "id": "uuid",
    "confidence": 0.99
  }
}
```

I suggerimenti sono sempre non vincolanti e modificabili dall'utente.

---

# 8. Metodi di pagamento

```http
GET    /api/v1/payment-methods
POST   /api/v1/payment-methods
PATCH  /api/v1/payment-methods/{payment_method_id}
DELETE /api/v1/payment-methods/{payment_method_id}
```

Il frontend deve poter ottenere i metodi disponibili per il contesto personale o di gruppo.

---

# 9. Spese

## 9.1 Lista

```http
GET /api/v1/expenses
```

Filtri supportati:

- `from_date`;
- `to_date`;
- `category_id`;
- `subcategory_id`;
- `merchant_id`;
- `payment_method_id`;
- `tag_id`;
- `group_id`;
- `is_extraordinary`;
- `source_type`;
- `min_amount`;
- `max_amount`;
- `search`;
- `currency`.

Sorting:

- `expense_date`;
- `total_amount`;
- `created_at`.

Il server deve validare i campi di sorting per evitare SQL injection tramite query dinamiche.

## 9.2 Dettaglio

```http
GET /api/v1/expenses/{expense_id}
```

## 9.3 Creazione

```http
POST /api/v1/expenses
```

Request esempio:

```json
{
  "expense_date": "2026-08-08",
  "total_amount": "50.00",
  "currency": "EUR",
  "personal_amount": "50.00",
  "category_id": "uuid",
  "subcategory_id": "uuid",
  "merchant_id": "uuid",
  "description": "Cena",
  "is_extraordinary": false,
  "group_id": null,
  "payments": [
    {
      "payment_method_id": "uuid-card",
      "amount": "30.00"
    },
    {
      "payment_method_id": "uuid-meal-voucher",
      "amount": "20.00"
    }
  ],
  "shares": [
    {
      "type": "PERSONAL",
      "amount": "50.00"
    }
  ],
  "tag_ids": []
}
```

Il backend deve verificare che:

```text
sum(payments) = total_amount
```

e che:

```text
0 <= personal_amount <= total_amount
```

## 9.4 Modifica

```http
PATCH /api/v1/expenses/{expense_id}
```

Le modifiche devono passare dalle stesse Business Rules della creazione.

## 9.5 Eliminazione

```http
DELETE /api/v1/expenses/{expense_id}
```

Per le entità finanziarie può essere implementato soft delete/archive.

La scelta effettiva deve preservare audit e integrità storica.

---

# 10. Contabilizzazione PSD2

Endpoint dedicato:

```http
POST /api/v1/psd2/transactions/{transaction_id}/accept
```

Request esempio:

```json
{
  "expense_date": "2026-08-08",
  "total_amount": "15.00",
  "currency": "EUR",
  "personal_amount": "15.00",
  "category_id": "uuid",
  "subcategory_id": "uuid",
  "merchant_id": "uuid",
  "description": "Coop",
  "is_extraordinary": false,
  "payments": [
    {
      "payment_method_id": "card",
      "amount": "5.00"
    },
    {
      "payment_method_id": "meal-voucher",
      "amount": "10.00"
    }
  ],
  "shares": [
    {
      "type": "PERSONAL",
      "amount": "15.00"
    }
  ]
}
```

Il backend deve eseguire atomicamente:

1. verifica che la transazione sia `PENDING`;
2. verifica autorizzazione dell'utente;
3. valida la spesa;
4. crea Expense;
5. crea ExpensePayment;
6. crea ExpenseShare;
7. collega `linked_expense_id`;
8. porta PSD2Transaction a `ACCEPTED`;
9. risolve l'Activity associata.

---

# 11. Ignora transazione PSD2

```http
POST /api/v1/psd2/transactions/{transaction_id}/ignore
```

Request opzionale:

```json
{
  "reason": "Prelievo non contabilizzato: registrerò separatamente le spese in contanti"
}
```

Effetto:

- PSD2Transaction → `IGNORED`;
- nessuna Expense;
- Activity → risolta/dismissed secondo stato UI.

La transazione resta disponibile nello storico tecnico PSD2.

---

# 12. Modifica PSD2 prima dell'accettazione

```http
PATCH /api/v1/psd2/transactions/{transaction_id}
```

Può aggiornare esclusivamente i dati necessari alla successiva contabilizzazione secondo le Business Rules.

Il dato bancario originale deve rimanere immutabile.

---

# 13. Lista PSD2

```http
GET /api/v1/psd2/transactions
```

Filtri:

- `status`;
- `bank_connection_id`;
- `from_date`;
- `to_date`;
- `merchant`;
- `transaction_type`.

La response deve includere chiaramente:

```json
{
  "bank_connection": {
    "id": "uuid",
    "institution_name": "Fineco",
    "display_name": "Conto Fineco"
  }
}
```

Questo requisito è fondamentale quando l'utente possiede più conti.

---

# 14. Bank Connections

Lista:

```http
GET /api/v1/bank-connections
```

Creazione/avvio collegamento:

```http
POST /api/v1/bank-connections/connect
```

Il backend restituisce l'URL/sessione necessaria per completare il consent presso il provider.

Dettaglio:

```http
GET /api/v1/bank-connections/{connection_id}
```

Disconnessione:

```http
POST /api/v1/bank-connections/{connection_id}/disconnect
```

Sincronizzazione manuale:

```http
POST /api/v1/bank-connections/{connection_id}/sync
```

La sincronizzazione iniziale parte da `sync_from`, normalmente uguale alla data/istante di collegamento.

---

# 15. Import CSV

## Upload

```http
POST /api/v1/imports/csv
```

Content-Type: `multipart/form-data`.

La response crea un `ImportBatch`.

## Preview/validazione

```http
GET /api/v1/imports/{import_id}
GET /api/v1/imports/{import_id}/rows
```

## Mapping

```http
POST /api/v1/imports/{import_id}/mapping
```

## Conferma

```http
POST /api/v1/imports/{import_id}/commit
```

## Annullamento

```http
POST /api/v1/imports/{import_id}/cancel
```

L'import CSV può contenere date precedenti alla creazione dell'account o al collegamento PSD2.

---

# 16. Activity Center

Lista:

```http
GET /api/v1/activities
```

Filtri:

- `status`;
- `type`;
- `from_date`;
- `to_date`.

Dettaglio:

```http
GET /api/v1/activities/{activity_id}
```

Segna come letta:

```http
POST /api/v1/activities/{activity_id}/read
```

Dismiss:

```http
POST /api/v1/activities/{activity_id}/dismiss
```

Resolve:

```http
POST /api/v1/activities/{activity_id}/resolve
```

Il Centro Attività deve poter rappresentare messaggi aggregati come:

> Individuate 12 operazioni che necessitano aggiornamenti.

Il dettaglio deve permettere di aprire direttamente la lista delle operazioni coinvolte.

---

# 17. Dashboard

## Summary

```http
GET /api/v1/dashboard/summary
```

Filtri:

- periodo;
- gruppo;
- categoria;
- tag;
- merchant;
- metodo di pagamento;
- extraordinary;
- valuta.

Response concettuale:

```json
{
  "total": "2450.00",
  "personal_total": "1980.00",
  "average": "65.83",
  "expense_count": 37,
  "extraordinary_total": "470.00"
}
```

## Time series

```http
GET /api/v1/dashboard/timeseries
```

Supporto a:
- giorno;
- settimana;
- mese.

## Categories

```http
GET /api/v1/dashboard/categories
```

## Payment methods

```http
GET /api/v1/dashboard/payment-methods
```

## Merchants

```http
GET /api/v1/dashboard/merchants
```

## Tags

```http
GET /api/v1/dashboard/tags
```

## Comparison

```http
GET /api/v1/dashboard/compare
```

Permette confronto tra due periodi.

Esempio:

```text
Agosto 2026 vs Agosto 2025
```

Le aggregazioni devono essere calcolate dal backend/database.

---

# 18. Dashboard configurabile

Configurazione:

```http
GET /api/v1/dashboard/layout
PUT /api/v1/dashboard/layout
```

Il layout può contenere widget come:

- totale spese;
- andamento nel tempo;
- categorie;
- top merchant;
- metodi di pagamento;
- spese straordinarie;
- confronto periodi;
- tag;
- insight statistici.

Il backend conserva solamente la configurazione, non HTML o componenti UI.

---

# 19. Gruppi

Lista:

```http
GET /api/v1/groups
```

Creazione:

```http
POST /api/v1/groups
```

Dettaglio:

```http
GET /api/v1/groups/{group_id}
```

Modifica:

```http
PATCH /api/v1/groups/{group_id}
```

Archiviazione:

```http
POST /api/v1/groups/{group_id}/archive
```

---

# 20. Membri gruppo

```http
GET  /api/v1/groups/{group_id}/members
POST /api/v1/groups/{group_id}/members
PATCH /api/v1/groups/{group_id}/members/{member_id}
DELETE /api/v1/groups/{group_id}/members/{member_id}
```

I permessi devono essere verificati server-side.

Il caso figli/genitori deve utilizzare il ruolo/permission model del gruppo senza introdurre una seconda gerarchia di utenti.

---

# 21. Tag

```http
GET    /api/v1/tags
POST   /api/v1/tags
PATCH  /api/v1/tags/{tag_id}
DELETE /api/v1/tags/{tag_id}
```

Condivisione in gruppo:

```http
POST /api/v1/groups/{group_id}/tags/{tag_id}/share
```

L'admin del gruppo può modificare/eliminare i tag globali secondo le Business Rules.

---

# 22. Valute e cambi

```http
GET /api/v1/currencies
GET /api/v1/currency-rates?date=2026-08-08
```

Il cambio utilizzato nella spesa deve essere salvato e non ricalcolato automaticamente a ogni accesso.

---

# 23. Admin API

Tutti gli endpoint `/admin` richiedono ruolo `ADMIN`.

## Dashboard utilizzo

```http
GET /api/v1/admin/dashboard/usage
```

Metriche possibili:
- utenti attivi;
- nuovi utenti;
- numero spese;
- numero operazioni PSD2;
- import CSV;
- gruppi;
- errori applicativi aggregati.

## Performance

```http
GET /api/v1/admin/dashboard/performance
```

Metriche:
- latency API;
- error rate;
- job falliti;
- sincronizzazioni PSD2;
- utilizzo risorse quando disponibile dal backend.

Non devono essere esposti dati finanziari individuali nelle metriche amministrative se non necessari.

---

# 24. Health endpoints

```http
GET /health/live
GET /health/ready
```

`live`: processo attivo.

`ready`: applicazione pronta a servire richieste, con dipendenze essenziali disponibili.

---

# 25. Idempotency

Endpoint sensibili che possono essere ritentati devono accettare:

```http
Idempotency-Key: <uuid>
```

In particolare:

- contabilizzazione PSD2;
- ignore PSD2;
- commit import;
- creazione spesa quando il client può ritentare dopo timeout;
- sync manuale quando necessario.

Una richiesta ripetuta con la stessa chiave deve restituire il risultato della prima operazione compatibile, non crearne una seconda.

---

# 26. Concorrenza

Il backend deve proteggere le operazioni PSD2 da doppia contabilizzazione.

Esempio:

```text
User A ---- accept ----+
                       +--> DB transaction/lock --> ONE Expense
User B ---- accept ----+
```

Il secondo tentativo deve ricevere un conflitto controllato.

---

# 27. Autorizzazione

Ogni endpoint deve verificare:

1. autenticazione;
2. ownership o membership;
3. ruolo;
4. contesto personale/gruppo;
5. eventuale permission specifica.

Non è sufficiente nascondere pulsanti nel frontend.

---

# 28. CORS e browser security

In produzione:

- consentire solo origin configurati;
- non usare `*` per API autenticate;
- cookie/token con policy sicure;
- HTTPS obbligatorio.

---

# 29. OpenAPI

Il backend deve generare automaticamente lo schema OpenAPI.

Il file deve poter essere esportato nel repository, ad esempio:

```text
contracts/openapi.yaml
```

La specifica generata dal codice deve essere coerente con questo documento.

---

# 30. Test API

Devono essere previsti almeno:

- test autenticazione;
- autorizzazione;
- CRUD categorie;
- CRUD spese;
- split pagamenti;
- personal amount;
- PSD2 accept/ignore;
- modifica importo PSD2;
- idempotenza;
- import CSV;
- gruppi;
- tag;
- dashboard;
- admin authorization.

I test devono verificare soprattutto le Business Rules, non soltanto gli status code HTTP.

---

# 31. Compatibilità frontend

Il frontend non deve dipendere da dettagli SQL.

Le API devono fornire dati già sufficientemente aggregati per:

- mobile;
- desktop;
- grafici;
- tabelle;
- ricerca;
- filtri.

Il backend deve evitare response gigantesche.

---

# 32. Regole per Codex

Quando implementa un endpoint Codex deve:

1. verificare le Business Rules;
2. verificare il Data Model;
3. implementare validation Pydantic;
4. implementare authorization;
5. aggiungere test;
6. aggiornare OpenAPI;
7. evitare logica contabile nel frontend;
8. usare transazioni DB quando modifica più entità;
9. gestire idempotenza dove prevista;
10. non introdurre nuovi endpoint duplicati per semplice comodità UI.

Se esiste un conflitto tra UI e Business Rules, prevalgono le Business Rules.

---

# 33. API non previste nella V1

Non implementare ancora endpoint per:

- budget;
- investimenti;
- patrimonio;
- allegati/scontrini;
- prestiti;
- pianificazione finanziaria;
- obiettivi di risparmio;
- AI conversazionale.

Le estensioni V2 devono essere aggiunte senza contaminare inutilmente il contratto V1.
