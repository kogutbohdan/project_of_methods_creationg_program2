from sqlalchemy import create_engine,Column,Integer,BigInteger,String,ForeignKey,Table
from sqlalchemy.orm import declarative_base,relationship,sessionmaker

Base=declarative_base()

engine=create_engine("mysql+pymysql://root:Singular_2026!@localhost/searchdb")

class UserMixin:
    id=Column(Integer,primary_key=True,autoincrement=True)
    password=Column(String(255),nullable=False)

user_relation=Table(
    "user_relation",Base.metadata,
    Column("user_id",ForeignKey("users.id"),primary_key=True),
    Column("chunck_id",ForeignKey("chuncks.id"),primary_key=True)
)

class User(Base,UserMixin):
    __tablename__="users"
    username=Column(String(255),nullable=False,unique=True)
    email=Column(String(255),nullable=False,unique=True)
    chuncks=relationship("Chunck",secondary=user_relation,
                         back_populates="users")

class UserBeforeIndentefication(Base,UserMixin):
    __tablename__="users_before_indentefication"
    username=Column(String(255),nullable=False)
    email=Column(String(255),nullable=False)
    code=Column(String(6),nullable=False)



class Chunck(Base):
    __tablename__="chuncks"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(20))
    url=Column(String(2000))
    topic=Column(String(20))
    sentences=relationship("Sentence",back_populates="chunck")
    users=relationship("User",secondary=user_relation,
                       back_populates="chuncks")

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
    except:
        session.rollback()
        raise
    finally:
        session.close()


