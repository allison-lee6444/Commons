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
    database="commons",
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

# Method to check if an email and studentID are in the student table.
def verifyStudentStatus(email,studentID):
    try:
        cur.execute(f"SELECT * FROM student WHERE email='{email}' and student_id={studentID}")
        result = cur.fetchall()
        if len(result) != 0:
            return True
        else:
            return False
    except: 
        return False

# Method to get a student's schedule.
def retrieveSchedule(studentID):
    try:
        cur.execute(f"SELECT * FROM takes WHERE student_id={studentID}")
        result = cur.fetchall()
        return {"takes":result}
    except:
        return {"error":True}

# Method to handle user identity verification requests.
@app.get("/verifyStudent")
def verifyStudent(email,studentID):
    return {"isAStudent":verifyStudentStatus(email,studentID)}

# Method to handle requests for a student's schedule.
@app.get("/getStudentSchedule")
def getStudentSchedule(studentID):
    return retrieveSchedule(studentID)

# <<< [TEST - DELETE AFTER TEST] >>> #
# Fake Server Communication Test
"""@app.get("/testRequest")
def testRequest():
    return {"FROM FAKE SERVER":"HI!!!"}"""
# <<< [TEST - DELETE AFTER TEST] >>> #

