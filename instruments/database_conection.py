import json
from .sql_database import*
from .faiss_database import do_search
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

            chuncks=None
            with open("/home/lenovo/Документи/backend/instruments/json/chunck.json","r") as r_file:
                chuncks=json.load(r_file)

            with open("/home/lenovo/Документи/backend/instruments/json/chunck.json","w") as w_file:
                print(groups[key]["vector"].tolist())
                chuncks.append({"id":chunck.id,"vector":groups[key]["vector"].tolist()[0]})
                w_file.write(json.dumps(chuncks))
            sentences=None
            with open("/home/lenovo/Документи/backend/instruments/json/sentence.json","r") as r_file:
                sentences=json.load(r_file)

            with open("/home/lenovo/Документи/backend/instruments/json/sentence.json","w") as w_file:
                for id,vector in zip(ids,groups[key]["texts"]):
                    sentences.append({"id":id,"vector":vector.tolist()})
                w_file.write(json.dumps(sentences))
            self.session.commit()
    
    def search(self,vector,topics,only_text_of_user):
        user_documents_id=None
        user_id=self.request.session.get("user_id")
        if only_text_of_user and user_id:
            user_relations=self.session.query(user_relation).filter(user_relation.c.user_id==user_id).all()
            user_documents_id=[relation.chunck_id for relation in user_relations]
        chuncks=None
        with open("/home/lenovo/Документи/backend/instruments/json/chunck.json","r") as file:
            chuncks=json.load(file)
            if not (user_documents_id is None):
                chuncks=list(filter((lambda elem:elem["id"] in user_documents_id),chuncks))
        ids=do_search(vector,chuncks)
        sentence_ids=[id for (id,) in self.session.query(Sentence.id).join(Sentence.chunck).filter(Chunck.id.in_(ids),
                                                                                                   Chunck.topic.in_(topics)).all()]
        print(sentence_ids)
        sentences=None
        with open("/home/lenovo/Документи/backend/instruments/json/sentence.json","r") as file:
            load_file=json.load(file)
            sentences=list(filter((lambda elem:elem["id"] in sentence_ids),load_file))
        
        print("sents",sentences)
        result_sentence_ids=do_search(vector,sentences)
        print(result_sentence_ids)
        result_sentences=self.session.query(Sentence).filter(Sentence.id.in_(result_sentence_ids)).all()
        return result_sentences
    
    def delete(self,id):
        chunck_query=self.session.query(Chunck).filter(Chunck.id==id)
        chunck=chunck_query.first()
        chuncks=None
        with open("/home/lenovo/Документи/backend/instruments/json/chunck.json","r") as r_file:
            chuncks=json.load(r_file)

        with open("/home/lenovo/Документи/backend/instruments/json/chunck.json","w") as w_file:
            chuncks=list(filter(lambda elem:elem["id"]!=chunck.id))
            w_file.write(json.dumps(chuncks))

        sentences=None
        with open("/home/lenovo/Документи/backend/instruments/json/sentence.json","r") as r_file:
            sentences=json.load(r_file)

        with open("/home/lenovo/Документи/backend/instruments/json/sentence.json","w") as w_file:
            for sentence in chunck.sentences:
                self.session.delete(sentence)
                sentences=list(filter(lambda elem:elem["id"]!=chunck.id))
                w_file.write(json.dumps(sentences))
        chunck_query.delete()
    
    def clear(self):
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM user_relation"))
            conn.execute(text("DELETE FROM sentences"))
            conn.execute(text("DELETE FROM chuncks"))
            with open("/home/lenovo/Документи/backend/instruments/json/sentence.json","w") as w_file:
                w_file.write("[]")
            with open("/home/lenovo/Документи/backend/instruments/json/chunck.json","w") as w_file:
                w_file.write("[]")
            conn.commit()
        
        