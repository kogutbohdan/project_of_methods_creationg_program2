import { useContext, useState } from "react"
import { useNavigate } from "react-router";
import { RegistrationContext } from "./scripts/context";

export default function Indentefication(){
    const [code,setCode]=useState("")
    const {isRegistration,setIsRegistration}=useContext(RegistrationContext)
    const navigate=useNavigate()

    const submmit=e=>{
        e.preventDefault();
        (async ()=>{
            const query=await fetch("http://localhost:8000/indentefication",{
                method:"POST",
                credentials: "include",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    code
                })
            })
            let result=await query.json()
            if(result?.ok){
                setIsRegistration(true)
                navigate("/add")
            }else{
                navigate("/registration")
            }
        })()
    }
    return(
        <div className="conteiner">
            <form action="" onSubmit={submmit} className="control code">
                <input type="number" value={code} onChange={e=>{
                    let text=e.target.value
                    if(text.length<=6) setCode(text) 
                }}/>
                <button>Send</button>
            </form>
        </div>
    )
}