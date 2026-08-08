import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

export function App() {
  return <main className="shell"><section className="card"><p className="eyebrow">Pecunia V1</p><h1>Controllo spese self-hosted</h1><p>Fondazione PWA pronta per le prossime milestone: identità, spese e dashboard.</p></section></main>;
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
