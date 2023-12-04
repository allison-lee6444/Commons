import requests
from server import cursor

def fetch_catalog(cur):
    print("Making request to university server.")
    url = f"http://localhost:8008/getCoursesSections"
    response = requests.get(url)
    if response.status_code == 200:
        print("Request complete.")
        data = response.json()
        if "error" not in data:
            courses = data["course"]
            sections = data["section"]

            print("Processing courses.")
            for row in courses:
                # First check if the course is already in course.
                courseData = {'courseID':row[0],'uniID':row[1]}
                cur.execute(
                    "SELECT * FROM course WHERE id=%(courseID)s AND uni_id=%(uniID)s",courseData
                )
                result = cur.fetchall()

                # If this row isn't already in course ...
                if len(result) == 0:
                    cur.execute(
                        "INSERT INTO course VALUES(%(courseID)s,%(uniID)s)",courseData
                    )
            print("Completed courses.")

            print("Processing sections.")
            for row in sections:
                # First check if the section is already in section.
                cur.execute(
                    "SELECT * FROM section WHERE course_id=%(courseID)s AND uni_id=%(uniID)s AND section_id=%(secID)s",
                    {'courseID':row[0] ,'uniID':row[2] ,'secID':row[1]}
                )
                result = cur.fetchall()

                # If this row isn't already in section ...
                if len(result) == 0:
                    cur.execute(
                        "INSERT INTO section VALUES(%(courseID)s,%(uniID)s,%(secID)s,%(startTime)s,"
                        "%(endTime)s,%(semStart)s,%(semEnd)s,%(year)s,%(meetsMon)s,%(meetsTue)s,"
                        "%(meetsWed)s,%(meetsThu)s,%(meetsFri)s,%(meetsSat)s,%(meetsSun)s)",
                        {
                            'courseID': row[0],
                            'uniID': row[2],
                            'secID': row[1],
                            'startTime': row[3],
                            'endtime': row[4],
                            'semStart': row[5],
                            'semdEnd': row[6],
                            'year': row[7],
                            'meetsMon': row[8],
                            'meetsTue': row[9],
                            'meetsWed': row[10],
                            'meetsThu': row[11],
                            'meetsFri': row[12],
                            'meetsSat': row[13],
                            'meetsSun': row[14]
                        }
                    )
            print("Completed sectionns.")

print("Starting utility ...")
fetch_catalog(cursor.cur)
print("Completed utility.")