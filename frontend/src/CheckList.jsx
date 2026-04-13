import { useEffect, useState } from "react"

export default function CheckList({isChecked,setIsChecked}){
    const [topics,setTopics]=useState([])
    const [textFind,setTextFind]=useState("")
    const [active,setActive]=useState(false)

    const random=(topics)=>topics[Math.floor(Math.random()*topics.length)]

    useEffect(()=>{
        (async ()=>{
            const topic_query=await fetch("http://localhost:8000/topics")
            let res=await topic_query.json()
            setTopics(res)
            setIsChecked([random(res)])
        })()
    },[])


    useEffect(()=>{
        if(isChecked.length===0){
            let random_topic=random(topics)
            if(random_topic) setIsChecked([random_topic])
        }
    },[isChecked])

    const stopPropagation=e=>{
        if(active) e.stopPropagation()
    }

    return(
        <div className="list" onClick={e=>setActive(!active)}>
            <input type="text" onClick={stopPropagation} onChange={e=>setTextFind(e.target.value)}/>
            {topics.map(elem=>{
                if(elem.includes(textFind) || !textFind) return (<label key={elem} className={`checkbox ${active?"active_checkbox":""}`}>
                    <input type="checkbox" checked={isChecked.includes(elem)} onClick={stopPropagation} onChange={e=>{
                        if(!isChecked.includes(elem)){
                            setIsChecked([...isChecked,elem])
                        }else{
                            setIsChecked(isChecked.filter(checked=>(checked!=elem)))
                        }
                    }}/>
                    {elem}
                </label>)
            })}
        </div>
    )
}