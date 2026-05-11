import { useState } from "react";
import CheckList from "./CheckList";

function Search({isRegistration}) {
    const [text,setText]=useState("")
    const [documents,setDocuments]=useState([])
    const [isChecked,setIsChecked]=useState([])
    const [needOnlyTextOfThisUser,setNeedOnlyTextOfThisUser]=useState(false)

    const getContext= async ()=>{
        const query=await fetch("http://localhost:8000/query",{
            method:"POST",
            credentials: "include",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                query:text,
                topics:isChecked,
                only_text_of_user:needOnlyTextOfThisUser
            })
        })
        const json=await query.json()
        console.log(json)
        setDocuments(json)
    }

    return (
        <div className="conteiner">
            <div className="control">
                <input onChange={e=>setText(e.target.value)} placeholder="Search..."/>
                <button onClick={getContext}>Search</button>
            </div>
            {isRegistration && <button className="btn_change_search" onClick={()=>setNeedOnlyTextOfThisUser(!needOnlyTextOfThisUser)}>{!needOnlyTextOfThisUser?"Search in all documnts":"Search in only documents of user"}</button>}
            <CheckList isChecked={isChecked} setIsChecked={setIsChecked} needOnlyTextOfThisUser={needOnlyTextOfThisUser}/>
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