# Pecunia

Pecunia è una Progressive Web App (PWA) self-hosted per il tracciamento e l'analisi delle spese personali e condivise.

La V1 è progettata per funzionare su un NAS domestico tramite Docker, con backend API, worker per le attività asincrone e PostgreSQL.

## Stato del progetto

**Milestone 1 — Bootstrap tecnico:** in corso.

Sono presenti:

- struttura iniziale frontend React + TypeScript + Vite;
- backend FastAPI;
- PostgreSQL tramite Docker Compose;
- health checks API;
- primo test backend;
- PWA manifest;
- container frontend/backend;
- CI iniziale.

Le funzionalità di dominio verranno implementate progressivamente tramite vertical slices.

## Avvio locale

Copiare `.env.example` in `.env`, impostare almeno i secret locali e avviare:

```bash
docker compose -f docker/compose.dev.yml up --build
```

Frontend: `http://localhost:5173`  
API: `http://localhost:8000`  
API health: `http://localhost:8000/health/live`

Il database non deve essere esposto in produzione.

## Documentazione

La documentazione funzionale e tecnica è la fonte di verità del progetto.

- [Visione](docs/00_Vision.md)
- [Requisiti funzionali](docs/01_Functional_Requirements.md)
- [Requisiti non funzionali](docs/02_Non_Functional_Requirements.md)
- [User stories](docs/03_User_Stories.md)
- [Regole di business](docs/04_Business_Rules.md)
- [Modello dati](docs/06_Data_Model.md)
- [Architettura](docs/05_System_Architecture.md)
- [API](docs/07_API_Specification.md)
- [Frontend/UX](docs/08_Frontend_UX_Specification.md)
- [Sicurezza](docs/09_Security_Specification.md)
- [Development Guidelines](docs/10_Development_Guidelines.md)

## Principi di progetto

1. **Rapidità di inserimento:** una spesa deve poter essere registrata in pochi secondi.
2. **Automazione assistita:** il sistema suggerisce, l'utente conferma quando l'informazione ha impatto contabile.
3. **Nessun dato finanziario inventato:** le spese derivano da inserimento manuale, import o operazioni PSD2 effettivamente rilevate e confermate.
4. **Separazione dei concetti:** spesa, movimento bancario, metodo di pagamento, origine e contesto di gruppo sono entità distinte.
5. **Privacy:** i dati personali restano personali salvo condivisione esplicita tramite gruppi.
6. **Self-hosted e leggero:** il backend deve essere adatto a un NAS domestico con risorse limitate.
7. **Sicurezza by design:** authorization server-side, secret management, cifratura e minimizzazione dei dati.
8. **Evolutivo:** V1 deve essere completa nel proprio perimetro senza introdurre complessità necessaria a funzionalità future.

## Branding

I file ufficiali del brand saranno inseriti in `frontend/public/branding/`.

File previsti:

- `pecunia-logo.svg` — logo completo;
- `pecunia-icon.svg` — icona applicazione;
- eventuali favicon e asset PWA.

## Sviluppo

Lo sviluppo segue una strategia a vertical slices:

1. bootstrap + autenticazione;
2. inserimento/lista spese;
3. split pagamenti e quota personale;
4. categorie/negozi/suggerimenti;
5. dashboard;
6. PSD2;
7. Centro Attività;
8. CSV;
9. gruppi;
10. dashboard admin;
11. hardening e deployment.

Ogni slice deve essere testabile e lasciare il progetto in uno stato funzionante.
