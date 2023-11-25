import json

from fastapi import HTTPException
import datetime
from cursor import cur

import string
import random


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
    try:
        date_time_sent = datetime.now()
        cur.execute("INSERT INTO message(sender_id, chatroom_id, message_text, date_time_sent) VALUES(%(sender_id)s, %(chatroomID)s, %(message_sent)s, %(date_time_sent)s)", {"sender_id" : sender_id, "chatroomID" : chatroomID, "message_sent" : message_sent, "date_time_sent" : date_time_sent})
        return True
    except:
        return False

#Create non-course chatroom
def createChatroom(user_id, chatroom_name, uni_id):
    try:
        # Generate invite id
        invite_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


        cur.execute("INSERT INTO chatroom(chatroom_name, invite_id, uni_id) VALUES(%(chatroom_name)s, %(invite_id)s %(uni_id)s)", {"chatroom_name" : chatroom_name, "uni_id" : uni_id, "invite_id" : invite_id})
        cur.execute("SELECT id FROM chatroom where chatroom_name = %(chatroom_name)s   AND uni_id = %(uni_id)s", {"chatroom_name" : chatroom_name, "uni_id" : uni_id})
        chatroom_id = cur.fetchall()[0][0]
        cur.execute("INSERT INTO in_chatroom(student_id, uni_id, chatroom_id) VALUES(%(user_id)s, %(uni_id)s, %(chatroom_id)s)", {"user_id" : user_id, "uni_id" : uni_id, "chatroom_id" : chatroom_id})
        return True
    except:
        return False
    
#Generate invite link for student (for non-course chatroom)
def GenerateInvite(target_user_id, chatroom_id):
    invite_object = {}
    invite_object.update({"target_user" : target_user_id})

    cur.execute("SELECT invite_id FROM chatroom WHERE id = %(chatroom_id)s", {"chatroom_id" : chatroom_id})
    invite_id = cur.fetchall()[0][0]
    invite_object.update({"invite_id" : invite_id})

    return json.dumps(invite_object)

