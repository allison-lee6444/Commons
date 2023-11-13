import json
from fastapi import HTTPException
from cursor import cur,serialize_datetime
import datetime

# Check if a specific chatroom has had any new messages since the provided time.
def get_msg_update(chatroom_id, date_time):
    try:
        cur.execute("SELECT * FROM message WHERE chatroom_id = %(chatroom_id)s and date_time_sent > %(date_time)s",
                    {"chatroom_id": chatroom_id, "date_time": date_time})
        result = json.dumps(cur.fetchall(),default=serialize_datetime)
        return result
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )

# Retrieve message functionality
def retrieveMessages(chatroom_id):
    cur.execute("SELECT * FROM message WHERE chatroom_id= %(chatroom_id)s", {"chatroom_id" : chatroom_id})
    result = json.dumps(cur.fetchall(),default=serialize_datetime)
    return result

# Save message functionality.
def saveMessage(sender_id, chatroomID, message_sent):
    try:
        date_time_sent = datetime.datetime.now()
        cur.execute(
            "INSERT INTO message(sender_id, chatroom_id, message_text, date_time_sent)" 
            "VALUES(%(sender_id)s, %(chatroomID)s, %(message_sent)s, %(date_time_sent)s)", 
            {"sender_id" : sender_id, "chatroomID" : chatroomID, "message_sent" : message_sent, "date_time_sent" : date_time_sent}
        )
        return True
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    
# Retrieve all of the chatrooms a student is in.
# WARNING: DOES NOT WORK CURRENTLY AS THERE IS NO WAY TO STORE CHATROOM NAME IN THE DATABASE.  TEST ONLY
# WHEN THIS IS FIXED.
def getChatrooms(student_id):
    try:
        cur.execute(
            "SELECT chatroom.id,chatroom.chatroom_name FROM in_chatroom LEFT JOIN chatroom ON"
            "in_chatroom.chatroom_id = chatroom.id WHERE in_chatroom.student_id = %(student_id)s",{'student_id':student_id}
        )
        result = cur.fetchall()
        return {"chatrooms":result}
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )