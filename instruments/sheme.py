from pydantic import BaseModel
from typing import List

class QuerySheme(BaseModel):
    query:str
    topics:List[str]

class AddFileSheme(BaseModel):
    query:str
    topic:str