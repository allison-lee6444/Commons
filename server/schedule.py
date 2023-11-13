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

def request_schedule(email):
    url = f"http://localhost:8008/getStudentSchedule?email={email}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        takesData = data["takes"]

        try:
            for row in takesData:
                # Order is different in tables.
                value = (row[0],row[3],row[1],row[2]) 
                cur.execute("INSERT INTO takes VALUES %(value)s",{'value':value})
            cur.execute("COMMIT")
        except Exception as e:
            print(e)
            return False
        
        return True
    else:
        return False