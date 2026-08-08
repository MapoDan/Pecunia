import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { fetchMe, googleLogin, logout, type User } from './api';
import './styles.css';

declare global {
  interface Window {
    google?: { accounts: { id: { initialize: (options: unknown) => void; renderButton: (element: HTMLElement, options: unknown) => void } } };
  }
}

const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID as string | undefined;

export function App() {
  const [user, setUser] = useState<User | null>(null);
  const [csrfToken, setCsrfToken] = useState<string>('');
  const [status, setStatus] = useState<string>('Caricamento profilo…');

  useEffect(() => {
    fetchMe().then((profile) => {
      setUser(profile);
      setStatus(profile ? 'Sessione attiva' : 'Accedi per continuare');
    }).catch(() => setStatus('Backend non raggiungibile'));
  }, []);

  useEffect(() => {
    if (!googleClientId || user) return;
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onload = () => {
      const button = document.getElementById('google-signin');
      window.google?.accounts.id.initialize({
        client_id: googleClientId,
        callback: async (response: { credential: string }) => {
          const auth = await googleLogin(response.credential);
          setUser(auth.user);
          setCsrfToken(auth.csrf_token);
          setStatus('Sessione attiva');
        },
      });
      if (button) window.google?.accounts.id.renderButton(button, { theme: 'outline', size: 'large', width: 280 });
    };
    document.body.appendChild(script);
    return () => { document.body.removeChild(script); };
  }, [user]);

  async function onLogout() {
    await logout(csrfToken);
    setUser(null);
    setCsrfToken('');
    setStatus('Logout effettuato');
  }

  return <main className="shell"><section className="card"><p className="eyebrow">Pecunia V1 · Identity</p><h1>Il tuo spazio spese privato</h1><p>{status}</p>{user ? <div className="profile"><strong>{user.display_name}</strong><span>{user.email}</span><span>Ruolo applicativo: {user.role}</span><span>Contesto personale: {user.personal_context_id}</span><button onClick={onLogout}>Esci</button></div> : <div className="auth"><div id="google-signin" aria-label="Accedi con Google" />{!googleClientId && <p className="warning">Configura VITE_GOOGLE_CLIENT_ID per abilitare Google Sign-In nel frontend.</p>}</div>}</section></main>;
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
