import requests

def request_schedule(cur,email):
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