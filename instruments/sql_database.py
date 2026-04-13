from sqlalchemy import create_engine,Column,Integer,BigInteger,String,ForeignKey
from sqlalchemy.orm import declarative_base,relationship,sessionmaker

Base=declarative_base()

engine=create_engine("mysql+pymysql://root:Singular_2026!@localhost/searchdb")

class Chunck(Base):
    __tablename__="chuncks"
    id=Column(Integer,primary_key=True,autoincrement=True)
    url=Column(String(2000))
    topic=Column(String(20))
    sentences=relationship("Sentence",back_populates="chunck")

class Sentence(Base):
    __tablename__="sentences"
    id=Column(Integer,primary_key=True,autoincrement=True)
    url=Column(String(2000))
    name=Column(String(5000))
    chunck_id=Column(Integer,ForeignKey("chuncks.id"))
    chunck=relationship("Chunck",back_populates="sentences")


Session=sessionmaker(bind=engine)
def get_db():
    session=Session()
    try:
        yield session
    finally:
        session.close()


