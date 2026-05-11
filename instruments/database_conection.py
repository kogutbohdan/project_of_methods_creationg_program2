from .milvus_database import*
from .sql_database import*
from sqlalchemy import text

class Connect:
    def __init__(self,session=None,request=None):
        self.session=session
        self.request=request

    def add(self,groups,url,topic):
        for key in groups:
            name_chunck=key[0:17]+"..."
            chunck=Chunck(name=name_chunck,url=url,topic=topic)
            for path,name in zip(groups[key]["urls"],groups[key]["names"]):
                chunck.sentences.append(Sentence(url=path,name=name))
            if self.request:
                user_id=self.request.session.get("user_id")
                print("id_user",user_id)
                print(10)
                if user_id:
                    user=self.session.query(User).filter(User.id==user_id).first()
                    chunck.users.append(user)
            self.session.add(chunck)
            self.session.flush()
            ids=[sentence.id for sentence in chunck.sentences]
            res=collection_chunks.insert([[chunck.id],[groups[key]["vector"]]])
            res2=collection_sentences.insert([ids,groups[key]["texts"]])
            self.session.commit()
            collection_chunks.load()
            collection_sentences.load()
    
    def search(self,vector,topics,only_text_of_user):
        param_search={
            "metric_type":"IP",
            "params":{"ef":64}
        }
        user_documents_id=None
        user_id=self.request.session.get("user_id")
        if only_text_of_user and user_id:
            user_relations=self.session.query(user_relation).filter(user_relation.c.user_id==user_id).all()
            user_documents_id=[relation.chunck_id for relation in user_relations]
        print("user_documents_id:",user_documents_id)
        print("only_text_of_user:",only_text_of_user)
        print("user_id:",self.request.session.get("user_id"))
        result=collection_chunks.search(vector,"vector",param_search,5,output_fields=["id"],expr=(f"id in {user_documents_id}" if not (user_documents_id is None) else "id>-1"))
        ids=[res.id for res in result[0]]
        sentence_ids=[id for (id,) in self.session.query(Sentence.id).join(Sentence.chunck).filter(Chunck.id.in_(ids),
                                                                                                   Chunck.topic.in_(topics)).all()]
        
        result2=collection_sentences.search(vector,"vector",param_search,10,output_fields=["id"],expr=f"id in {sentence_ids}")
        result_sentence_ids=[res.id for res in result2[0]]
        result_sentences=self.session.query(Sentence).filter(Sentence.id.in_(result_sentence_ids)).all()
        return result_sentences
    
    def delete(self,id):
        chunck_query=self.session.query(Chunck).filter(Chunck.id==id)
        chunck=chunck_query.first()
        collection_chunks.delete(expr=f"id=={chunck.id}")
        for sentence in chunck.sentences:
            self.session.delete(sentence)
            collection_sentences.delete(expr=f"id=={sentence.id}")
        chunck_query.delete()
    
    def clear(self):
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM sentences"))
            conn.execute(text("DELETE FROM chuncks"))
            conn.commit()
            collection_chunks.drop()
            collection_sentences.drop()
        
        