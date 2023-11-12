import json

from fastapi import HTTPException
import datetime
from cursor import cur


# Check if a specific chatroom has had any new messages since the provided time.
def get_msg_update(chatroom_id, date_time):
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
    

#Retrieve message functionality
def retrieveMessages(chatroom_id):
    cur.execute("SELECT * FROM messages WHERE chatroom_id= %(chatroom_id)s", {"chatroom_id" : chatroom_id})
    result = json.dumps(cur.fetchall())
    return result

#Save message functionality
def saveMessage(sender_id, chatroomID, message_sent):
    date_time_sent = datetime.now()
    cur.execute("INSERT INTO message(sender_id, chatroom_id, message_text, date_time_sent) VALUES(%(sender_id)s, %(chatroomID)s, %(message_sent)s, %(date_time_sent)s)", {"sender_id" : sender_id, "chatroomID" : chatroomID, "message_sent" : message_sent, "date_time_sent" : date_time_sent})
    result = json.dumps(cur.fetchall())
    return result