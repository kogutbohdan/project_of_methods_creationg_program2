from fastapi import FastAPI,Query,Request,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import requests as req
from instruments.read_files import FileReader,normalize
from instruments.sheme import*
from instruments.global_variables import sentens_transformer
from instruments.functions import urlnormilize
from instruments.database_conection import Connect 
from instruments.sql_database import get_db,Chunck,UserBeforeIndentefication,User,user_relation
from instruments.send_massege import send_massage
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from random import randint
from bs4 import BeautifulSoup

app = FastAPI()
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

app.add_middleware(SessionMiddleware,secret_key="super-secret-key")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates=Jinja2Templates("./instruments/html")

@app.get("/")
def render(request: Request,url:str=Query("")):
    site=req.get(url,headers={
        "User-Agent": "Mozilla/5.0"
    })

    soup=BeautifulSoup(site.content,"html.parser")
    html_body=soup.body.decode_contents()

    return templates.TemplateResponse("index.html",{"request":request,"html_body":html_body})

@app.post("/query")
def complete_query(request:Request,data:QuerySheme,session:Session=Depends(get_db)):
    query_embedding=normalize(sentens_transformer.encode([data.query]))
    database=Connect(session,request)
    results=database.search(query_embedding,data.topics,data.only_text_of_user)

    response=[]
    for item in results:
        response.append({
            "id":item.id,
            "url":item.url,
            "name":item.name if len(item.name)<=100 else item.name[0:100]+"..."
        })

    print(response)
    return response

@app.post("/file")
def add_file(request:Request,path_file:AddFileSheme,session:Session=Depends(get_db)):
    try:
        url=urlnormilize(path_file.query)
        if session.query(Chunck).filter(Chunck.url==url).all():
            return {"ok":False,"msg":"Такий файл вже є"}
        file=req.get(url,headers={
            "User-Agent": "Mozilla/5.0"
        })
        content_type = file.headers.get("Content-Type")
        reader=FileReader()
        groups=reader.get_embedding(content_type=content_type.lower(),url=url,file=file)
        database=Connect(session,request)
        database.add(groups,url,path_file.topic)
        return {"ok":True,"msg":"Данні успішно збережені"}
    except Exception as e:
        print(e)
        return {"ok":False,"msg":"Упс щось пішло не так"}
    
@app.get("/topics")
def get_topic(only:bool,request:Request,session:Session=Depends(get_db)):
    user_id=request.session.get("user_id")
    if only and user_id:
        relations=session.query(user_relation.c.chunck_id).filter(user_relation.c.user_id==user_id).all()
        ids=[chunck_id for (chunck_id,) in relations]
        result=session.query(Chunck.topic).filter(Chunck.id.in_(ids)).distinct().all()
    else:result=session.query(Chunck.topic).distinct().all()
    return [topic for (topic,) in result]

@app.post("/registration")
def registration(request:Request,user_info:UsserInfo,session:Session=Depends(get_db)):
    try:
        print(user_info.password)
        if session.query(User).filter(User.email==user_info.email).first():
            return {"ok":False,"msg":"Такий email вже є"}
        if session.query(User).filter(User.username==user_info.user_name).first():
            return {"ok":False,"msg":"Такий username вже є"}
        if len(user_info.password)<5:
            return {"ok":False,"msg":"Пароль за короткий"}
        password=pwd_context.hash(user_info.password)
        code="".join([str(randint(0,9)) for i in range(6)])
        send_massage(f"Ваш код для верефікації:{code}","Код для верефікації",user_info.email)
        user=UserBeforeIndentefication(email=user_info.email,password=password,username=user_info.user_name,code=code)
        session.add(user)
        session.commit()
        request.session["new_user_id"]=user.id
        return {"ok":True}
    except Exception as e:
        print(e)
        return {"ok":False,"msg":"Щось пішло не так"}


@app.post("/indentefication")
def indentefication(request:Request,indentify:Indentification,session:Session=Depends(get_db)):
    new_user=session.query(UserBeforeIndentefication).filter(UserBeforeIndentefication.id==request.session.get("new_user_id")).first()
    if new_user:
        if indentify.code==new_user.code:
            user=User(username=new_user.username,email=new_user.email,password=new_user.password)
            session.add(user)
            session.delete(new_user)
            del request.session["new_user_id"]
            session.commit()
            request.session["user_id"]=user.id
            return {"ok":True}
        del request.session["new_user_id"]
        session.delete(new_user)
        session.commit()
        return {"ok":False,"msg":"Неправильний код"}
    return {"ok":False,"msg":"Щось пішло не так"}

@app.delete("/user_before_indentification")
def delete_new_user(request:Request,session:Session=Depends(get_db)):
    new_user=session.query(UserBeforeIndentefication).filter(UserBeforeIndentefication.id==request.session.get("new_user_id")).first()
    session.delete(new_user)
    session.commit()
    del request.session["new_user_id"]
    return {"ok":True}

@app.post("/autorization")
def autorization(request:Request,user_info:UserInfoAuth,session:Session=Depends(get_db)):
    user=session.query(User).filter(User.username==user_info.user_name).first()
    if user and pwd_context.verify(user_info.password,user.password):
        request.session["user_id"]=user.id
        return {"ok":True}
    return {"ok":False,"msg":"Ви непровильно ввели пароль або username"}

@app.get("/chuncks")
def get_chuncks(request:Request,session:Session=Depends(get_db)):
    user_id=request.session.get("user_id")
    print(user_id)
    if user_id:
        user=session.query(User).filter(User.id==user_id).first()
        return [{"id":chunck.id,"name":chunck.name} for chunck in user.chuncks]
    return []

@app.delete("/chuncks")
def delete_chunck(request:Request,chunck_info:ChunckInfo,session:Session=Depends(get_db)):
    user_id=request.session.get("user_id")
    if user_id:
        results=session.query(user_relation).filter(user_relation.c.user_id==user_id,
                                        user_relation.c.chunck_id==chunck_info.id)
        if results.all():
            results.delete()
            Connect(session,request).delete(chunck_info.id)
            session.commit()
            return {"ok":True}
        
    return {"ok":False}


@app.get("/me")
def is_user(request:Request):
    return {"ok":bool(request.session.get("user_id"))}

@app.delete("/logout")
def exit(request:Request):
    if request.session.get("user_id"):
        del request.session["user_id"]
        return {"ok":True}
    return {"ok":False}

@app.post("/share")
def share(shair_info:ShareInfo,request:Request,session:Session=Depends(get_db)):
    user_id=request.session.get("user_id")
    if user_id and session.query(user_relation).filter(user_relation.c.user_id==user_id,user_relation.c.chunck_id==shair_info.id).all():
        user=session.query(User).filter(User.username==shair_info.user_name).first()
        chunck=session.query(Chunck).filter(Chunck.id==shair_info.id).first()

        is_reletion=session.query(user_relation).filter(user_relation.c.user_id==user.id,user_relation.c.chunck_id==shair_info.id).all()
        if user and chunck and not is_reletion:
            user.chuncks.append(chunck)
            send_massage("Вам надали доступ до документу",f"від користувача {user.username}",user.email)
            session.commit()
            return {"ok":True}
        if is_reletion:
            return {"ok":False,"msg":"Цей юзер вже має цей документ"}
        return {"ok":False,"msg":"Нема такого"}
    return {"ok":False}


@app.get("/users")
def get_users(request:Request,session:Session=Depends(get_db)):
    user_id=request.session.get("user_id")
    if user_id:
        return {"ok":True,
                "users":[name for (name,) in session.query(User.username).filter(User.id!=user_id).all()]}
    return {"ok":False}