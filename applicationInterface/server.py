import json

import psycopg2
import bcrypt
import secrets
import tg
from tg import expose, RestController, MinimalApplicationConfigurator
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

sessionid_dict = {}  # key: sessionid, value: email


# Verify if an account already exists.
def verifyAccount(email, password):
    # Check if we find a username and password that matches.
    try:
        cur.execute("SELECT * FROM student WHERE email=%(email)s", {'email': email})
        cur.execute("SELECT salt FROM student WHERE email=%(email)s", {'email': email})
        salt = cur.fetchall()[0][0]
        hashedPassword = bcrypt.hashpw(password.encode('utf8'), salt.encode('utf8')).decode('utf8')
        # cur.execute("SELECT * FROM test WHERE id=%s and number=%s",(username,hashedPassword)) # Test
        cur.execute("SELECT * FROM student WHERE email=%(email)s and password=%(password)s",
                    {'email': email, 'password': hashedPassword})
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
    cur.execute("SELECT * FROM Student WHERE email=%(email)s", {'email': email})
    result = cur.fetchall()

    if len(result) != 0:
        return False

    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode('utf8'), salt).decode('utf8')
    salt = salt.decode('utf8')
    try:
        # cur.execute("INSERT INTO test VALUES (%s,%s)",(username,hashedPassword)) # Test
        cur.execute("INSERT INTO Student VALUES (%(email)s,%(hashedPassword)s,%(salt)s)",
                    {{'email': email, 'hashedPassword': hashedPassword, 'salt': salt}})
    except:
        return False
    cur.execute("SELECT * FROM Student WHERE email=%(email)s", {'email': email})
    result = cur.fetchall()
    return True


def editProfile(email, hobbies, interests, fname, lname, new_email):
    try:
        cur.execute("SELECT * FROM student_profile WHERE email=%(email)s", {'email': email})
        result = cur.fetchall()

        if len(result) != 0:
            cur.execute(
                "UPDATE student_profile SET email=%(new_email)s,hobbies=%(hobbies)s,interests=%(interests)s,"
                "fname=%(fname)s,lname=%(lname)s WHERE email=%(email)s",
                {'email': email, 'new_email': new_email, 'hobbies': hobbies, 'interests': interests, 'fname': fname,
                 'lname': lname}
            )
        else:
            cur.execute(
                "INSERT INTO student_profile(email, hobbies, interests, fname, lname) VALUES(%(new_email)s, %(hobbies)s,"
                "%(interests)s, %(fname)s, %(lname)s)",
                {'new_email': new_email, 'hobbies': hobbies, 'interests': interests, 'fname': fname,
                 'lname': lname}
            )
    except:
        return False
    return True


def retrieveProfileData(email):
    cur.execute("SELECT * FROM student_profile WHERE email=%(email)s", {'email': email})
    result = cur.fetchall()
    result = json.dumps(result)
    return result

# Check if a specific chatroom has had any new messages since the provided time.
def checkForMessages(chatroomID,dateTime):
    try:
        cur.execute("SELECT * FROM message WHERE chatroom_id = %(chatroomID)s and date_time_sent > %(dateTime)s",
                    {"chatroomID":chatroomID,"dateTime":dateTime})
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
    format = '%Y-%m-%d %H:%M:%S'
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
    date = dateTimeObj.strftime('%Y-%m-%d')

    # Select (CourseStartTime,CourseEndTime) if a course meets on the same day of the week as the event and the event occurs during the
    # semester.
    # <<< [TEST - UNCOMMENT AFTER TEST] >>>
    query = (
        f"SELECT section.start_time,section.end_time"
        f" FROM takes LEFT JOIN section ON takes.uni_id = section.uni_id"
        f" AND takes.course_id = section.course_id AND takes.section_id = section.section_id WHERE "
        f"takes.student_id = {studentID} AND section.{dayToCol[dayOfWeek]} = 'True' AND section.semStartDate < "
        f"{date} AND section.semEndDate > {date}"
    )
    # <<< [TEST - UNCOMMENT AFTER TEST] >>>
    cur.execute(query) #<<< [TEST - UNCOMMENT AFTER TEST] >>>
    result = cur.fetchall() #<<< [TEST - UNCOMMENT AFTER TEST] >>>
    #result = [("07:00:00","07:59:59"),("15:00:00","16:00:00"),("16:30:00","18:30:00")] # <<< [TEST - DELETE AFTER TEST] >>>

    # For all course times, add them to the date of the event, convert them to epoch time, and add it to the output list.
    # If an event occurs during the semester, and the event day of the week is on the same day as when a class meets, there may be a conflict.
    for time in result:
        courseStartTime = date+" "+time[0]
        courseStartEpoch = (datetime.datetime.strptime(courseStartTime, format)).timestamp()
        courseEndTime = date+" "+time[1]
        courseEndEpoch = (datetime.datetime.strptime(courseEndTime, format)).timestamp()
        output.append((courseStartEpoch,courseEndEpoch))
    return output

