import { useState } from "react";

function Search() {
    const [text,setText]=useState("")
    const [documents,setDocuments]=useState([])

    const getContext= async ()=>{
        const query=await fetch("http://localhost:8000/query",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                query:text
            })
        })
        const json=await query.json()
        console.log(json)
        setDocuments(json)
    }
    return (
        <div className="conteiner">
            <div className="control">
                <input onChange={e=>setText(e.target.value)}/>
                <button onClick={getContext}>Search</button>
            </div>
            <div className="rusults">
                {documents.map(element=>(
                    <div className="result">
                        <a href={element["url"]} className="search__link">{element["name"]}</a>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Search;