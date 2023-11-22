from sqlalchemy import Column,Integer,String,TIMESTAMP,func
from sqlalchemy.ext.declarative import declarative_base


Base=declarative_base()
    
class Employee(Base):
    __tablename__='employee'
    __table_args__={'schema':'practice'}

    employee_id=Column('employee_id',Integer,nullable=False,primary_key=True,autoincrement=True)
    employee_name=Column('employee_name',String,nullable=False)
    employee_email=Column("email",String,nullable=False)
    password=Column("password",String,nullable=False)
    joined_time=Column('joined_time',TIMESTAMP,nullable=False,server_default=func.now())


    