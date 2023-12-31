import asyncio
import datetime
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
processed_requests = {
    'saveMessage': {},
    'createChatroom': {},
    'createEvent': {},
    'editEvent': {}
}
name_cache = {}


def check_session_id(id):
    if id in sessions:
        return sessions[id]
    else:
        return None


def cleanup_processed_requests(req):
    now = datetime.datetime.now()
    for k, v in req.items():
        if v - now > datetime.timedelta(seconds=10):
            del req[k]


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
@app.post("/createEvent/")
def createEvent(sessionid, chatroomID, eventName, description, locName, locCoord, startTime, endTime):
    email = check_session_id(sessionid)
    # check authorization using email and convert host id
    host_id, uni_id = profiles.get_student_uni_id(cur, email)
    if (sessionid, email, host_id, uni_id, eventName, chatroomID) in processed_requests[
        'createEvent']:  # idempotency protection
        return {"result": False}
    processed_requests['createEvent'][
        (sessionid, email, host_id, uni_id, eventName, chatroomID)] = datetime.datetime.now()
    return {
        "result":
            events.create_event(cur, chatroomID, eventName, host_id, uni_id, description, locName, locCoord, startTime,
                                endTime)
    }


# Method to edit an event.
@app.put('/editEvent')
def editEvent(sessionid, event_name, description, loc_name, loc_coords, start_time, end_time, event_id):
    email = check_session_id(sessionid)
    # check authorization using email and convert host id
    host_id, uni_id = profiles.get_student_uni_id(cur, email)
    if (sessionid, email, host_id, uni_id, event_name) in processed_requests[
        'createEvent']:  # idempotency protection
        return {"result": False}
    processed_requests['editEvent'][
        (sessionid, email, host_id, uni_id, event_name)] = datetime.datetime.now()
    return events.edit_event(cur, event_name, host_id, uni_id, description, loc_name, loc_coords,
                             start_time,
                             end_time, event_id)


# Method called when a student joins a event.
@app.put("/joinEvent/")
def joinEvent(sessionid, eventID):
    email = check_session_id(sessionid)
    student_id, uni_id = profiles.get_student_uni_id(cur, email)
    return {"result": events.join_event(cur, eventID, student_id, uni_id)}


# Method called when a student leaves an event.
@app.put("/leaveEvent/")
def leaveEvent(sessionid, eventID):
    email = check_session_id(sessionid)
    student_id, _ = profiles.get_student_uni_id(cur, email)
    return {"result": events.leave_event(cur, student_id, eventID)}


# Method called when the host of an event cancels the event.
@app.delete("/cancelEvent/")
def cancelEvent(sessionid, eventID):
    email = check_session_id(sessionid)
    hostID, _ = profiles.get_student_uni_id(cur, email)
    return {"result": events.cancel_event(cur, hostID, eventID)}


# Method called to get event info of one event given event id
@app.get("/getEvent/")
def getEvent(sessionid, eventID):
    email = check_session_id(sessionid)
    student_id, uni_id = profiles.get_student_uni_id(cur, email)
    return {"result": events.get_event(cur, eventID, student_id, uni_id)}


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
def hasConflict(sessionid, startTime, endTime, event_id):
    email = check_session_id(sessionid)
    student_id, _ = profiles.get_student_uni_id(cur, email)
    return {"result": events.has_conflict(cur, startTime, endTime, student_id, event_id)}


@app.put("/saveMessage/")
def saveMessage(sessionid, chatroomID, message_sent, message_id):
    email = check_session_id(sessionid)
    student_id, _ = profiles.get_student_uni_id(cur, email)
    if message_id in processed_requests['saveMessage']:  # idempotency protection
        return {"result": False}
    processed_requests['saveMessage'][message_id] = datetime.datetime.now()
    cleanup_processed_requests(processed_requests['saveMessage'])
    return {"result": chatroom.save_message(cur, student_id, chatroomID, message_sent)}


@app.get("/retrieveMessages/")
def retrieveMessages(chatroomID):
    return {"result": chatroom.retrieve_messages(cur, chatroomID)}


@app.get("/importStudentSchedule/")
def importStudentSchedule(email):
    return {"result": request_uni.request_schedule(cur, email)}


@app.get("/importStudentProfile/")
def importStudentProfile(email):
    return {"result": request_uni.request_profile(cur, email)}


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


@app.get("/getName/")
def getName(email):
    if email in name_cache:
        return name_cache[email]
    name = profiles.get_profile(cur, email)['result'][0][-2:]
    name_cache[email] = name
    return name


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


@app.post("/createFlashcard/")
def createFlashcard(chatroom_id, front_text, back_text):
    return {"result": flashcard.createFlashcard(cur, chatroom_id, front_text, back_text)}


@app.delete("/deleteFlashcard/")
def deleteFlashcard(chatroom_id, front_text, back_text):
    return {"result": flashcard.deleteFlashcard(cur, chatroom_id, front_text, back_text)}


@app.get("/getFlashcards/")
def getAllFlashcards(chatroom_id):
    return {"result": flashcard.getFlashcards(cur, chatroom_id)}


@app.post("/generateInvite")
def generateInvite(session_id, target_user_email, chatroom_id):
    email = check_session_id(session_id)
    sender_id, uni_id = profiles.get_student_uni_id(cur, email)
    try:
        target_user_id, uni_id = profiles.get_student_uni_id(cur, target_user_email)
    except BaseException:
        print(f'Exception: Invalid email address for invite target')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    return {"result": chatroom.generate_invite(cur, target_user_id, sender_id, chatroom_id, uni_id)}


@app.post("/acceptInvite")
def acceptInvite(sessionid, invite_id):
    email = check_session_id(sessionid)
    target_user_id, _ = profiles.get_student_uni_id(cur, email)
    return {"result": chatroom.accept_invite(cur, invite_id, target_user_id)}


@app.put("/createChatroom")
def createChatroom(sessionid, chatroom_name):
    email = check_session_id(sessionid)
    if (sessionid, chatroom_name) in processed_requests['createChatroom']:  # idempotency protection
        return {"result": False}
    processed_requests['createChatroom'][(sessionid, chatroom_name)] = datetime.datetime.now()
    cleanup_processed_requests(processed_requests['createChatroom'])

    user_id, uni_id = profiles.get_student_uni_id(cur, email)
    return {"result": chatroom.create_chatroom(cur, user_id, chatroom_name, uni_id)}


# Method called to get a student's verification status.
@app.get("/getVerificationStatus/")
def getVerificationStatus(sessionid):
    email = check_session_id(sessionid)
    return profiles.is_verified(cur, email)


# Method called to get a list events in a chatroom.
@app.get("/getChatroomEvents")
def getChatroomEvents(chatroomID):
    return chatroom.get_chatroom_events(cur, chatroomID)


# Test function to send random data.
@app.get("/test/")
def test(data):
    print(data)
    if int(data) % 2 == 0:
        return {"result": True}
    return {"result": False}
