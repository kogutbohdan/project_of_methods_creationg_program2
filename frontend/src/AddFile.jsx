import { useState } from "react"

function AddFile() {
    const [text,setText]=useState("")

    const addFile=async ()=>{
        const url=await fetch("http://localhost:3000/file",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
               query:text 
            })
        })
        console.log(await url.json())
    }
    return ( 
        <div className="conteiner">
         <div className="control">
             <input type="text" onChange={e=>setText(e.target.value)}/>
             <button onClick={addFile}>add</button>
         </div>
        </div> 
    );
}

export default AddFile;