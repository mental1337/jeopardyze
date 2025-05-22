import { Route, Routes } from 'react-router-dom'

import './App.css'
import Home from './pages/Home'
import GameSession from './pages/GameSession'

function App() {

  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/play/:gameSessionId" element={<GameSession />} />
      </Routes>
    </>
  )
}

export default App
