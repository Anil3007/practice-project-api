from sqlalchemy import Column,Integer,String,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base


Base=declarative_base()

class Employer(Base):
    __tablename__='employer'
    __table_args__={'schema':'practice'}


    employer_id=Column('employer_id',Integer,nullable=False,primary_key=True)
    employer_name=Column('employer_name',String,nullable=False)


