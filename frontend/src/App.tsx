import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { api, User } from './api/client'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'

function App() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.auth
      .me()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div>Loading...</div>

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            user
              ? <DashboardPage user={user} onLogout={() => setUser(null)} />
              : <Navigate to="/login" replace />
          }
        />
        <Route
          path="/login"
          element={user ? <Navigate to="/" replace /> : <LoginPage onLogin={setUser} />}
        />
        <Route
          path="/register"
          element={user ? <Navigate to="/" replace /> : <RegisterPage onRegister={setUser} />}
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App
