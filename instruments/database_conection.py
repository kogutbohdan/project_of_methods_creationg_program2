from .milvus_database import*
from .sql_database import*
from sqlalchemy import text

class Connect:
    def __init__(self,session=None):
        self.session=session

    def add(self,groups,url,topic):
        for key in groups:
            chunck=Chunck(url=url,topic=topic)
            for path,name in zip(groups[key]["urls"],groups[key]["names"]):
                chunck.sentences.append(Sentence(url=path,name=name))
            self.session.add(chunck)
            self.session.flush()
            ids=[sentence.id for sentence in chunck.sentences]
            res=collection_chunks.insert([[chunck.id],[groups[key]["vector"]]])
            res2=collection_sentences.insert([ids,groups[key]["texts"]])
            self.session.commit()
            collection_chunks.load()
            collection_sentences.load()
    
    def search(self,vector,topics):
        param_search={
            "metric_type":"IP",
            "params":{"ef":64}
        }
        result=collection_chunks.search(vector,"vector",param_search,5,output_fields=["id"])
        ids=[res.id for res in result[0]]
        sentence_ids=[id for (id,) in self.session.query(Sentence.id).join(Sentence.chunck).filter(Chunck.id.in_(ids),
                                                                                                   Chunck.topic.in_(topics)).all()]
        
        result2=collection_sentences.search(vector,"vector",param_search,10,output_fields=["id"],expr=f"id in {sentence_ids}")
        result_sentence_ids=[res.id for res in result2[0]]
        result_sentences=self.session.query(Sentence).filter(Sentence.id.in_(result_sentence_ids)).all()
        return result_sentences
    
    def clear(self):
        with engine.connect() as conn:
            conn.execute(text("TRUNCATE TABLE chuncks CASCADE"))
            conn.commit()
            collection_chunks.drop()
            collection_sentences.drop()
        
        