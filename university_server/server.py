import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create database connection.
conn = psycopg2.connect(
    host="localhost",
    database="uni_server",
    user="commons_dev",
    password="commons_dev"
)
"""
university_server
user="commons_dev",
password="commons_dev"
"""

# Create cursor to interact with the database.
cur = conn.cursor()


# Method to check if an email are in the student table.
def verifyStudentEmail(email):
    try:
        cur.execute("SELECT * FROM student WHERE email=%(email)s", {'email': email})
        result = cur.fetchall()
        if len(result) != 0:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


# Method to get a student's schedule.
def retrieveSchedule(email):
    try:
        cur.execute(
            "SELECT takes.student_id,takes.course_id,takes.section_id,takes.uni_id FROM takes LEFT JOIN student"
            " ON takes.student_id = student.student_id WHERE student.email=%(email)s", {'email': email}
        )
        result = cur.fetchall()
        return {"takes": result}
    except Exception as e:
        print(e)
        return {"error": True}


# Method to get a student's profile data.
# school, school id, grad year, major
def retrieveProfile(email):
    try:
        cur.execute("SELECT student_id,uni_id,major,graduation_year FROM student WHERE email=%(email)s",
                    {'email': email})
        result = cur.fetchall()
        return {"profile": result}
    except Exception as e:
        print(e)
        return {"error": True}

def get_courses_sections():
    try:
        cur.execute("SELECT * FROM course")
        courses = cur.fetchall()
        cur.execute("SELECT * FROM section")
        sections = cur.fetchall()
        return {"course": courses, "section": sections}
    except Exception as e:
        print(e)
        return {"error": True}
    
# Method to check if a student's major or graduation has changed.  If it did, return the new values.
# Student should be verified at this point so we use studentID.
def checkProfileChange(studentID,major,gradYear):
    pass


# Method to handle user identity verification requests.
@app.get("/verifyStudentEmail")
def verifyStudentEmail(email):
    return {"emailExists": verifyStudentEmail(email)}


# Method to handle requests for a student's schedule.
@app.get("/getStudentSchedule")
def getStudentSchedule(email):
    return retrieveSchedule(email)


# Method to handle requests for a student's profile.
@app.get("/getStudentProfile")
def getStudentProfile(email):
    return retrieveProfile(email)

@app.get("/getCoursesSections")
def getCoursesSections():
    return get_courses_sections()

# Method to handle requests to see if a student's profile changed.
@app.get("/checkProfile")
def checkProfile(studentID,major,gradYear):
    return checkProfileChange(studentID,major,gradYear)

# <<< [TEST - DELETE AFTER TEST] >>> #
# Fake Server Communication Test
"""@app.get("/testRequest")
def testRequest():
    return {"FROM FAKE SERVER":"HI!!!"}"""
# <<< [TEST - DELETE AFTER TEST] >>> #
