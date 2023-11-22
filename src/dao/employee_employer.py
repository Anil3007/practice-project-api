from src.model import employee_employer,employee,employer
from sqlalchemy import and_,func


def subscribe_to_employer(connection,employee_id,employer_id):
    insert_obj=employee_employer.EmployeeEmployer(employee_id=employee_id,employer_id=employer_id)
    connection.add(insert_obj)
    connection.commit()
    return {"id":insert_obj.id}

def update_employer_details(connection,employee_id,old_employer_id,new_employer_id):
    update_obj=connection.query(employee_employer.EmployeeEmployer).filter(
        and_(
            employee_employer.EmployeeEmployer.employee_id==employee_id,
            employee_employer.EmployeeEmployer.employer_id==old_employer_id
        )
    ).first()

    if update_obj is not None:
        update_obj.employer_id=new_employer_id
        connection.commit()
        return True
    return False


def joining_two_tables(connection):
    obj=connection.query(employee_employer.EmployeeEmployer.employee_id,
                         employee_employer.EmployeeEmployer.employer_id,
                         employee.Employee.employee_name,employee.Employee.joined_time).join(
                             employee.Employee,employee_employer.EmployeeEmployer.employee_id==employee.Employee.employee_id
                             )
    data=[]

    for row in obj:
        data.append({
            "employee_name":row.employee_name,
            "employee_id":row.employee_id,
            "employer_id":row.employer_id,
            "joined_time":str(row.joined_time)
        })
    
    return data 

def get_details_of_three_joined_tables(connection):
    obj=connection.query(employee.Employee.employee_id,employee.Employee.employee_name,
                         employee.Employee.joined_time,
                         employer.Employer.employer_id,employer.Employer.employer_name).join(employee_employer.EmployeeEmployer,employee.Employee.employee_id==employee_employer.EmployeeEmployer.employee_id).join(
                             employer.Employer,employer.Employer.employer_id==employee_employer.EmployeeEmployer.employer_id
                         )
    
    data=[]
    for row in obj:
        data.append({
            "employee_name":row.employee_name,
            "employee_id":row.employee_id,
            "employer_name":row.employer_name,
            "employer_id":row.employer_id,
            "joined_time":str(row.joined_time)
        })

    return  data


def unsubscribe_employee_to_employer(connection,employee_id,employer_id):
    del_obj=connection.query(employee_employer.EmployeeEmployer).filter(
        and_(
            employee_employer.EmployeeEmployer.employee_id==employee_id,
            employee_employer.EmployeeEmployer.employer_id==employer_id
        )
    ).first()

    if del_obj!=None:
        connection.delete(del_obj)
        connection.commit()
        return True

    return False

def get_employer_enrollment_count(connection):
    res_obj=connection.query(employer.Employer.employer_name,func.count("*").label("count_of_enrollments")).join(employee_employer.EmployeeEmployer,employer.Employer.employer_id==employee_employer.EmployeeEmployer.employer_id).group_by(employer.Employer.employer_id)

    print(res_obj)
    return {
        "employer_name":res_obj.employer_name,
        
    }
