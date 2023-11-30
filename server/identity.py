import requests

def verify_uni_email(cur,email):
    url = f"http://localhost:8008/verifyStudentEmail?email={email}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error":True}
    
def retrieve_verification_status(cur,email):
    cur.execute("SELECT * FROM student WHERE email=%(email)s AND student_id IS NOT NULL",{'email':email})
    result = cur.fetchall()
    if len(result) != 0:
        return {"verified":True}
    return {"verified":False}