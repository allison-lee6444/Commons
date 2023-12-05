import secrets

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# Backend Functions
import authentication
import chatroom
import events
import profiles
import schedule
import verify_identity
import identity
import flashcard
from cursor import cur

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

sessions = {}


def check_session_id(id):
    if id in sessions:
        return sessions[id]
    else:
        return None


# Method to handle user authentication requests.
@app.get("/login/")
def login(email, password):
    result = authentication.check_login(cur, email, password)
    token = None
    if result:
        token = secrets.token_urlsafe(20)
        sessions[token] = email
    return {"result": result, "sessionid": token}


# Method to handle new user registration.
@app.post("/register/")
def register(email, password):
    result = authentication.register_account(cur, email, password)
    token = None
    if result:
        token = secrets.token_urlsafe(20)
        sessions[token] = email
    return {"result": result, "sessionid": token}


@app.put("/changePassword/")
def changePassword(sessionid, current_pw, new_pw):
    email = check_session_id(sessionid)
    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid session ID",
        )
    return {"result": authentication.change_password(cur, email, current_pw, new_pw)}


# Method to create student profile
@app.put("/editProfile/")
def editProfile(sessionid, hobbies, interests, fname, lname, new_email):
    email = check_session_id(sessionid)
    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid session ID",
        )

    if email != new_email:
        sessions[sessionid] = new_email

    return {
        "result": profiles.edit_profile(cur, email, hobbies, interests, fname, lname, new_email)}


# Method to retrieve data of a student profile for a particular student
@app.get("/getProfile/")
def getProfile(sessionid):
    email = check_session_id(sessionid)
    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid session ID",
        )
    return profiles.get_profile(cur, email)


@app.get("/getEmail/")
def getEmail(sessionid):
    email = check_session_id(sessionid)
    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid session ID",
        )
    return {"result": email}


# Method used by the front-end to check if there are any new messages.
@app.get("/newMessages/")
def newMessages(chatroomID, dateTime):
    return chatroom.get_msg_update(cur, chatroomID, dateTime)


# Method to create a new event and save it in the DB.
@app.post("/editEvent/")
def editEvent(sessionid, chatroomID, eventName, description, locName, locCoord, startTime, endTime):
    email = check_session_id(sessionid)
    # check authorization using email and convert host id
    host_id, uni_id = profiles.get_student_uni_id(cur, email)
    return {
        "result":
            events.editEvent(cur, chatroomID, eventName, host_id, uni_id, description, locName, locCoord, startTime,
                             endTime)
    }


# Method called when a student joins a event.
@app.put("/joinEvent/")
def joinEvent(eventID, studentID, chatroomID):
    return {"result": events.join_event(cur, eventID, studentID, chatroomID)}


# Method called when a student leaves an event.
@app.put("/leaveEvent/")
def leaveEvent(studentID, eventID):
    return {"result": events.leave_event(cur, studentID, eventID)}


# Method called when the host of an event cancels the event.
@app.delete("/cancelEvent/")
def cancelEvent(hostID, eventID):
    return {"result": events.cancel_event(cur, hostID, eventID)}


# Method called to get event info of one event given event id
@app.get("/getEvent/")
def getEvent(sessionid, eventID, chatroomID):
    email = check_session_id(sessionid)
    student_id, uni_id = profiles.get_student_uni_id(cur, email)
    return {"result": events.get_event(cur, eventID, chatroomID, student_id, uni_id)}


# Method called to get all events a student is a part of.
@app.get("/getEvents/")
def getEvents(sessionid):
    email = check_session_id(sessionid)
    student_id, uni_id = profiles.get_student_uni_id(cur, email)
    return {"result": events.get_events(cur, student_id, uni_id)}


# Method called to get all courses a student is in.
@app.get("/getCourses/")
def getCourses(sessionid):
    email = check_session_id(sessionid)
    student_id, uni_id = profiles.get_student_uni_id(cur, email)
    return {"result": events.get_courses(cur, student_id, uni_id)}


# Method called to help a student identify if joining an event will create a time conflict.
@app.get("/hasConflict/")
def hasConflict(startTime, endTime, studentID):
    return {"result": events.has_conflict(cur, startTime, endTime, studentID)}
 

@app.put("/saveMessage/")
def saveMessage(sender_id, chatroomID, message_sent):
    return {"result": chatroom.saveMessage(cur, sender_id, chatroomID, message_sent)}


@app.get("/retrieveMessages/")
def retrieveMessages(chatroom_id):
    return {"result": chatroom.retrieveMessages(cur, chatroom_id)}

@app.get("/importStudentSchedule/")
def importStudentSchedule(email):
    return {"result": schedule.request_schedule(cur,email)}

@app.get("/importStudentProfile/")
def importStudentProfile(email):
    return {"result":profiles.request_profile(cur,email)}

@app.post("/verifyIdentity/")
def verifyIdentity(student_id, uni_id, email, fname, lname, graduation_year):
    return {"result": verify_identity.verifyIdentity(cur, student_id, uni_id, email, fname, lname, graduation_year)}


@app.post("/createFlashcard/")
def createFlashcard(chatroom_id, front_text, back_text):
    return {"result": flashcard.createFlashcard(cur, chatroom_id, front_text, back_text)}


@app.delete("/deleteFlashcard/")
def deleteFlashcard(chatroom_id, front_text, back_text):
    return {"result": flashcard.deleteFlashcard(cur, chatroom_id, front_text, back_text)}


@app.get("/getFlashcards/")
def getAllFlashcards(chatroom_id):
    return {"result": flashcard.getFlashcards(cur, chatroom_id)}

# Method called to get a student's verification status.
@app.get("/getVerificationStatus/")
def getVerificationStatus(email):
    return identity.retrieve_verification_status(cur,email)

# Test function to send random data.
@app.get("/test/")
def test(data):
    print(data)
    if int(data) % 2 == 0:
        return {"result":True}
    return {"result":False}