import json

import psycopg2
import bcrypt
import secrets
import tg
from tg import expose, RestController, MinimalApplicationConfigurator
from wsgiref.simple_server import make_server

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
        cur.execute(f"SELECT * FROM takes LEFT JOIN section ON takes.uni_id = section.uni_id AND takes.course_id = section.course_id AND takes.section_id = section.section_id WHERE student_id = {studentID}")
        result = cur.fetchall()
        return result
    except:
        return False

# Returns any users with a time conflict for a given event.
def getTimeConflict():
    pass

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
    def identifyTimeConflict():
        pass

    ######################### ^ NEW 11/1 ^ #########################


config = MinimalApplicationConfigurator()
config.update_blueprint({
    'root_controller': RootController(),
})
application = config.make_wsgi_app()
print("Serving on port 8060...")

server = make_server('', 8060, application)

server.serve_forever()
