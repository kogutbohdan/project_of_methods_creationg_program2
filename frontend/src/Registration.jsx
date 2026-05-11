import { useState } from "react";
import { Link } from "react-router";
import { useNavigate } from "react-router";


export default function Registration(){

    const [username,setUsername]=useState("")
    const [password,setPassword]=useState("")
    const [email,setEmail]=useState("")
    const [responce,setResponce]=useState({})
    const navigate=useNavigate()

    const submmit=(e)=>{
        e.preventDefault();
        (async()=>{
            const query=await fetch("http://localhost:8000/registration",{
                method:"POST",
                credentials: "include",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    user_name:username,
                    password,
                    email
                })
            })
            let result=await query.json()
            if (result?.ok){
                navigate("/indentification")
            }
            setResponce(result)
        })()
    }
    console.log((Object.keys(responce).length!=0 && responce?.ok))
    return (
        <div className="conteiner">
            <form className="control inputs" onSubmit={submmit}>
                <input type="text" placeholder="email..." onChange={e=>setEmail(e.target.value)}/>
                <input type="text" placeholder="username..." onChange={e=>setUsername(e.target.value)}/>
                <input type="password" placeholder="password..." onChange={e=>setPassword(e.target.value)}/>
                <button>Sign up</button>
                <Link to="/autorization" className="link">Sign up</Link>
            </form>
            {(Object.keys(responce).length!=0 && !responce?.ok) && <p className={responce?.ok?"msg":"msg msg-error"}>{responce?.msg}</p>}
        </div>
    )
}