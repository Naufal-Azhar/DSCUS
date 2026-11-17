import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import DecisionInputPage from './pages/DecisionInputPage'
import DecisionWorkspacePage from './pages/DecisionWorkspacePage'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/new" element={<DecisionInputPage />} />
          <Route path="/decision/:id" element={<DecisionWorkspacePage />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
