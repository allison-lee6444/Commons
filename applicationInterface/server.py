import json

import psycopg2
import bcrypt
import tg
from tg import expose, TGController, AppConfig
from wsgiref.simple_server import make_server
import datetime

# Create database connection.
conn = psycopg2.connect(
    host="localhost",
    database="commons",
    user="commons_dev",
    password="commons_dev"
)
"""
user="commons_dev",
password="commons_dev"
"""

# Create cursor to interact with the database.
cur = conn.cursor()


# Verify if an account already exists.
def verifyAccount(email, password):
    # Check if we find a username and password that matches.
    try:
        cur.execute(f"SELECT * FROM student WHERE email='{email}'")
        cur.execute(f"SELECT salt FROM student WHERE email='{email}'")
        salt = cur.fetchall()[0][0]
        hashedPassword = bcrypt.hashpw(password.encode('utf8'), salt.encode('utf8')).decode('utf8')
        # cur.execute("SELECT * FROM test WHERE id=%s and number=%s",(username,hashedPassword)) # Test
        cur.execute(f"SELECT * FROM student WHERE email='{email}' and password='{hashedPassword}'")
        result = cur.fetchall()
    except:
        return False

    # Returns true if authentication was a success.
    if len(result) == 1:
        return True
    # False otherwise.
    return False


# Register a new account.
def registerAccount(email, password):
    # Check if the username exists, if it does return false.
    cur.execute(f"SELECT * FROM Student WHERE email='{email}'")
    result = cur.fetchall()

    if len(result) != 0:
        return False

    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode('utf8'), salt).decode('utf8')
    salt = salt.decode('utf8')
    try:
        # cur.execute("INSERT INTO test VALUES (%s,%s)",(username,hashedPassword)) # Test
        cur.execute(f"INSERT INTO Student VALUES ('{email}','{hashedPassword}','{salt}')")
    except:
        return False
    cur.execute(f"SELECT * FROM Student WHERE email='{email}'")
    result = cur.fetchall()
    print(result)
    return True


def editProfile(email, hobbies, interests, fname, lname, new_email):
    try:
        cur.execute(f"SELECT * FROM student_profile WHERE email='{email}'")
        result = cur.fetchall()

        if len(result) != 0:
            cur.execute(
                f"UPDATE student_profile SET email='{new_email}',hobbies='{hobbies}',interests='{interests}',fname='{fname}',lname='{lname}' WHERE email='{email}'"
            )
        else:
            cur.execute(
                f"INSERT INTO student_profile(email, hobbies, interests, fname, lname) VALUES('{email}', '{hobbies}', '{interests}', '{fname}', '{lname}')"
            )
    except:
        return False
    return True


def retrieveProfileData(email):
    cur.execute(f"SELECT * FROM student_profile WHERE email='{email}'")
    result = cur.fetchall()
    result = json.dumps(result)
    return result

# Check if a specific chatroom has had any new messages since the provided time.
def checkForMessages(chatroomID,dateTime):
    try:
        cur.execute(f"SELECT * FROM message WHERE chatroom_id = {chatroomID} and date_time_sent > {dateTime}")
        result = json.dumps(cur.fetchall())
        return result
    except:
        return {"noNewMessages":True}

######################### V NEW 11/1 V #########################
# Create a new event.
def createEvent(eventName,hostID,description,locName,locCoord,startTime,endTime,eventID):
    try:
        cur.execute(f"INSERT INTO Event VALUES ('{eventName}',{hostID},'{description}','{locName}',{locCoord},{startTime},{endTime},{eventID})")
        return True
    except: 
        return False

# When a student hits the "join event" button.
def studentJoinEvent(eventID,studentID,chatroomID):
    try:
        cur.execute(f"INSERT INTO going_to_event VALUES ({eventID},{studentID},{chatroomID})")
        return True
    except:
        return False

# User decided to leave an event.
def deleteEvent(studentID,eventID):
    try:
        cur.execute(f"DELETE FROM going_to_event WHERE student_id = {studentID} AND event_id = {eventID}")
        return True
    except:
        return False

# Host decided to cancel an event.
def cancelEvent(hostID,eventID):
    try:
        cur.execute(f"DELETE FROM event WHERE host_id = {hostID} AND event_id = {eventID}")

        cur.execute(f"SELECT student_id FROM going_to_event WHERE event_id = {eventID}")
        result = cur.fetchall()
        for student in result:
            deleteEvent(student[0],eventID)

        return True
    except:
        return False

# Get a list of all events a user is participating in.
def getUserEvents(studentID):
    try:
        cur.execute(f"SELECT * FROM going_to_event LEFT JOIN event ON going_to_event.event_id = event.event_id WHERE going_to_event.studentID = {studentID}")
        result = cur.fetchall()
        return result
    except:
        return False

# Get a list of all courses a user is in.
def getUserCourses(studentID):
    try:
        cur.execute(f"SELECT * FROM takes LEFT JOIN section ON takes.uni_id = section.uni_id AND takes.course_id = section.course_id AND takes.section_id = section.section_id WHERE takes.student_id = {studentID}")
        result = cur.fetchall()
        return result
    except:
        return False

