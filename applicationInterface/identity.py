import requests
from cursor import cur

def requestIdentityVerification(email,studentID):
    url = f"http://localhost:8008/verifyStudent?email={email}&student_id={studentID}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error":True}