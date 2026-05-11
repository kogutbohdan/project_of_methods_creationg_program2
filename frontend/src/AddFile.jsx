import { useState } from "react"
import ChunckList from "./ChunckList"

function AddFile() {
    const [text,setText]=useState("")
    const [topic,setTopic]=useState("")
    const [responce,setResponce]=useState()


    const addFile=async ()=>{
        setResponce({})
        const url=await fetch("http://localhost:8000/file",{
            method:"POST",
            credentials: "include",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
               query:text,
               topic:topic 
            })
        })
        setResponce(await url.json())
    }
    return ( 
        <div className="conteiner">
         <div className="control">
             <div className="inputs">
                <input type="text" onChange={e=>setText(e.target.value)} placeholder="enter URL..."/>
                <input type="text" onChange={e=>setTopic(e.target.value)} placeholder="enter topic..."/>
             </div>
             <button onClick={addFile}>add</button>
         </div>
         {responce && Object.keys(responce).length!==0?
         <p className={responce?.ok?"msg":"msg msg-error"}>{responce?.msg}</p>
         :responce && <div className="loader"/>}
         <ChunckList responce={responce}/>
        </div> 
    );
}

export default AddFile;