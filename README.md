# Pecunia

Pecunia è una Progressive Web App (PWA) self-hosted per il tracciamento e l'analisi delle spese personali e condivise.

L'obiettivo della V1 è permettere di registrare le spese con il minimo attrito possibile, integrarle con operazioni bancarie tramite PSD2 senza registrazione automatica, importare lo storico da CSV e fornire dashboard utili a comprendere i comportamenti di spesa e individuare opportunità di risparmio.

## Documentazione

- [Visione prodotto](docs/00_Vision.md)
- [Requisiti funzionali](docs/01_Functional_Requirements.md)
- [Requisiti non funzionali](docs/02_Non_Functional_Requirements.md)
- [User stories](docs/03_User_Stories.md)
- [Regole di business](docs/04_Business_Rules.md)
- [Modello dati](docs/05_Data_Model.md)
- [Architettura](docs/06_System_Architecture.md)
- [API](docs/07_API_Design.md)
- [UI/UX](docs/08_UI_UX_Guidelines.md)
- [Dashboard](docs/09_Dashboard_Specification.md)
- [Backlog](docs/10_Backlog.md)
- [Linee guida per Codex](docs/11_AI_DEVELOPMENT_GUIDELINES.md)
- [Standard di coding](docs/12_Coding_Standards.md)
- [Decisioni tecnologiche](docs/13_Technology_Decisions.md)

## Logo

I file ufficiali del brand saranno inseriti in `assets/branding/`.

- `logo.png` — logo completo
- `icon.png` — icona applicazione
- `favicon.png` — favicon

Placeholder/documentazione: [Branding](docs/08_UI_UX_Guidelines.md#branding).

## Principi di progetto

1. **Rapidità di inserimento:** una spesa deve poter essere registrata in pochi secondi.
2. **Automazione assistita:** il sistema suggerisce, l'utente conferma quando l'informazione ha impatto contabile.
3. **Nessun dato finanziario inventato:** le spese devono derivare da inserimento manuale, import o operazioni PSD2 effettivamente rilevate e confermate.
4. **Separazione dei concetti:** spesa, movimento bancario, metodo di pagamento, origine e contesto di gruppo sono entità concettualmente distinte.
5. **Privacy:** i dati personali restano personali salvo condivisione esplicita tramite gruppi.
6. **Self-hosted e leggero:** il backend deve essere adatto a un NAS domestico con risorse limitate.
7. **Evolutivo:** V1 deve essere completa nel proprio perimetro, senza introdurre complessità necessaria a funzionalità future.

## Stato

La documentazione è la specifica di riferimento per lo sviluppo della V1. Le decisioni non ancora definite devono essere trattate come aperte e non inventate autonomamente durante l'implementazione.
