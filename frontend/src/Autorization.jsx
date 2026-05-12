import { useContext, useState } from "react"
import { RegistrationContext } from "./scripts/context"
import { useNavigate,Link } from "react-router"

export default function Autorization(){
    const [username,setUsername]=useState("")
    const [password,setPassword]=useState("")
    const [responce,setResponce]=useState({})
    const {isRegistration,setIsRegistration}=useContext(RegistrationContext)
    const navigate=useNavigate()


    const submmit=(e)=>{
        console.log(e)
        e.preventDefault();
        (async()=>{
            const query=await fetch("http://localhost:8000/autorization",{
                method:"POST",
                credentials: "include",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    user_name:username,
                    password
                })
            })
            const result=await query.json()
            console.log(setIsRegistration)
            if(result?.ok){
                setIsRegistration(true)
                navigate("/add")
            }
            setResponce(result)
        })()
    }
    return(
        <div className="conteiner">
            <form action="" className="control inputs" onSubmit={submmit}>
                <input type="text" placeholder="username..." onChange={e=>setUsername(e.target.value)}/>
                <input type="password" placeholder="password..." onChange={e=>setPassword(e.target.value)}/>
                <button>Sign in</button>
                <Link to="/registration" className="link">Sign up</Link>
            </form>
            {(Object.keys(responce).length!=0 && !responce?.ok) && <p className={responce?.ok?"msg":"msg msg-error"}>{responce?.msg}</p>}
        </div>
    )
}