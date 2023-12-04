import requests

def request_schedule(cur,email):
    url = f"http://localhost:8008/getStudentSchedule?email={email}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        takesData = data["takes"]

        try:
            # Get student ID as we need it to make sure the course/section they are taking isn't already in the takes table.
            cur.execute("SELECT student_id FROM student WHERE email=%(email)s",{'email':email})
            id = cur.fetchone()[0]
            for row in takesData:
                # Make sure this student's course/section isn't already in takes.
                cur.execute("SELECT * FROM takes WHERE student_id=%(id)s AND course_id=%(course)s AND section_id=%(sec)s",{'id':id,'course':row[1],'sec':row[2]})
                result = cur.fetchall()
                if len(result) == 0:
                    # Order is different in tables.
                    cur.execute(
                        "INSERT INTO takes VALUES (%(student_id)s,%(uni_id)s,%(course_id)s,%(section_id)s)",
                        {'student_id':row[0],'uni_id':row[3],'course_id':row[1],'section_id':row[2]}
                    )
            cur.execute("COMMIT")
        except Exception as e:
            print(e)
            return False
        
        return True
    else:
        return False