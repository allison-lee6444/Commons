import requests


def request_profile(cur, email):
    url = f"http://localhost:8008/getStudentProfile?email={email}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "error" not in data:
            profileData = data["profile"][0]
            profilesDict = {
                'student_id': profileData[0],
                'uni_id': profileData[1],
                'major': profileData[2],
                'graduation_year': profileData[3],
                'email': email
            }
            cur.execute(
                "UPDATE student SET student_id=%(student_id)s, uni_id=%(uni_id)s, major=%(major)s, graduation_year=%(graduation_year)s WHERE email=%(email)s",
                profilesDict)
            cur.execute("COMMIT")

            return True
    return False


def request_schedule(cur, email):
    url = f"http://localhost:8008/getStudentSchedule?email={email}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        takesData = data["takes"]

        try:
            for row in takesData:
                # Make sure this course/section isn't already in takes.
                cur.execute("SELECT * FROM takes WHERE course_id=%(course)s AND section_id=%(sec)s",
                            {'course': row[1], 'sec': row[2]})
                result = cur.fetchall()
                if len(result) == 0:
                    # Order is different in tables.
                    value = (row[0], row[3], row[1], row[2])
                    cur.execute("INSERT INTO takes VALUES %(value)s", {'value': value})
            cur.execute("COMMIT")
        except Exception as e:
            print(e)
            return False

        return True
    else:
        return False