# Takes a DateTime object and returns a list of (CourseStartEpoch,CourseEndEpoch) for each course that meets on the same day.
def courseDataToEpoch(dateTimeObj):
    output = []

    # Used to convert a day of the week to the name of the column that stores whether or not a course meets on that day.
    dayToCol = {
        "Monday":"meetsMon",
        "Tuesday":"meetsTue",
        "Wednesday":"meetsWed",
        "Thursday":"meetsThu",
        "Friday":"meetsFri",
        "Saturday":"meetsSat",
        "Sunday":"meetsSun"
    }

    # Takes the DateTime and gets the day of the week.
    dayOfWeek = dateTimeObj.strftime('%A')
    # Gets only the date from the Datetime obj.
    date = dateTimeObj.date()

    # Select (CourseStartTime,CourseEndTime) if a course meets on the same day of the week as the event and the event occurs during the
    # semester.
    query = (
        f"SELECT section.start_time,section.end_time"
        f" FROM takes LEFT JOIN section ON takes.uni_id = section.uni_id"
        f" AND takes.course_id = section.course_id AND takes.section_id = section.section_id WHERE "
        f"takes.student_id = {studentID} AND section.{dayToCol[dayOfWeek]} = 'True' AND section.semStartDate < "
        f"{date} AND section.semEndDate > {date}"
    )
    cur.execute(query)
    result = cur.fetchall()

    # For all course times, add them to the date of the event, convert them to epoch time, and add it to the output list.
    # If an event occurs during the semester, and the event day of the week is on the same day as when a class meets, there may be a conflict.
    for time in result:
        courseStartTime = date+" "+time[0]
        courseStartEpoch = (datetime.strptime(courseStartTime, format)).timestamp()
        courseEndTime = date+" "+time[1]
        courseEndEpoch = (datetime.strptime(courseEndTime, format)).timestamp()
        output.append((courseStartEpoch,courseEndEpoch))
    return output

# For a given event's start/end times and a student, return True if the student has a time conflict.  False otherwise.
def identifiedTimeConflict(startTime,endTime,studentID):
    format = '%Y-%m-%d %H:%M:%S'

    # > Convert start/end time of event into DateTime obj.
    eventStartDateTime = datetime.strptime(startTime, format)
    eventEndDateTime = datetime.strptime(endTime, format)

    # > Take the start/end DateTimes of the event and convert them into epoch values.
    startEpoch = eventStartDateTime.timestamp()
    endEpoch = eventEndDateTime.timestamp()

    # > Get all events the student is in as a list of tuples of type (EventStartEpoch,EventEndEpoch).
    cur.execute(f"SELECT event.start_time,event.end_time FROM going_to_event LEFT JOIN event ON going_to_event.event_id = event.event_id WHERE going_to_event.studentID = {studentID}")
    eventResult = cur.fetchall()

    # Go though eventResult (ex: [("YYYY-MM-DD HH:mm:ss", "YYYY-MM-DD HH:mm:ss"), ...]) and convert them into epoch values.
    for i in range(len(eventResult)):
        newStart = (datetime.strptime(eventResult[i][0], format)).timestamp()
        newEnd = (datetime.strptime(eventResult[i][1], format)).timestamp()
        eventResult[i] = (newStart,newEnd)

    # > Get all courses the student is in as a list of tuples of type (CourseStartEpoch,CourseEndEpoch).
    courseResult = []
    courseResult.extend(courseDataToEpoch(courseQueryResult,eventStartDateTime))
    courseResult.extend(courseDataToEpoch(courseQueryResult,eventEndDateTime))

    # > Go through the scheduled events/courses on the same days as the event and see if a conflict exists.
    schedule = eventResult + courseResult
    for i in schedule:
        if (startEpoch <= i[1]) and (endEpoch >= i[0]):
            return True
    return False

######################### ^ NEW 11/1 ^ #########################

# Main controller class.
class RootController(TGController):
    def _before(self, *remainder, **params):
        tg.response.headers.update({'Access-Control-Allow-Origin': '*'})

    # Method to handle user authentication requests.
    @expose('json')
    def authenticateUserSignIn(self, email, password):
        return {"result": verifyAccount(email, password)}

    # Method to handle new user registration.
    @expose('json')
    def registerNewUser(self, email, password):
        return {"result": registerAccount(email, password)}

    # Method to create student profile
    @expose('json')
    def editStudentProfile(self,email, hobbies, interests, fname, lname,new_email):
        print(email, hobbies, interests, fname, lname,new_email)
        return {
            "result": editProfile(email,hobbies, interests, fname, lname,new_email)}

    # Method to retrieve data of a student profile for a particular student
    @expose('json')
    def getStudentProfileData(self, email):
        return retrieveProfileData(email)
    
    # Method used by the front-end to check if there are any new messages.
    @expose('json')
    def newMesages(self,chatroomID,dateTime):
        return checkForMessages(chatroomID,dateTime)

    ######################### V NEW 11/1 V #########################

    @expose('json')
    def scheduleNewEvent(self,eventName,hostID,description,locName,locCoord,startTime,endTime,eventID):
        return {"success":createEvent(eventName,hostID,description,locName,locCoord,startTime,endTime,eventID)}

    @expose('json')
    def joinEventClicked(self,eventID,studentID,chatroomID):
        return {"success":studentJoinEvent(eventID,studentID,chatroomID)}

    @expose('json')
    def leaveEventClicked(self,studentID,eventID):
        return {"success":deleteEvent(studentID,eventID)}

    @expose('json')
    def cancelScheduledEvent(self,hostID,eventID):
        return {"success":cancelEvent(hostID,eventID)}

    @expose('json')
    def getUserEvents(self,studentID):
        result = getUserEvents(studentID)
        if not result:
            return {"success":False}
        return {"events":result}

    @expose('json')
    def getUserCourses(self,studentID):
        result = getUserCourses(studentID)
        if not result:
            return {"success":False}
        return {"courses":result}

    @expose('json')
    def identifyTimeConflict(self,startTime,endTime,studentID):
        return {"timeConflictExists":identifiedTimeConflict(startTime,endTime,studentID)}

    ######################### ^ NEW 11/1 ^ #########################


config = AppConfig(minimal=True, root_controller=RootController())
application = config.make_wsgi_app()

print("Serving on port 8060...")
server = make_server('', 8060, application)
server.serve_forever()
