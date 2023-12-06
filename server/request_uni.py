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


def request_courses_sections(cur):
    url = f"http://localhost:8008/getCoursesSections"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        section_data = data["section"]
        course_data = data["course"]

        try:
            for row in course_data:
                # Make sure this course isn't already in courses.
                cur.execute("SELECT * FROM course WHERE id=%(course)s AND uni_id=%(uni_id)s",
                            {'course': row[0], 'uni_id': row[1]})
                result = cur.fetchall()
                if len(result) == 0:
                    # Order is different in tables.
                    cur.execute("INSERT INTO course VALUES (%(course)s, %(uni_id)s)",
                                {'course': row[0], 'uni_id': row[1]})
                    print(f'course inserted {row[0]}')
            cur.execute("COMMIT")

            for row in section_data:
                # Make sure this section isn't already in section.
                cur.execute("SELECT * FROM section WHERE course_id=%(course)s AND uni_id=%(uni_id)s "
                            "AND section_id=%(sec_id)s",
                            {'course': row[0], 'uni_id': row[2], 'sec_id': row[1]})
                result = cur.fetchall()
                if len(result) == 0:
                    # Order is different in tables.
                    cur.execute("INSERT INTO section VALUES (%(course)s,%(uni_id)s,%(section_id)s,"
                                "%(start_time)s, %(end_time)s, "
                                "%(semStartDate)s, %(semEndDate)s, %(year)s,"
                                "%(meetsMon)s, %(meetsTue)s,%(meetsWed)s,"
                                "%(meetsThu)s,%(meetsFri)s,%(meetsSat)s"
                                ",%(meetsSun)s)",
                                {'course': row[0],
                                 'uni_id': row[2],
                                 'section_id': row[1],
                                 'start_time': row[3],
                                 'end_time': row[4],
                                 'semStartDate': row[5],
                                 'semEndDate': row[6],
                                 'year': row[7],
                                 'meetsMon': row[8],
                                 'meetsTue': row[9],
                                 'meetsWed': row[10],
                                 'meetsThu': row[11],
                                 'meetsFri': row[12],
                                 'meetsSat': row[13],
                                 'meetsSun': row[14]
                                 })
                    cur.execute("COMMIT")
        except Exception as e:
            print(e)
            return False

        return True
    else:
        return False
