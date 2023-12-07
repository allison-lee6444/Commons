import asyncio
import secrets

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# Backend Functions
import authentication
import chatroom
import events
import profiles
import request_uni
import verification
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


@app.get("/getChatroom/")
def getChatroom(sessionid):
    email = check_session_id(sessionid)
    student_id, uni_id = profiles.get_student_uni_id(cur, email)
    return chatroom.getChatrooms(cur, student_id, uni_id)


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
def hasConflict(sessionid, startTime, endTime):
    email = check_session_id(sessionid)
    student_id, _ = profiles.get_student_uni_id(cur, email)
    return {"result": events.has_conflict(cur, startTime, endTime, student_id)}


@app.put("/saveMessage/")
def saveMessage(sessionid, chatroomID, message_sent):
    email = check_session_id(sessionid)
    student_id, _ = profiles.get_student_uni_id(cur, email)
    return {"result": chatroom.saveMessage(cur, student_id, chatroomID, message_sent)}


@app.get("/retrieveMessages/")
def retrieveMessages(chatroomID):
    return {"result": chatroom.retrieveMessages(cur, chatroomID)}


@app.get("/importStudentSchedule/")
def importStudentSchedule(email):
    return {"result": request_uni.request_schedule(cur, email)}


@app.get("/importStudentProfile/")
def importStudentProfile(email):
    return {"result": request_uni.request_profile(cur, email)}

#"""
@app.post("/verifyIdentity/")
def verifyIdentity(sessionid):
    email = check_session_id(sessionid)
    if getVerificationStatus(sessionid)['verified']:
        return {'result': False}
    return {"result": asyncio.run(verification.start_verify(email))}


@app.get("/checkVerificationCode/")
def checkVerificationCode(sessionid, token):
    if getVerificationStatus(sessionid)['verified']:
        return {'result': False}
    email = check_session_id(sessionid)
    is_verified = verification.check_token(email, token)
    if is_verified:
        request_uni.request_schedule(cur, email)
        request_uni.request_profile(cur, email)
    return {"result": is_verified}
#"""

@app.post("/createFlashcard/")
def createFlashcard(chatroom_id, front_text, back_text):
    return {"result": flashcard.createFlashcard(cur, chatroom_id, front_text, back_text)}


@app.delete("/deleteFlashcard/")
def deleteFlashcard(chatroom_id, front_text, back_text):
    return {"result": flashcard.deleteFlashcard(cur, chatroom_id, front_text, back_text)}


@app.get("/getFlashcards/")
def getAllFlashcards(chatroom_id):
    return {"result": flashcard.getFlashcards(cur, chatroom_id)}

@app.get("/generateInvite")
def generateInviteForStudent(target_user_id, chatroom_id):
    return {"result": chatroom.generate_invite(cur, target_user_id, chatroom_id)}

@app.post("/acceptInvite")
def acceptInvite(invite_object, target_user_id):
    return {"result":chatroom.accept_invite(cur, invite_object, target_user_id)}

@app.put("/createChatroom")
def createChatroom(user_id, chatroom_name, uni_id):
    return {"result" : chatroom.create_chatroom(cur, user_id, chatroom_name, uni_id)}

@app.get("/getChatroomsForStudent")
def getChatroomsForStudent(student_id):
    return {"result" : chatroom.get_chatrooms_for_student(cur, student_id)}


# Method called to get a student's verification status.
@app.get("/getVerificationStatus/")
def getVerificationStatus(sessionid):
    email = check_session_id(sessionid)
    return profiles.is_verified(cur, email)


# Test function to send random data.
@app.get("/test/")
def test(data):
    print(data)
    if int(data) % 2 == 0:
        return {"result": True}
    return {"result": False}
