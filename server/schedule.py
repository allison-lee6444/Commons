import requests
from cursor import cur

# <<< [TEST - DELETE AFTER TEST] >>> #
# Fake Server Communication Test
"""def testRequest():
    url = f"http://localhost:8008/testRequest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()"""
# <<< [TEST - DELETE AFTER TEST] >>> #

def requestStudentSchedule(studentID):
    url = f"http://localhost:8008/getStudentSchedule?student_id={studentID}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        takesData = data["takes"]

        for row in takesData:
            cur.execute(f"INSERT INTO takes VALUES {row}")

        return True
    else:
        return False