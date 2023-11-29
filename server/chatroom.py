import json

from fastapi import HTTPException
import datetime

import string
import random


# Check if a specific chatroom has had any new messages since the provided time.
def get_msg_update(cur, chatroom_id, date_time):
    try:
        cur.execute("SELECT * FROM message WHERE chatroom_id = %(chatroom_id)s and date_time_sent > %(date_time)s",
                    {"chatroom_id": chatroom_id, "date_time": date_time})
        result = json.dumps(cur.fetchall())
        return result
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# Retrieve message functionality
def retrieveMessages(cur, chatroom_id):
    try:
        cur.execute("SELECT (sender_id, chatroom_id, message_text, cast(date_time_sent as text)) FROM message WHERE chatroom_id= %(chatroom_id)s",
                     {"chatroom_id": chatroom_id})
        result = json.dumps(cur.fetchall())
        return result
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# Save message functionality
def saveMessage(cur, sender_id, chatroomID, message_sent):
    try:
        date_time_sent = datetime.datetime.now()
        cur.execute(
            "INSERT INTO message(sender_id, chatroom_id, message_text, date_time_sent) VALUES(%(sender_id)s, %(chatroomID)s, %(message_sent)s, %(date_time_sent)s)",
            {"sender_id": sender_id, "chatroomID": chatroomID, "message_sent": message_sent,
             "date_time_sent": date_time_sent})
        return True
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# Create non-course chatroom
def createChatroom(cur, user_id, chatroom_name, uni_id):
    try:
        # Generate invite id
        invite_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        cur.execute("INSERT INTO chatroom(chatroom_name, uni_id, invite_id) VALUES(%(chatroom_name)s, %(uni_id)s, %(invite_id)s)", {"chatroom_name" : chatroom_name, "uni_id" : uni_id, "invite_id" : invite_id})
        
        cur.execute("SELECT id FROM chatroom where chatroom_name = %(chatroom_name)s   AND uni_id = %(uni_id)s", {"chatroom_name" : chatroom_name, "uni_id" : uni_id})
        
        chatroom_id = cur.fetchall()[0][0]
        
        cur.execute(
            "INSERT INTO in_chatroom(student_id, uni_id, chatroom_id) VALUES(%(user_id)s, %(uni_id)s, %(chatroom_id)s)",
            {"user_id": user_id, "uni_id": uni_id, "chatroom_id": chatroom_id})
        
        return True
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    
#Generate invite link for student (for non-course chatroom)
def GenerateInvite(cur, target_user_id, chatroom_id):
    try:
        invite_object = {}
        invite_object.update({"target_user" : target_user_id})
        cur.execute("SELECT invite_id FROM chatroom WHERE id = %(chatroom_id)s", {"chatroom_id" : chatroom_id})
        invite_id = cur.fetchall()[0][0]
        invite_object.update({"invite_id" : invite_id})
        return json.dumps(invite_object)
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )

#Accept an invite and join a (non-course) chatroom
def AcceptInvite(cur, invite_object, target_user_id):
    try:
        invite = json.loads(invite_object)

        
        #check if target_user_id matches invite["target_user"]
        if (target_user_id != invite["target_user"]):
            return False
        
        invite_id = invite["invite_id"]
        
        cur.execute("SELECT id FROM chatroom WHERE invite_id = %(invite_id)s", {"invite_id" : invite_id})
        chatroom_id = cur.fetchall()[0][0]
        
        #do not allow insertion of user into in_chatroom if uni_id for target user and chatroom do not match
        cur.execute("SELECT uni_id FROM chatroom WHERE id = %(chatroom_id)s", {"chatroom_id" : chatroom_id})
        uni_id = cur.fetchall()[0][0]
        cur.execute("SELECT uni_id FROM student WHERE student_id = %(target_user_id)s", {"target_user_id" : target_user_id})
    
        student_uni_id = cur.fetchall()[0][0]
        
        if (student_uni_id != uni_id):
            return False
        
        #insert target user into in_chatroom
        cur.execute("INSERT INTO in_chatroom(student_id, uni_id, chatroom_id) VALUES(%(target_user_id)s, %(uni_id)s, %(chatroom_id)s)",
                    {"target_user_id" : target_user_id, "uni_id" : uni_id, "chatroom_id" : chatroom_id})
        
        return True
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )

# Get the list of chatrooms that a student is in (for visibility of chatrooms functionality)
def getChatroomsForStudent(cur, student_id):
    try:
        cur.execute("SELECT chatroom_name FROM (in_chatroom JOIN chatroom ON chatroom_id = id) WHERE student_id = %(student_id)s",
                     {"student_id" : student_id})
        #cur.execute("SELECT chatroom_name FROM chatroom")
        res = cur.fetchall()
        chatroom_names = [x[0] for x in res]
        chatrooms = {"chatrooms" : chatroom_names}
        return(json.dumps(chatrooms))
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )