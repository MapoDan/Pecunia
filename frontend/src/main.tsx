import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function App() {
  return (
    <main className="shell">
      <header className="header">
        <div>
          <p className="eyebrow">PERSONAL FINANCE</p>
          <h1>Pecunia</h1>
        </div>
        <button className="iconButton" aria-label="Notifiche">🔔</button>
      </header>

      <section className="summary" aria-labelledby="summary-title">
        <p id="summary-title" className="muted">Spese del mese</p>
        <strong>€ 0,00</strong>
        <p className="muted">La tua prima spesa comparirà qui.</p>
      </section>

      <button className="primaryAction">+ Inserisci spesa</button>

      <section className="card">
        <h2>Dashboard</h2>
        <p className="muted">Le analisi delle tue spese saranno disponibili qui.</p>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
