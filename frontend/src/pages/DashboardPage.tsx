import { useState, useEffect, useCallback } from 'react'
import { api, User, Transaction, Summary, NewTransaction } from '../api/client'
import TransactionForm from '../components/TransactionForm'
import TransactionList from '../components/TransactionList'

interface Props {
  user: User
  onLogout: () => void
}

export default function DashboardPage({ user, onLogout }: Props) {
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [summary, setSummary] = useState<Summary>({ income: 0, expenses: 0, net: 0 })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchTransactions = useCallback(async () => {
    try {
      const data = await api.transactions.list()
      setTransactions(data.transactions)
      setSummary(data.summary)
    } catch {
      setError('Failed to load transactions')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchTransactions()
  }, [fetchTransactions])

  async function handleAdd(newTransaction: NewTransaction) {
    await api.transactions.create(newTransaction)
    await fetchTransactions()
  }

  async function handleDelete(id: number) {
    await api.transactions.delete(id)
    await fetchTransactions()
  }

  async function handleLogout() {
    await api.auth.logout()
    onLogout()
  }

  if (loading) return <div>Loading...</div>

  return (
    <div>
      <header>
        <h1>Ledgerly</h1>
        <span>Welcome, {user.username}</span>
        <button onClick={handleLogout}>Logout</button>
      </header>

      <section>
        <h2>Summary</h2>
        <div>Income: ${summary.income.toFixed(2)}</div>
        <div>Expenses: ${summary.expenses.toFixed(2)}</div>
        <div>Net: ${summary.net.toFixed(2)}</div>
      </section>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <TransactionForm onAdd={handleAdd} />
      <TransactionList transactions={transactions} onDelete={handleDelete} />
    </div>
  )
}
