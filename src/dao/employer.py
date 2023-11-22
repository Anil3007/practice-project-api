from src.model import employer

def get_all_employers(connection):
    res_obj=connection.query(employer.Employer.employer_id,employer.Employer.employer_name).all()

    response=[]
    for row in res_obj:
        response.append({
            "employer_id":row.employer_id,
            "employer_name":row.employer_name
        })
    return response
