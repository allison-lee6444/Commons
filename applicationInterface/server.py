from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Backend Functions
from authentication import *
from chatroom import *
from events import *
from profiles import *

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
@app.post("/registerNewUser")
def registerNewUser(email, password):
    return {"result": registerAccount(email, password)}


# Method to create student profile
@app.post("/editStudentProfile")
def editStudentProfile(email, hobbies, interests, fname, lname, new_email):
    return {
        "result": editProfile(email, hobbies, interests, fname, lname, new_email)}


# Method to retrieve data of a student profile for a particular student
@app.get("/getStudentProfileData")
def getStudentProfileData(email):
    return retrieveProfileData(email)


# Method used by the front-end to check if there are any new messages.
@app.get("/newMesages")
def newMesages(chatroomID, dateTime):
    return checkForMessages(chatroomID, dateTime)


# Method to create a new event and save it in the DB.
@app.post("/scheduleNewEvent")
def scheduleNewEvent(eventName, hostID, description, locName, locCoord, startTime, endTime, eventID):
    return {"result": createEvent(eventName, hostID, description, locName, locCoord, startTime, endTime, eventID)}


# Method called when a student joins a event.
@app.post("/joinEventClicked")
def joinEventClicked(eventID, studentID, chatroomID):
    return {"result": studentJoinEvent(eventID, studentID, chatroomID)}


# Method called when a student leaves an event.
@app.post("/leaveEventClicked")
def leaveEventClicked(studentID, eventID):
    return {"result": deleteEvent(studentID, eventID)}


# Method called when the host of an event cancels the event.
@app.post("/cancelScheduledEvent")
def cancelScheduledEvent(hostID, eventID):
    return {"result": cancelEvent(hostID, eventID)}


# Method called to get all events a student is a part of.
@app.get("/getUserEvents")
def getUserEvents(studentID):
    result = getUserEvents(studentID)
    if not result:
        return {"result": False}
    return {"result": result}


# Method called to get all courses a student is in.
@app.get("/getUserCourses")
def getUserCourses(studentID):
    result = getUserCourses(studentID)
    if not result:
        return {"success": False}
    return {"courses": result}


# Method called to help a student identify if joining an event will create a time conflict.
@app.get("/identifyTimeConflict")
def identifyTimeConflict(startTime, endTime, studentID):
    return {"timeConflictExists": identifiedTimeConflict(startTime, endTime, studentID)}


# <<< [TEST - DELETE AFTER TEST] >>> #
"""@app.get("/test")
def test(self):
    # Fake event start and end time.
    startTime = "2023-11-03 08:00:00"
    endTime = "2023-11-03 10:00:00"
    # Fake student ID.
    studentID = "abc123"
    return {"timeConflictExists":identifiedTimeConflict(startTime,endTime,studentID)}"""
# <<< [TEST - DELETE AFTER TEST] >>> #
