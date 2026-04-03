import { useState, FormEvent } from 'react'
import { NewTransaction } from '../api/client'

const CATEGORIES: Record<'income' | 'expense', string[]> = {
  expense: ['Food & Drink', 'Rent', 'Transport', 'Utilities', 'Entertainment', 'Healthcare', 'Shopping', 'Education', 'Other'],
  income: ['Salary', 'Freelance', 'Investment', 'Gift', 'Other'],
}

function todayString() {
  return new Date().toISOString().split('T')[0]
}

interface Props {
  onAdd: (transaction: NewTransaction) => Promise<void>
}

export default function TransactionForm({ onAdd }: Props) {
  const [amount, setAmount] = useState('')
  const [type, setType] = useState<'income' | 'expense'>('expense')
  const [category, setCategory] = useState(CATEGORIES.expense[0])
  const [customCategory, setCustomCategory] = useState('')
  const [note, setNote] = useState('')
  const [date, setDate] = useState(todayString())
  const [error, setError] = useState('')

  function handleTypeChange(newType: 'income' | 'expense') {
    setType(newType)
    setCategory(CATEGORIES[newType][0])
    setCustomCategory('')
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')

    const resolvedCategory = category === 'Other' ? customCategory.trim() : category
    if (!resolvedCategory) {
      setError('Please enter a category name.')
      return
    }

    try {
      await onAdd({
        amount: parseFloat(amount),
        category: resolvedCategory,
        type,
        note: note || undefined,
        transaction_date: date,
      })
      setAmount('')
      setCategory(CATEGORIES[type][0])
      setCustomCategory('')
      setNote('')
      setDate(todayString())
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
          <label>Date</label>
          <input
            type="date"
            value={date}
            max={todayString()}
            onChange={e => setDate(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Type</label>
          <select
            value={type}
            onChange={e => handleTypeChange(e.target.value as 'income' | 'expense')}
          >
            <option value="expense">Expense</option>
            <option value="income">Income</option>
          </select>
        </div>
        <div>
          <label>Category</label>
          <select value={category} onChange={e => setCategory(e.target.value)}>
            {CATEGORIES[type].map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
        {category === 'Other' && (
          <div>
            <label>Custom category</label>
            <input
              value={customCategory}
              onChange={e => setCustomCategory(e.target.value)}
              placeholder="e.g. Pet care"
              required
            />
          </div>
        )}
        <div>
          <label>Amount</label>
          <input
            type="number"
            step="0.01"
            min="0.01"
            value={amount}
            onChange={e => setAmount(e.target.value)}
            required
          />
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
