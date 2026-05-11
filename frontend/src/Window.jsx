import { useEffect, useState } from "react"

export default function Window({setIsShow,id}){
    const [user_name,setUsername]=useState("")
    const [error,setError]=useState(null)
    const [namesOfUsers,setNamesOfUsers]=useState([])

    useEffect(()=>{
        (async ()=>{
            const query=await fetch("http://localhost:8000/users",{
                credentials: "include"
            })
            let result=await query.json()
            setNamesOfUsers(result?.users)
            console.log(result)
        })()
    },[])

    const cancle=()=>setIsShow(false)
    const ok=async ()=>{
        const query=await fetch("http://localhost:8000/share",{
            method:"POST",
            credentials: "include",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({id,user_name})
        })

        const result=await query.json()
        if(result?.ok){
            setIsShow(false)
        }
        setError(result?.msg)
    }
    return (
        <div className="background" onClick={cancle}>
            <div className="control" onClick={e=>e.stopPropagation()}>
                <input type="text" value={user_name} onChange={e=>setUsername(e.target.value)}/>
                <button onClick={ok}>Ok</button>
                <button onClick={cancle}>Cancle</button>
            </div>
            {error &&  <p className={"msg msg-error"}>{error}</p>}
            {namesOfUsers.map(name=>{
                if(user_name && name.includes(user_name)) return (<p className="name" key={name} onClick={e=>{
                    e.stopPropagation()
                    setUsername(e.target.textContent)
                }}>{name}</p>)
            })}
        </div>
    )
}