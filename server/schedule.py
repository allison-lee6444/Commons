import requests

def request_schedule(cur,email):
    url = f"http://localhost:8008/getStudentSchedule?email={email}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        takesData = data["takes"]

        try:
            for row in takesData:
                # Make sure this course/section isn't already in takes.
                cur.execute("SELECT * FROM takes WHERE course_id=%(course)s AND section_id=%(sec)s",{'course':row[1],'sec':row[2]})
                result = cur.fetchall()
                if len(result) == 0:
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