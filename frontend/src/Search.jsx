import { useState } from "react";
import CheckList from "./CheckList";

function Search() {
    const [text,setText]=useState("")
    const [documents,setDocuments]=useState([])
    const [isChecked,setIsChecked]=useState([])

    const getContext= async ()=>{
        const query=await fetch("http://localhost:8000/query",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                query:text,
                topics:isChecked
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
            <CheckList isChecked={isChecked} setIsChecked={setIsChecked}/>
            <div className="rusults">
                {documents.map(element=>(
                    <div className="result" key={element["url"]}>
                        <a href={element["url"]} className="search__link">{element["name"]}</a>
                        <p>Звідки:{element["url"]}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Search;