export type User = { id: string; email: string; display_name: string; role: 'USER' | 'ADMIN'; status: 'ACTIVE' | 'DISABLED'; personal_context_id: string; settings: { default_currency: string; locale: string; timezone: string; dashboard_config: Record<string, unknown>; notification_preferences: Record<string, unknown> } };
export type Category = { id: string; name: string; parent_id: string | null; children: Category[] };
export type PaymentMethodType = { id: string; code: string; name: string };
export type Expense = { id: string; amount: string; personal_amount: string; currency: string; description: string; transaction_date: string; extraordinary: boolean; source: string; category_id: string | null; subcategory_id: string | null; merchant_name: string | null; payment_method_type_id: string | null; tags: string[]; notes: string | null };
export type Suggestion = { merchant_name: string | null; category_id: string | null; subcategory_id: string | null; payment_method_type_id: string | null; reason: string };

async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`/api/v1${path}`, { credentials: 'include', ...options, headers: { 'Content-Type': 'application/json', ...(options.headers ?? {}) } });
  if (!response.ok) throw new Error(`API error ${response.status}`);
  if (response.status === 204) return undefined as T;
  return response.json();
}

export async function googleLogin(idToken: string): Promise<{ user: User; csrf_token: string }> { return api('/auth/google', { method: 'POST', body: JSON.stringify({ id_token: idToken }) }); }
export async function fetchMe(): Promise<User | null> { const response = await fetch('/api/v1/auth/me', { credentials: 'include' }); if (response.status === 401) return null; if (!response.ok) throw new Error('Profilo non disponibile'); return response.json(); }
export async function logout(csrfToken: string): Promise<void> { await api('/auth/logout', { method: 'POST', headers: { 'x-csrf-token': csrfToken } }); }
export async function fetchCategories(): Promise<Category[]> { return api('/categories'); }
export async function fetchPaymentMethods(): Promise<PaymentMethodType[]> { return api('/payment-methods'); }
export async function fetchExpenses(): Promise<Expense[]> { return api('/expenses'); }
export async function fetchSuggestion(text: string): Promise<Suggestion> { return api(`/classification/suggestions?q=${encodeURIComponent(text)}`); }
export async function createExpense(payload: { amount: string; description: string; transaction_date: string; currency: string; extraordinary: boolean; category_id: string | null; subcategory_id: string | null; merchant_name: string; payment_method_type_id: string | null; tags: string[] }): Promise<Expense> { return api('/expenses', { method: 'POST', body: JSON.stringify(payload) }); }
