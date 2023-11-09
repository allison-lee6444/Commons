from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Backend Functions
from authentication import *
from chatroom import *
from events import *
from profiles import *
from schedule import *
from identity import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Method to handle user authentication requests.
@app.get("/authenticateUserSignIn")
def authenticateUserSignIn(email, password):
    return {"result": verifyAccount(email, password)}

# Method to handle new user registration.
@app.get("/registerNewUser")
def registerNewUser(email, password):
    return {"result": registerAccount(email, password)}

# Method to create student profile
@app.get("/editStudentProfile")
def editStudentProfile(email, hobbies, interests, fname, lname,new_email):
    print(email, hobbies, interests, fname, lname,new_email)
    return {
        "result": editProfile(email,hobbies, interests, fname, lname,new_email)}

# Method to retrieve data of a student profile for a particular student
@app.get("/getStudentProfileData")
def getStudentProfileData(email):
    return retrieveProfileData(email)

# Method used by the front-end to check if there are any new messages.
@app.get("/newMesages")
def newMesages(chatroomID,dateTime):
    return checkForMessages(chatroomID,dateTime)

# Method to create a new event and save it in the DB.
@app.get("/scheduleNewEvent")
def scheduleNewEvent(eventName,hostID,description,locName,locCoord,startTime,endTime,eventID):
    return {"success":createEvent(eventName,hostID,description,locName,locCoord,startTime,endTime,eventID)}

# Method called when a student joins a event.
@app.get("/joinEventClicked")
def joinEventClicked(eventID,studentID,chatroomID):
    return {"success":studentJoinEvent(eventID,studentID,chatroomID)}

# Method called when a student leaves a event.
@app.get("/leaveEventClicked")
def leaveEventClicked(studentID,eventID):
    return {"success":deleteEvent(studentID,eventID)}

# Method called when the host of an event cancels the event.
@app.get("/cancelScheduledEvent")
def cancelScheduledEvent(hostID,eventID):
    return {"success":cancelEvent(hostID,eventID)}

# Method called to get all events a student is apart of.
@app.get("/getUserEvents")
def getUserEvents(studentID):
    result = getUserEvents(studentID)
    if not result:
        return {"success":False}
    return {"events":result}

# Method called to get all courses a student is in.
@app.get("/getUserCourses")
def getUserCourses(studentID):
    result = getUserCourses(studentID)
    if not result:
        return {"success":False}
    return {"courses":result}

# Method called to help a student identify if joining an event will create a time conflict.
@app.get("/identifyTimeConflict")
def identifyTimeConflict(startTime,endTime,studentID):
    return {"timeConflictExists":identifiedTimeConflict(startTime,endTime,studentID)}

# Method called to verify if a student is really a student at the university.
@app.get("/studentIdentityVerification")
def studentIdentityVerification(email,studentID):
    return requestIdentityVerification(email,studentID)

# Method called to import a student's schedule directly from the university.
@app.get("/importStudentSchedule")
def importStudentSchedule(studentID):
    return {"success":requestStudentSchedule(studentID)}

# <<< [TEST - DELETE AFTER TEST] >>> #
# Fake Server Communication Test
"""@app.get("/test")
def test():
    return {"FROM COMMONS SERVER":testRequest()}"""
# <<< [TEST - DELETE AFTER TEST] >>> #

# <<< [TEST - DELETE AFTER TEST] >>> #
"""@app.get("/test")
def test():
    # Fake event start and end time.
    startTime = "2023-11-03 08:00:00"
    endTime = "2023-11-03 10:00:00"
    # Fake student ID.
    studentID = "abc123"
    return {"timeConflictExists":identifiedTimeConflict(startTime,endTime,studentID)}"""
# <<< [TEST - DELETE AFTER TEST] >>> #
