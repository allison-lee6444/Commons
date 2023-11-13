import secrets

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# Backend Functions
import authentication
import chatroom
import events
import profiles
import identity
import schedule

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
    result = authentication.check_login(email, password)
    token = None
    print(result)
    if result:
        token = secrets.token_urlsafe(20)
        sessions[token] = email
    return {"result": result, "sessionid": token}


# Method to handle new user registration.
@app.post("/register/")
def register(email, password):
    result = authentication.register_account(email, password)
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
    return {"result": authentication.change_password(email, current_pw, new_pw)}


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
        "result": profiles.edit_profile(email, hobbies, interests, fname, lname, new_email)}


# Method to retrieve data of a student profile for a particular student
@app.get("/getProfile/")
def getProfile(sessionid):
    email = check_session_id(sessionid)
    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid session ID",
        )
    return profiles.get_profile(email)


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
    return chatroom.get_msg_update(chatroomID, dateTime)

@app.put("/saveMessage/")
def saveMessage(sender_id, chatroomID, message_sent):
    return {"result" : chatroom.saveMessage(sender_id, chatroomID, message_sent)}

@app.get("/retrieveMessages/")
def retrieveMessages(chatroom_id):
    return {"result" : chatroom.retrieveMessages(chatroom_id)}

@app.get("/retrieveChatrooms")
def retrieveChatrooms(student_id):
    return chatroom.getChatrooms(student_id)

# Method to create a new event and save it in the DB.
@app.post("/scheduleNewEvent/")
def scheduleNewEvent(eventName, hostID, uniID, description, locName, locCoord, startTime, endTime):
    return {
        "result": events.create_event(eventName, hostID, uniID, description, locName, locCoord, startTime, endTime)
    }


# Method called when a student joins a event.
@app.put("/joinEvent/")
def joinEvent(eventID, studentID, chatroomID):
    return {"result": events.join_event(eventID, studentID, chatroomID)}


# Method called when a student leaves an event.
@app.put("/leaveEvent/")
def leaveEvent(studentID, eventID):
    return {"result": events.delete_event(studentID, eventID)}


# Method called when the host of an event cancels the event.
@app.delete("/cancelEvent/")
def cancelEvent(hostID, eventID):
    return {"result": events.cancel_event(hostID, eventID)}


# Method called to get all events a student is a part of.
@app.get("/getEvents/")
def getEvents(studentID):
    return {"result": events.get_event(studentID)}


# Method called to get all courses a student is in.
@app.get("/getCourses/")
def getCourses(studentID):
    return {"result": events.get_courses(studentID)}


# Method called to help a student identify if joining an event will create a time conflict.
@app.get("/hasConflict/")
def hasConflict(startTime, endTime, studentID):
    return {"result": events.has_conflict(startTime, endTime, studentID)}

# Method called to verify if a email is a university email.
@app.get("/universityEmailVerification")
def universityEmailVerification(email):
    return identity.verify_uni_email(email)

# Method called to get a student's verification status.
@app.get("/getVerificationStatus/")
def getVerificationStatus(email):
    return identity.retrieve_verification_status(email)

# Method called to import a student's schedule directly from the university.
@app.get("/importStudentSchedule/")
def importStudentSchedule(email):
    return {"success":schedule.request_schedule(email)}

# Method called to import a student's profile directly from the university.
@app.get("/importStudentProfile/")
def importStudentSchedule(email):
    return {"success":profiles.request_profile(email)}

# Test function to send random data.
@app.get("/test/")
def test(data):
    print(data)
    if int(data) % 2 == 0:
        return {"result":True}
    return {"result":False}

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
