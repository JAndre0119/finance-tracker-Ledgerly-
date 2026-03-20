# Ledgerly

A personal finance tracker. Built with a Flask REST API backend and a React + TypeScript frontend.

## Stack

**Backend**
- Python / Flask
- Flask-Login (session-based auth) + Flask-Bcrypt (password hashing)
- Flask-SQLAlchemy + SQLite
- Flask-Cors

**Frontend**
- React 18 + TypeScript
- Vite
- React Router v6

## Project Structure

```
finance-tracker-Ledgerly-/
├── backend/
│   ├── app/
│   │   ├── __init__.py        # App factory
│   │   ├── extensions.py      # db, login_manager, bcrypt
│   │   ├── models.py          # User, Transaction models
│   │   └── routes/
│   │       ├── auth.py        # /api/auth/*
│   │       └── transactions.py # /api/transactions
│   ├── run.py
│   ├── requirements.txt
│   └── .env
└── frontend/
    ├── src/
    │   ├── api/client.ts      # Typed fetch wrapper
    │   ├── pages/             # LoginPage, RegisterPage, DashboardPage
    │   └── components/        # TransactionForm, TransactionList
    ├── vite.config.ts
    └── package.json
```

## API Endpoints

| Method | Path | Auth required | Description |
|--------|------|:---:|---|
| POST | `/api/auth/register` | | Create account |
| POST | `/api/auth/login` | | Log in |
| POST | `/api/auth/logout` | ✓ | Log out |
| GET | `/api/auth/me` | | Current user (or 401) |
| GET | `/api/transactions` | ✓ | List transactions + summary |
| POST | `/api/transactions` | ✓ | Add transaction |
| DELETE | `/api/transactions/<id>` | ✓ | Delete transaction |

## Running Locally

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/Scripts/activate   # Git Bash / WSL
# or: source venv/bin/activate  # macOS / Linux

pip install -r requirements.txt
python run.py
# Runs on http://localhost:5000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

Open `http://localhost:5173`. In development, Vite proxies all `/api/*` requests to the Flask server on port 5000.
