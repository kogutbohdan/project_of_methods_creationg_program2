import { useState } from "react"

function AddFile() {
    const [text,setText]=useState("")
    const [topic,setTopic]=useState("")

    const addFile=async ()=>{
        const url=await fetch("http://localhost:8000/file",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
               query:text,
               topic:topic 
            })
        })
        console.log(await url.json())
    }
    return ( 
        <div className="conteiner">
         <div className="control">
             <div className="inputs">
                <input type="text" onChange={e=>setText(e.target.value)}/>
                <input type="text" onChange={e=>setTopic(e.target.value)}/>
             </div>
             <button onClick={addFile}>add</button>
         </div>
        </div> 
    );
}

export default AddFile;