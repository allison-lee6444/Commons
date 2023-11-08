from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Backend Functions
from authentication import *
from chatroom import *
from events import *
from profiles import *
from flashcard import *

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
def authenticateUserSignIn(self, email, password):
    return {"result": verifyAccount(email, password)}

# Method to handle new user registration.
@app.get("/registerNewUser")
def registerNewUser(self, email, password):
    return {"result": registerAccount(email, password)}

# Method to create student profile
@app.get("/editStudentProfile")
def editStudentProfile(self,email, hobbies, interests, fname, lname,new_email):
    print(email, hobbies, interests, fname, lname,new_email)
    return {
        "result": editProfile(email,hobbies, interests, fname, lname,new_email)}

# Method to retrieve data of a student profile for a particular student
@app.get("/getStudentProfileData")
def getStudentProfileData(self, email):
    return retrieveProfileData(email)

# Method used by the front-end to check if there are any new messages.
@app.get("/newMesages")
def newMesages(self,chatroomID,dateTime):
    return checkForMessages(chatroomID,dateTime)

# Method to create a new event and save it in the DB.
@app.get("/scheduleNewEvent")
def scheduleNewEvent(self,eventName,hostID,description,locName,locCoord,startTime,endTime,eventID):
    return {"success":createEvent(eventName,hostID,description,locName,locCoord,startTime,endTime,eventID)}

# Method called when a student joins a event.
@app.get("/joinEventClicked")
def joinEventClicked(self,eventID,studentID,chatroomID):
    return {"success":studentJoinEvent(eventID,studentID,chatroomID)}

# Method called when a student leaves a event.
@app.get("/leaveEventClicked")
def leaveEventClicked(self,studentID,eventID):
    return {"success":deleteEvent(studentID,eventID)}

# Method called when the host of an event cancels the event.
@app.get("/cancelScheduledEvent")
def cancelScheduledEvent(self,hostID,eventID):
    return {"success":cancelEvent(hostID,eventID)}

# Method called to get all events a student is apart of.
@app.get("/getUserEvents")
def getUserEvents(self,studentID):
    result = getUserEvents(studentID)
    if not result:
        return {"success":False}
    return {"events":result}

# Method called to get all courses a student is in.
@app.get("/getUserCourses")
def getUserCourses(self,studentID):
    result = getUserCourses(studentID)
    if not result:
        return {"success":False}
    return {"courses":result}

# Method called to help a student identify if joining an event will create a time conflict.
@app.get("/identifyTimeConflict")
def identifyTimeConflict(self,startTime,endTime,studentID):
    return {"timeConflictExists":identifiedTimeConflict(startTime,endTime,studentID)}

@app.get("/createFlashcard")
def createFlashcardForChatroom(self, chatroom_id, front_text, back_text):
    return {"success":createFlashcard(chatroom_id, front_text, back_text)}

@app.get("/deleteFlashcard")
def deleteFlashcardFromChatroom(self, chatroom_id, front_text, back_text):
    return {"success":createFlashcard(chatroom_id, front_text, back_text)}

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
