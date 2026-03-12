import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Search from './Search.jsx'
import AddFile from './AddFile.jsx'
import {BrowserRouter,Routes,Route,Link} from "react-router-dom"
import './App.css'

function App() {

  return (
    <BrowserRouter>
      <nav>
        <Link to="" className="link">Search</Link>
        <Link to="/add" className="link">Add file</Link>
      </nav>
      <Routes>
        <Route path="" element={<Search/>}/>
        <Route path="/add" element={<AddFile/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
