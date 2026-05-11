import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Search from './Search.jsx'
import AddFile from './AddFile.jsx'
import Registration from './Registration.jsx'
import Autorization from './Autorization.jsx'
import Indentefication from './Indentefication.jsx'
import {BrowserRouter,Routes,Route,Link} from "react-router-dom"
import './App.css'
import { RegistrationContext } from './scripts/context.js'

function App() {
  const [isRegistration,setIsRegistration]=useState(false)
  useEffect(()=>{
    (async()=>{
        const query=await fetch("http://localhost:8000/me",{
          credentials: "include"
        })
        let result=await query.json()
        setIsRegistration(result?.ok)
    })()
  },[isRegistration])

  const exit=()=>{
    (async()=>{
      const query=await fetch("http://localhost:8000/logout",{
        method:"DELETE",
        credentials: "include"
      })
      let result=await query.json()
      if(result?.ok) setIsRegistration(false)
    })()
  }
  return (
    <RegistrationContext.Provider value={{isRegistration,setIsRegistration}}>
      <BrowserRouter>
        <nav>
          <div className="links">
            <Link to="" className="link">Search</Link>
            <Link to="/add" className="link">Add file</Link>
            {!isRegistration && <Link to="/registration" className="link">Registration</Link>}
          </div>
          {isRegistration && <button onClick={exit}>exit</button>}
        </nav>
        <Routes>
          <Route path="" element={<Search isRegistration={isRegistration}/>}/>
          <Route path="/add" element={<AddFile/>}/>
          {!isRegistration &&(<>
            <Route path="/registration" element={<Registration/>}/>
            <Route path="/autorization" element={<Autorization/> }/>
            <Route path="/indentification" element={<Indentefication/>}/>
          </>)}
        </Routes>
      </BrowserRouter>
    </RegistrationContext.Provider>
  )
}

export default App
