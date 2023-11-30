import pathlib,sys

root_path=pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve()
sys.path.append(str(root_path))




import os
from flask import Flask,request
import json,yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.dao import employee,employer,employee_employer
import re
from flask_bcrypt import Bcrypt 
import hashlib

app=Flask(__name__)
bcrypt=Bcrypt(app)

def get_db_connection():
    Session= sessionmaker(bind=engine_obj)
    return Session()

def get_hashed_pswd(password):
    h=hashlib.new("sha256")
    password=password.encode("UTF-8")
    h.update(password)
    pw_hash=h.hexdigest()
    return pw_hash

@app.route("/",methods=["GET"])
def default():
    return "works"

# curl "http://localhost:5001/return_json?a=3&b=5"
@app.route("/query_parameters",methods=["GET"])
def return_json():
    num1=request.args.get('a')
    num2=request.args.get('b')
    res={
        "num1":num1,
        "num2":num2,
        "addition":int(num1)+int(num2)
    }
    return json.dumps(res)

# curl -X POST -d "a=2" -d "b=5" http://localhost:5001/form_data
@app.route("/form_data",methods=["POST"])
def return_form_data():
    num1=request.form.get('a')
    num2=request.form.get('b')
    res={
        "num1":num1,
        "num2":num2,
        "add":int(num1)+int(num2)
    }
    return json.dumps(res)

# curl -X POST -d '{"a":2,"b":3}' http://localhost:5001/add_without_json
@app.route('/add_without_json',methods=["POST"])
def add_without_json():
    data=request.get_json(force=True)
    num1=data.get('a')
    num2=data.get('b')
    res={
        "num1":num1,
        "num2":num2,
        "addition":int(num1)+int(num2)
    }
    return json.dumps(res)

#  curl -X POST -H "Content-Type:application/json" -d '{"a":2,"b":3}' http://localhost:5001/add_with_json
@app.route('/add_with_json',methods=["POST"])
def add_with_json():
    num1=request.json.get('a')
    num2=request.json.get('b')
    res={
        "num1":num1,
        "num2":num2,
        "addition":int(num1)+int(num2)
    }
    return json.dumps(res)

#API to get all employee details
@app.route("/employees",methods=["GET"])
def get_employee_details():
    res={
        "status":None,
        "message":"success",
        "data":None
    }
    try:
        connection=get_db_connection()
        res["data"]=employee.get_all_employee_details(connection)
    except Exception as e:
        print(e)
        res["message"]="unable to get the results"
        res["status"]="failure"

    return json.dumps(res)

#API to get particular employee details
@app.route("/employee",methods=["POST"])
def employee_details():
    input=request.get_json(force=True)
    employee_name=input["employee_name"]
    password=input["password"]
    hashed_password=get_hashed_pswd(password)
    res={
        "status":"success",
        "message":None,
        "data":None
    }
    try:
        connection=get_db_connection()
        response=employee.get_employee_details(connection,employee_name)
        if response==None:
            res["status"]="failure"
            res["message"]="User Doesn't exist"
        else:
            if (hashed_password==response["employee_pw_hash"]):
                res["data"]=response
            else:
                res["status"]="fail"
                res["message"]="Invalid Password"

    except Exception as e:
        print(str(e))
        res["status"]="failure"
        res["message"]="unable to get details"

    return json.dumps(res)

#API to get particular employee details
@app.route("/getEmployee/<id>",methods=["GET"])
def get_employee(id):
    res={
        "status":"success",
        "message":None,
        "data":None,
    }
    try:
        connection=get_db_connection()
        res["data"]=employee.get_particular_employee_details(connection,int(id))
    except Exception as e:
        print(e)
        res["message"]="unable to get the "
        res["status"]="failure"
    return json.dumps(res)

#API to get all employer details
@app.route("/employers",methods=["GET"])
def employer_details():
    res={
        "status":"success",
        "message":None,
        "data":None,
    }
    try:
        connection=get_db_connection()
        res["data"]=employer.get_all_employers(connection)
    except Exception as e:
        print(str(e.message))
        res["message"]="unable to get the "
        res["status"]="failure"
    return json.dumps(res)

#API to subscribe to the employer 
@app.route("/employee/subscribe",methods=["POST"])
def suscribe_to_employer():
    input=request.get_json(force=True)
    employee_id=input.get("employee_id")
    employer_id=input.get("employer_id")
    res={
        "status":"success",
        "message":None,
        "data":None
    }
    try:
        if "employee_id" not in request.json:
            res["status"]="failure"
            res["message"]="employee id is not given"
        elif not re.match("^\d{1,9}$",str(employee_id)):
            res["status"]="failure"
            res["message"]="Invalid employee id is given"
        elif "employer_id" not in request.json:
            res["status"]="failure"
            res["message"]="employer is is not given"
        elif not re.match("^\d{1,4}",str(employer_id)):
            res["status"]="failure"
            res["message"]="Invalid employer id is given"
        else:   
            connection=get_db_connection()
            res["data"]=employee_employer.subscribe_to_employer(connection,employee_id,employer_id)
            res["message"]="successfully added"
    except Exception as e:
        print(str(e))
        res["status"]="failure"
        res["message"]="unable to subscribe"
    return json.dumps(res)

#API for adding new employee 
@app.route("/add/newemployee",methods=["POST"])
def new_employee():
    input=request.get_json(force=True)
    employee_name=input.get("employee_name")
    employee_email=input.get("email")
    password=input.get("password")
    # pw_hash=bcrypt.generate_password_hash(password)
    res={
        "status":None,
        "message":"success",
        "data":None
    }
    try:
        connection=get_db_connection()
        pw_hash=get_hashed_pswd(password)
        res["data"]=employee.add_new_employee(connection,employee_name,pw_hash,employee_email)
    except Exception as e:
        print(e)
        res["status"]="failure"
        res["message"]="unable to add"

    return json.dumps(res)

