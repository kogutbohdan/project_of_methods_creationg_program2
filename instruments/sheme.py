from pydantic import BaseModel,EmailStr
from typing import List

class QuerySheme(BaseModel):
    query:str
    topics:List[str]
    only_text_of_user:bool

class AddFileSheme(BaseModel):
    query:str
    topic:str

class UsserInfo(BaseModel):
    user_name:str
    password:str
    email:EmailStr

class Indentification(BaseModel):
    code:str

class UserInfoAuth(BaseModel):
    user_name:str
    password:str

class ChunckInfo(BaseModel):
    id:int

class ShareInfo(BaseModel):
    id:int
    user_name:str