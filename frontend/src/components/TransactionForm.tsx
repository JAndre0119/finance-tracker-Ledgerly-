import { useState, FormEvent } from 'react'
import { NewTransaction } from '../api/client'

interface Props {
  onAdd: (transaction: NewTransaction) => Promise<void>
}

export default function TransactionForm({ onAdd }: Props) {
  const [amount, setAmount] = useState('')
  const [category, setCategory] = useState('')
  const [type, setType] = useState<'income' | 'expense'>('expense')
  const [note, setNote] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    try {
      await onAdd({
        amount: parseFloat(amount),
        category,
        type,
        note: note || undefined,
      })
      setAmount('')
      setCategory('')
      setType('expense')
      setNote('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add transaction')
    }
  }

  return (
    <div>
      <h2>Add Transaction</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Amount</label>
          <input
            type="number"
            step="0.01"
            min="0"
            value={amount}
            onChange={e => setAmount(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Category</label>
          <input
            value={category}
            onChange={e => setCategory(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Type</label>
          <select
            value={type}
            onChange={e => setType(e.target.value as 'income' | 'expense')}
          >
            <option value="expense">Expense</option>
            <option value="income">Income</option>
          </select>
        </div>
        <div>
          <label>Note</label>
          <input value={note} onChange={e => setNote(e.target.value)} />
        </div>
        <button type="submit">Add</button>
      </form>
    </div>
  )
}