# For a given event's start/end times and a student, return True if the student has a time conflict.  False otherwise.
def identifiedTimeConflict(startTime,endTime,studentID):
    format = '%Y-%m-%d %H:%M:%S'

    # > Convert start/end time of event into DateTime obj.
    eventStartDateTime = datetime.datetime.strptime(startTime, format)
    eventEndDateTime = datetime.datetime.strptime(endTime, format)

    # > Take the start/end DateTimes of the event and convert them into epoch values.
    startEpoch = eventStartDateTime.timestamp()
    endEpoch = eventEndDateTime.timestamp()

    # > Get all events the student is in as a list of tuples of type (EventStartEpoch,EventEndEpoch).
    cur.execute(f"SELECT event.start_time,event.end_time FROM going_to_event LEFT JOIN event ON going_to_event.event_id = event.event_id WHERE going_to_event.studentID = {studentID}") #<<< [TEST - UNCOMMENT AFTER TEST] >>>
    eventResult = cur.fetchall() #<<< [TEST - UNCOMMENT AFTER TEST] >>>
    #eventResult = [("2023-11-03 07:00:00","2023-11-03 08:30:00"),("2023-11-03 15:00:00","2023-11-03 16:00:00"),("2023-11-04 10:00:00","2023-11-04 12:00:00")] # <<< [TEST - DELETE AFTER TEST] >>>

    # Go though eventResult (ex: [("YYYY-MM-DD HH:mm:ss", "YYYY-MM-DD HH:mm:ss"), ...]) and convert them into epoch values.
    for i in range(len(eventResult)):
        newStart = (datetime.datetime.strptime(eventResult[i][0], format)).timestamp()
        newEnd = (datetime.datetime.strptime(eventResult[i][1], format)).timestamp()
        eventResult[i] = (newStart,newEnd)

    # > Get all courses the student is in as a list of tuples of type (CourseStartEpoch,CourseEndEpoch).
    courseResult = []
    courseResult.extend(courseDataToEpoch(eventStartDateTime))
    # If the event is on different dates ...
    eventStartDate = eventStartDateTime.strftime('%Y-%m-%d')
    eventEndDate = eventEndDateTime.strftime('%Y-%m-%d')
    if (eventStartDate != eventEndDate):
        courseResult.extend(courseDataToEpoch(eventEndDateTime))

    # > Go through the scheduled events/courses on the same days as the event and see if a conflict exists.
    schedule = eventResult + courseResult
    for i in schedule:
        if (startEpoch <= i[1]) and (endEpoch >= i[0]):
            return True
    return False

######################### ^ NEW 11/1 ^ #########################

# Main controller class.
class RootController(RestController):
    def _before(self, *remainder, **params):
        tg.response.headers.update({'Access-Control-Allow-Origin': '*'})

    @staticmethod
    def is_method(method):
        def inner(func):
            def wrapper(*args, **kwargs):
                if method == tg.request.method:
                    return func(*args, **kwargs)
                else:
                    print(f"Expect request method {method}, received {tg.request.method} instead")
                    return {"result": False}

            return wrapper

        return inner

    @staticmethod
    def check_session_id(id):
        if id in sessionid_dict:
            return sessionid_dict[id]
        else:
            return None

    # Method to handle user authentication requests.
    @expose('json')
    def authenticateUserSignIn(self, email, password):
        result = verifyAccount(email, password)
        token = 0
        if result:
            token = secrets.token_urlsafe(20)
            sessionid_dict[token] = email
        return {"result": result, "sessionid": token}

    # Method to handle new user registration.
    @expose('json')
    @is_method('POST')
    def registerNewUser(self, email, password):
        result = registerAccount(email, password)
        token = 0
        if result:
            token = secrets.token_urlsafe(20)
            sessionid_dict[token] = email
            editProfile(email, '', '', '', '', email)
        return {"result": result, "sessionid": token}

    # Method to create student profile
    @expose('json')
    @is_method('POST')
    def editStudentProfile(self, sessionid, hobbies, interests, fname, lname, new_email):
        email = self.check_session_id(sessionid)
        return {
            "result": editProfile(email, hobbies, interests, fname, lname, new_email)}

    # Method to retrieve data of a student profile for a particular student
    @expose('json')
    def getStudentProfileData(self, sessionid):
        email = self.check_session_id(sessionid)
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

    # <<< [TEST - DELETE AFTER TEST] >>> #
    """@expose('json')
    def test(self):
        # Fake event start and end time.
        startTime = "2023-11-03 08:00:00"
        endTime = "2023-11-03 10:00:00"
        # Fake student ID.
        studentID = "abc123"
        return {"timeConflictExists":identifiedTimeConflict(startTime,endTime,studentID)}"""
    # <<< [TEST - DELETE AFTER TEST] >>> #

    ######################### ^ NEW 11/1 ^ #########################


config = MinimalApplicationConfigurator()
config.update_blueprint({
    'root_controller': RootController(),
})
application = config.make_wsgi_app()
print("Serving on port 8060...")

server = make_server('', 8060, application)

server.serve_forever()
