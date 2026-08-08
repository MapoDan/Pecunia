export type User = {
  id: string;
  email: string;
  display_name: string;
  role: 'USER' | 'ADMIN';
  status: 'ACTIVE' | 'DISABLED';
  personal_context_id: string;
  settings: {
    default_currency: string;
    locale: string;
    timezone: string;
    dashboard_config: Record<string, unknown>;
    notification_preferences: Record<string, unknown>;
  };
};

export async function googleLogin(idToken: string): Promise<{ user: User; csrf_token: string }> {
  const response = await fetch('/api/v1/auth/google', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ id_token: idToken }),
  });
  if (!response.ok) throw new Error('Accesso Google non riuscito');
  return response.json();
}

export async function fetchMe(): Promise<User | null> {
  const response = await fetch('/api/v1/auth/me', { credentials: 'include' });
  if (response.status === 401) return null;
  if (!response.ok) throw new Error('Profilo non disponibile');
  return response.json();
}

export async function logout(csrfToken: string): Promise<void> {
  const response = await fetch('/api/v1/auth/logout', {
    method: 'POST',
    headers: { 'x-csrf-token': csrfToken },
    credentials: 'include',
  });
  if (!response.ok) throw new Error('Logout non riuscito');
}
