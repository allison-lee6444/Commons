import json
from fastapi import HTTPException
import datetime


def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()


# Check if a specific chatroom has had any new messages since the provided time.
def get_msg_update(cur, chatroom_id, date_time):
    try:
        cur.execute("SELECT * FROM message WHERE chatroom_id = %(chatroom_id)s and date_time_sent > %(date_time)s",
                    {"chatroom_id": chatroom_id, "date_time": date_time})
        result = json.dumps(cur.fetchall(), default=serialize_datetime)
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
        cur.execute("SELECT sender_id, chatroom_id, message_text, date_time_sent, fname, lname, email "
                    "FROM message JOIN student ON (sender_id = student_id) WHERE chatroom_id=%(chatroom_id)s"
                    , {"chatroom_id": chatroom_id})
        result = json.dumps(cur.fetchall(), default=serialize_datetime)
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    cur.execute("COMMIT")
    return result


# Save message functionality
def saveMessage(cur, sender_id, chatroomID, message_sent):
    try:
        date_time_sent = datetime.datetime.now()
        cur.execute(
            "INSERT INTO message(sender_id, chatroom_id, message_text, date_time_sent) VALUES(%(sender_id)s, %(chatroomID)s, %(message_sent)s, %(date_time_sent)s)",
            {"sender_id": sender_id, "chatroomID": chatroomID, "message_sent": message_sent,
             "date_time_sent": date_time_sent})
        cur.execute("COMMIT")
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
        cur.execute("INSERT INTO chatroom(chatroom_name, uni_id) VALUES(%(chatroom_name)s, %(uni_id)s)",
                    {"chatroom_name": chatroom_name, "uni_id": uni_id})
        cur.execute("SELECT id FROM chatroom where chatroom_name = %(chatroom_name)s   AND uni_id = %(uni_id)s",
                    {"chatroom_name": chatroom_name, "uni_id": uni_id})
        chatroom_id = cur.fetchall()[0][0]
        cur.execute(
            "INSERT INTO in_chatroom(student_id, uni_id, chatroom_id) VALUES(%(user_id)s, %(uni_id)s, %(chatroom_id)s)",
            {"user_id": user_id, "uni_id": uni_id, "chatroom_id": chatroom_id})
        cur.execute("COMMIT")
        return True
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


def getChatrooms(cur, student_id, uni_id):
    try:
        cur.execute(
            "SELECT chatroom.id,chatroom.chatroom_name FROM in_chatroom LEFT JOIN chatroom ON "
            "in_chatroom.chatroom_id = chatroom.id WHERE in_chatroom.student_id = %(student_id)s AND "
            "in_chatroom.uni_id = %(uni_id)s",
            {'student_id': student_id, 'uni_id': uni_id}
        )
        result = cur.fetchall()
        return {"chatrooms": result}
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
