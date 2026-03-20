const BASE_URL = '/api'

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    credentials: 'include',
    ...options,
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error ?? 'Request failed')
  return data as T
}

export interface User {
  id: number
  username: string
  email: string
}

export interface Transaction {
  id: number
  amount: number
  category: string
  type: 'income' | 'expense'
  note: string | null
  transaction_date: string
}

export interface Summary {
  income: number
  expenses: number
  net: number
}

export interface TransactionsResponse {
  transactions: Transaction[]
  summary: Summary
}

export interface NewTransaction {
  amount: number
  category: string
  type: 'income' | 'expense'
  note?: string
}

export const api = {
  auth: {
    register: (data: { username: string; email: string; password: string }) =>
      request<User>('/auth/register', { method: 'POST', body: JSON.stringify(data) }),

    login: (data: { username: string; password: string }) =>
      request<User>('/auth/login', { method: 'POST', body: JSON.stringify(data) }),

    logout: () =>
      request<{ message: string }>('/auth/logout', { method: 'POST' }),

    me: () =>
      request<User>('/auth/me'),
  },

  transactions: {
    list: () =>
      request<TransactionsResponse>('/transactions'),

    create: (data: NewTransaction) =>
      request<Transaction>('/transactions', { method: 'POST', body: JSON.stringify(data) }),

    delete: (id: number) =>
      request<{ message: string }>(`/transactions/${id}`, { method: 'DELETE' }),
  },
}
