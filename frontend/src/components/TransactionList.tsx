import { Transaction } from '../api/client'

interface Props {
  transactions: Transaction[]
  onDelete: (id: number) => Promise<void>
}

export default function TransactionList({ transactions, onDelete }: Props) {
  if (transactions.length === 0) return <p>No transactions yet.</p>

  return (
    <div>
      <h2>Transactions</h2>
      <ul>
        {transactions.map(t => (
          <li key={t.id}>
            <span>{t.transaction_date}</span>
            {' | '}
            <span>{t.category}</span>
            {' | '}
            <span style={{ color: t.type === 'income' ? 'green' : 'red' }}>
              {t.type === 'income' ? '+' : '-'}${t.amount.toFixed(2)}
            </span>
            {t.note && <span> ({t.note})</span>}
            {' '}
            <button onClick={() => onDelete(t.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
