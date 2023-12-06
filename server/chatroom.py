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
def retrieve_messages(cur, chatroom_id):
    try:
        cur.execute("SELECT (sender_id, email, fname, lname, chatroom_id, message_text, cast(date_time_sent as text)) FROM message JOIN student ON student_id = sender_id WHERE chatroom_id= %(chatroom_id)s",
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
def save_message(cur, sender_id, chatroomID, message_sent):
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
def create_chatroom(cur, user_id, chatroom_name, uni_id):
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
def generate_invite(cur, target_user_id, invite_sender_id, chatroom_id, uni_id):
    try:

        #Generate invite id
        invite_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        #make sure that the university actually exists in the database
        cur.execute("SELECT id FROM university where id = %(uni_id)s", {"uni_id" : uni_id})
        res = cur.fetchall()[0][0]
        if (res != uni_id):
            raise HTTPException(
            status_code=500,
            detail="This university is not registered in our database",
        )
        
        #make sure that the invite sender is actually in the chatroom
        cur.execute("SELECT chatroom_id FROM in_chatroom WHERE student_id = %(invite_sender_id)s", {"invite_sender_id" : invite_sender_id})
        res = cur.fetchall()#[0][0]
        res = [x[0] for x in res]
        if (chatroom_id not in res):
            raise HTTPException(status_code=500, detail="The sender of the invite is not in the chatroom!")
        
        #make sure that target_user_id exists in the student database
        cur.execute("SELECT student_id FROM student")
        res = cur.fetchall()
        res = [str(x[0]) for x in res]
        if (str(target_user_id) not in res):
            raise HTTPException(status_code=500, detail="The invitee is not a registered user on our platform!")


        #make sure that the uni_id of target_user_id matches
        # the paramter uni_id and the uni_id of chatroom_id

        cur.execute("SELECT uni_id FROM student WHERE student_id = %(target_user_id)s", {"target_user_id" : target_user_id})
        res = cur.fetchall()[0][0]
        if (res != uni_id):
            raise HTTPException(status_code=500, detail="uni_id mismatch")
        cur.execute("SELECT uni_id FROM in_chatroom where chatroom_id = %(chatroom_id)s", {"chatroom_id" : chatroom_id})
        res = cur.fetchall()[0][0]
        if (res != uni_id):
            raise HTTPException(status_code=500, detail="uni_id mismatch")
        
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
        #make sure the target user is verified
        cur.execute("SELECT student_id FROM student WHERE student_id = %(target_user_id)s",
                    {"target_user_id" : target_user_id})
        res = cur.fetchall()[0][0]
        if (res != target_user_id):
            raise HTTPException(status_code=500, detail="Student not verified!")
        
        #get target user of invite, check to see if it matches target_user_id parameter
        cur.execute("SELECT target_user_id FROM invite WHERE invite_id=%(invite_id)s", {"invite_id" : invite_id})
        res = cur.fetchall()[0][0]
        if (res != target_user_id):
            raise HTTPException(status_code=500, detail="The invite is not for this user")

        
        cur.execute("SELECT id FROM chatroom WHERE invite_id = %(invite_id)s", {"invite_id" : invite_id})
        chatroom_id = cur.fetchall()[0][0]
        
        #do not allow insertion of user into in_chatroom if uni_id for target user and chatroom do not match
        cur.execute("SELECT uni_id FROM chatroom WHERE id = %(chatroom_id)s", {"chatroom_id" : chatroom_id})
        uni_id = cur.fetchall()[0][0]
        cur.execute("SELECT uni_id FROM student WHERE student_id = %(target_user_id)s", {"target_user_id" : target_user_id})
    
        student_uni_id = cur.fetchall()[0][0]
        
        if (student_uni_id != uni_id):
            raise HTTPException(status_code=500, detail="The university of the invitee does not match the university of the chatroom")
        
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
def get_chatrooms_for_student(cur, student_id):
    try:
        """
        cur.execute("SELECT chatroom_name FROM (in_chatroom JOIN chatroom ON chatroom_id = id) WHERE student_id = %(student_id)s",
                     {"student_id" : student_id})
        """
        cur.execute("SELECT (chatroom_name, chatroom.id) FROM (in_chatroom JOIN chatroom ON chatroom_id = id) WHERE student_id = %(student_id)s",
                     {"student_id" : student_id})
        #cur.execute("SELECT chatroom_name FROM chatroom")
        res = cur.fetchall()
        chatroom_names = [x[0][0] for x in res]
        chatroom_ids = [x[0][1] for x in res]
        chatrooms = {"chatroom_names" : chatroom_names, "chatroom_ids" : chatroom_ids}
        return(json.dumps(chatrooms))
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )