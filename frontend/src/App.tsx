import { useState } from 'react'
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'

import './App.css'
import Home from './pages/Home'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </>
  )
}

export default App
