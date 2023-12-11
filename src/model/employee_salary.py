from sqlalchemy import Column,Integer,TIMESTAMP,Date
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class EmployeeSalary(Base):
    __tablename__="employee_salary"
    __table_args__={"schema":"practice"}

    id=Column("id",Integer,nullable=False,primary_key=True,autoincrement=True)
    employee_id=Column("employee_id",Integer,nullable=False)
    employer_id=Column("employer_id",Integer,nullable=False)
    year=Column("salary_year",Date,nullable=False)
    month=Column("mt",Integer,nullable=False)
    salary=Column("salary_amt",Integer,nullable=False)