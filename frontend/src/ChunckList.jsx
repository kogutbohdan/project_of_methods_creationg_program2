import { useEffect,useState } from "react"
import Window from "./Window"

export default function ChunckList({responce}){
    const [chuncks,setChuncks]=useState([])
    const [isShow,setIsShow]=useState(false)
    const [id,setId]=useState(null)

    useEffect(()=>{
        (async ()=>{
            const chunck_query=await fetch("http://localhost:8000/chuncks",{
                credentials: "include"
            })
            let res=await chunck_query.json()
            setChuncks(res)
            console.log(res)
        })()
    },[responce])

    const deleteChunck = id=>()=>{
        setChuncks(chuncks.filter(elem=>elem!=id));
        (async ()=>{
            const delete_query=await fetch("http://localhost:8000/chuncks",{
                method:"DELETE",
                credentials: "include",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({id})
            })
            console.log(await delete_query.json())
        })()
    }

    const showWindow=id=>()=>{
        setIsShow(true)
        setId(id)
    }
    return(<>
        {isShow && <Window setIsShow={setIsShow} id={id}/>}
        {chuncks.map((elem)=>{
            return (
                <div className="chunck control" key={elem.id}>
                    <p>{elem.name}</p>
                    <div className="btns">
                        <button onClick={deleteChunck(elem.id)}>delete</button>
                        <button onClick={showWindow(elem.id)}>share</button>
                    </div>
                </div>
            )
        })}
    </>
    )
}