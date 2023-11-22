from src.model import employee
from sqlalchemy import text
import json
from sqlalchemy import and_


def get_all_employee_details(connection):
    res=connection.query(employee.Employee.employee_id,employee.Employee.employee_name).all()
    data=[]

    for row in res:
        data.append({
            "employee_id":row.employee_id,
            "employee_name":row.employee_name
        })
    return data

def add_new_employee(connection,employee_name,pw_hash,employee_email):
    add_obj=employee.Employee(employee_name=employee_name,password=pw_hash,employee_email=employee_email)
    connection.add(add_obj)
    connection.commit()

    return {"id":str(add_obj.joined_time)}


    
def delete_employee(connection,employee_id):
    del_obj=connection.query(employee.Employee).filter(employee.Employee.employee_id==employee_id).first()
    connection.delete(del_obj)
    connection.commit()
    
    return {"id":del_obj.employee_id}
    
    
def     get_employee_details(connection,employee_name):
    obj=connection.query(employee.Employee.employee_id,employee.Employee.employee_name,employee.Employee.employee_email,employee.Employee.password).filter(employee.Employee.employee_name==employee_name).first()

    print(obj)
    if obj!=None:
        return {
            "employee_id":obj.employee_id,
            "employee_name":obj.employee_name,
            "employee_pw_hash":obj.password
        }
    return None
    
        
    
def get_particular_employee_details(connection,employee_id):
    obj=connection.query(employee.Employee.employee_id,employee.Employee.employee_name,employee.Employee.employee_email).filter(employee.Employee.employee_id==employee_id).first()

    print(obj)
    if obj!=None:
        return {
            "employee_id":obj.employee_id,
            "employee_name":obj.employee_name,
            "employee_email":obj.employee_email
        }
    return None