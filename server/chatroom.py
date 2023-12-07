import json
from fastapi import HTTPException
import datetime

import string
import random



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
def retrieve_messages(cur, chatroom_id):
    try:
        cur.execute("SELECT (sender_id, email, fname, lname, chatroom_id, message_text, cast(date_time_sent as text)) FROM message JOIN student ON student_id = sender_id WHERE chatroom_id= %(chatroom_id)s",
                     {"chatroom_id": chatroom_id})
        result = json.dumps(cur.fetchall())
        
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    cur.execute("COMMIT")
    return result


# Save message functionality
def save_message(cur, sender_id, chatroomID, message_sent):
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
def create_chatroom(cur, user_id, chatroom_name, uni_id):
    try: 
        cur.execute("INSERT INTO chatroom(chatroom_name, uni_id) VALUES(%(chatroom_name)s, %(uni_id)s)", {"chatroom_name" : chatroom_name, "uni_id" : uni_id})
        
        #cur.execute("SELECT id FROM chatroom where chatroom_name = %(chatroom_name)s   AND uni_id = %(uni_id)s", {"chatroom_name" : chatroom_name, "uni_id" : uni_id})
        cur.execute("SELECT count(*) FROM chatroom")

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
    
#Generate invite link for student (for non-course chatroom)
def generate_invite(cur, target_user_id, invite_sender_id, chatroom_id, uni_id):
    try:

        #Generate invite id
        invite_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        #Check to make sure that the invite_id doesn't already exist in the db
        cur.execute("SELECT invite_id FROM invite")
        res = cur.fetchall()
        res = [x[0] for x in res]
        #keep regenerating the invite id until you get something that doesn't exist in the db
        while (invite_id in res):
            invite_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            cur.execute("SELECT invite_id FROM invite")
            res = cur.fetchall()
            res = [x[0] for x in res]

        
        #make sure that the university actually exists in the database
        cur.execute("SELECT id FROM university where id = %(uni_id)s", {"uni_id" : uni_id})
        res = cur.fetchall()[0][0]
        if (res != uni_id):
            raise HTTPException(
            status_code=500,
            detail="This university is not registered in our database",
        )
        
        cur.execute("""SELECT s.student_id, t.student_id FROM student s JOIN in_chatroom ic ON s.student_id = ic.student_id JOIN university u ON s.uni_id = u.id
        JOIN chatroom c ON ic.chatroom_id = c.id, student t WHERE s.student_id = %(sender_id)s AND t.student_id = %(target_id)s AND ic.chatroom_id = %(chatroom_id)s
        AND c.course_id IS NULL and s.uni_id=t.uni_id""", {"sender_id" : invite_sender_id, "target_id" : target_user_id, "chatroom_id" : chatroom_id})
        res = cur.fetchall()[0][0]
        if (res == None or res == []):
            raise HTTPException(
            status_code=500,
            detail="Database error",
        )
        
        #make sure that the chatroom is not a course chatroom
        cur.execute("SELECT course_id FROM chatroom WHERE id = %(chatroom_id)s", {"chatroom_id" : chatroom_id})
        c_id = cur.fetchall()[0][0]
        if (c_id != None):
            raise HTTPException(
            status_code=500,
            detail="Creating an invite for a course chatroom is not allowed",
        )
        
        cur.execute("INSERT INTO invite values(%(invite_id)s, %(chatroom_id)s, %(invite_sender_id)s, %(target_user_id)s, %(uni_id)s)",
                    {"invite_id" : invite_id, "chatroom_id" : chatroom_id, "invite_sender_id" : invite_sender_id, "target_user_id" : target_user_id, "uni_id" : uni_id})
        
        
        return True

    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )

#Accept an invite and join a (non-course) chatroom
def accept_invite(cur, invite_id, target_user_id):
    try:
        
        #get target user of invite, check to see if it matches target_user_id parameter
        """
        cur.execute("SELECT target_user_id FROM invite WHERE invite_id=%(invite_id)s", {"invite_id" : invite_id})
        res = cur.fetchall()[0][0]
        if (res != target_user_id):
            raise HTTPException(status_code=500, detail="The invite is not for this user")
        """
        
        #cur.execute("SELECT id FROM chatroom WHERE invite_id = %(invite_id)s", {"invite_id" : invite_id})
        #cur.execute("SELECT chatroom_id FROM invite WHERE invite_id=%(invite_id)s", {"invite_id" : invite_id})
        cur.execute("SELECT invite.chatroom_id FROM chatroom JOIN invite on chatroom.id = invite.chatroom_id WHERE invite_id = %(invite_id)s AND target_user_id=%(target_user_id)s",
                    {"invite_id" : invite_id, "target_user_id" : target_user_id})
        chatroom_id = cur.fetchall()[0][0]
        if (chatroom_id == None or chatroom_id == [] or chatroom_id == ''):
            raise HTTPException(status_code=500, detail="either the chatroom does not exist or this invite is for a different user")

        

        #do not allow insertion of user into in_chatroom if uni_id for target user and chatroom do not match
        #cur.execute("SELECT uni_id FROM chatroom WHERE id = %(chatroom_id)s", {"chatroom_id" : chatroom_id})
        #uni_id = cur.fetchall()[0][0]
        #cur.execute("SELECT uni_id FROM student WHERE student_id = %(target_user_id)s", {"target_user_id" : target_user_id})
        
        cur.execute("SELECT chatroom_id FROM student JOIN invite on student.uni_id = (SELECT uni_id FROM chatroom WHERE chatroom.id = invite.chatroom_id)")
        student_chrm_id = cur.fetchall()[0][0]
        
        if (student_chrm_id != chatroom_id): #uni_id):
            raise HTTPException(status_code=500, detail="The university of the invitee does not match the university of the chatroom")
        
        #insert target user into in_chatroom
        cur.execute("INSERT INTO in_chatroom(student_id, uni_id, chatroom_id) VALUES(%(target_user_id)s, (SELECT uni_id FROM chatroom WHERE id = %(chatroom_id)s), %(chatroom_id)s)",
                    {"target_user_id" : target_user_id, "chatroom_id" : chatroom_id})
        
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
