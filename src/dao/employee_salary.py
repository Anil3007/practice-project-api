from src.model import employee_salary,employer,employee
import json

def getSalaryDetails(connection):
    res_obj=connection.query(employee_salary.EmployeeSalary.id,
                             employee_salary.EmployeeSalary.employee_id,
                             employee.Employee.employee_name,
                             employee_salary.EmployeeSalary.employer_id,
                             employer.Employer.employer_name,
                             employee_salary.EmployeeSalary.year,
                             employee_salary.EmployeeSalary.month,
                             employee_salary.EmployeeSalary.salary,
                             ).join(employer.Employer,employer.Employer.employer_id==employee_salary.EmployeeSalary.employer_id).join(employee.Employee,employee.Employee.employee_id==employee_salary.EmployeeSalary.employee_id).all()

    data=[]

    for item in res_obj:
        data.append({
            "id":item.id,
            "employee_id":item.employee_id,
            "employee_name":item.employee_name,
            "employer_id":item.employer_id,
            "employer_name":item.employer_name,
            "year":item.year,
            "month":item.month,
            "salary":item.salary
        })

    return data