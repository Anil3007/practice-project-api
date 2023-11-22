from sqlalchemy import Column,Integer
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class EmployeeEmployer(Base):
    __tablename__="employee_employer"
    __table_args__={"schema":"practice"}

    id=Column("id",Integer,nullable=False,primary_key=True)
    employee_id=Column("employee_id",Integer,nullable=False)
    employer_id=Column("employer_id",Integer,nullable=False)

    