@app.route("/delete/employee",methods=["DELETE"])
def delete_employee_row():
    input=request.get_json(force=True)
    employee_id=input.get("employee_id")
    res={
        "status":"success",
        "message":None,
        "data":None
    }
    try:
        if "employee_id" not in input:
            res["status"]="failure"
            res["message"]="Employee_id not given"
        elif not re.match("^\d{1,4}",str(employee_id)):
            res["status"]="failure"
            res["message"]="Invalid employee_id given"
        else:
            connection=get_db_connection()
            res["data"]=employee.delete_employee(connection,employee_id)
    except Exception as e:
        print("this is error",str(e))
        res["status"]="failure"
        res["message"]="unable to delete"

    return json.dumps(res)

@app.route("/update/employee/employer",methods=["POST"])
def update():
    input=request.get_json(force=True)
    res={
        "status":"success",
        "message":None,
        "data":None
    }
    try:
        if "employee_id" not in input:
            res["status"]="failure"
            res["message"]="employee id not given"
        elif not re.match("^\d{1,3}",str(input["employee_id"])):
            res["status"]="failure"
            res["message"]="Invalid employee id given"
        elif "old_employer_id" not in input:
            res["status"]="failure"
            res["message"]="old employer id not given"
        elif not re.match("^\d{1,3}",str(input["old_employer_id"])):
            res["status"]="failure"
            res["message"]="Invalid old employer id given"
        elif "new_employer_id" not in input:
            res["status"]="failure"
            res["message"]="new employer id not given"
        elif not re.match("^\d{1,3}",str(input["new_employer_id"])):
            res["status"]="failure"
            res["message"]="Invalid new employer id"
        else:
            connection=get_db_connection()
            res["data"]=employee_employer.update_employer_details(
                connection,
                employee_id=input["employee_id"],
                old_employer_id=input["old_employer_id"],
                new_employer_id=input["new_employer_id"]
            )
    except Exception as e:
        print(str(e))
        res["status"]="failure"
        res["message"]="unable to get the details"
    return json.dumps(res)

#API to delete subscription
@app.route("/unsubscribe/employee",methods=["DELETE"])
def unsubscribe_employee():
    input=request.get_json(force=True)
    res={
        "status":"success",
        "message":None,
        "data":None
    }
    try:
        if "employee_id" not in input:
            res["status"]="failure"
            res["message"]="employee_id not given"
        elif not re.match("^\d{1,4}",str(input["employee_id"])):
            res["status"]="failure"
            res["message"]="Invalid employee_id is given"
        elif "employer_id" not in input:
            res["status"]="failure"
            res["message"]="employer_id not given"
        elif not re.match("^\d{1,4}",str(input["employer_id"])):
            res["status"]="failure"
            res["message"]="Invalid employer_id is given"
        else:
            connection=get_db_connection()
            res["data"]=employee_employer.unsubscribe_employee_to_employer(
                connection,
                input["employee_id"],
                input["employer_id"]
            )
    except Exception as e:
        print(str(e))
        res["status"]="failure"
        res["message"]="Unable to unsubscribe to employer"
    return json.dumps(res)

@app.route("/count_employer_enrollments",methods=["GET"])
def get_count():
    res={
        "status":"success",
        "message":None,
        "data":None
    }
    try:
        connection=get_db_connection()
        res["data"]=employee_employer.get_employer_enrollment_count(connection)
    except Exception as e:
        print(str(e))
        res["status"]="failure"
        res["message"]="uable to get details"
    return json.dumps(res)

@app.route("/details/with/names",methods=["GET"])
def get_all_details_with_names():
    res={
        "status":"success",
        "message":None,
        "data":None
    }
    try:
        connection=get_db_connection()
        res["data"]=employee_employer.joining_two_tables(connection)
    except Exception as e:
        print(str(e))
        res["status"]="failure"
        res["message"]="unable to get details"
    
    return json.dumps(res)

@app.route("/employee/employer/data",methods=["GET"])
def join_three_tables():
    res={
        "status":"success",
        "message":None,
        "data":None
    }
    try:
        connection=get_db_connection()
        res["data"]=employee_employer.get_details_of_three_joined_tables(connection)
    except Exception as e:
        print(str(e))
        res["status"]="failure"
        res["message"]="unable to get details"

    return json.dumps(res)
@app.route("/update/password",methods=["POST"])
def update_pswd():
    input=request.get_json(force=True)
    res={
        "status":"success",
        "message":None,
        "data":None
    }
    try:
        if "employee_name" not in input:
            res["status"]="failure"
            res["message"]="employee name not given"
        elif "email" not in input:
            res["status"]="failure"
            res["message"]="email id not given"
        elif "password" not in input:
            res["status"]="failure"
            res["message"]="password not given"
        else:
            connection=get_db_connection()
            password=input["password"]
            res["message"]=employee.update_employee_pswd(
                connection=connection,
                employee_name=input["employee_name"],
                email=input["email"],
                password=get_hashed_pswd(password)
                )
    except Exception as e:
        print(str(e))
        res["status"]="failure"
        res["message"]="unable to update the password"
    return json.dumps(res)

file_config=yaml.load(open(os.path.join(root_path,'conf','config.yml')))
engine_obj=create_engine(file_config["db_connection_string"],pool_size=30,isolation_level="READ COMMITTED")
app.run('localhost',5001)
