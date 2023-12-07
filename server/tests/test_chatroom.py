from server import chatroom
import random
import string
import datetime
import json

from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql", "database/triggers.sql"],
)
postgresql = factories.postgresql("postgresql_proc")

def test_create_chatroom_func(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO student(email, password, salt, student_id) VALUES('a', 'a', 'a', '123')")
    cur.execute("INSERT INTO university values('NYU')")

    chatroom.create_chatroom(cur, '123', 'some_chatroom', 'NYU')

    #cur.execute("SELECT invite_id FROM chatroom")
    #invite_id = (cur.fetchall()[0][0])
    #assert (invite_id != '')

    cur.execute("SELECT chatroom_name FROM chatroom")
    name = cur.fetchall()[0][0]
    assert (name == 'some_chatroom')
      
    #assert(chatroom.createChatroom(cur, '123', 'some_chatroom', 'NYU')==True)
    
def test_retrieve_messages(postgresql):
    cur = postgresql.cursor()

    cur.execute("INSERT INTO student(email, password, salt, student_id) VALUES('a', 'a', 'a', '123')")
    cur.execute("INSERT INTO university values('NYU')")
    chatroom_name = 'a'
    uni_id = 'NYU'
    cur.execute("INSERT INTO chatroom(chatroom_name, uni_id) VALUES(%(chatroom_name)s, %(uni_id)s)", {"chatroom_name" : chatroom_name, "uni_id" : uni_id})
    
    #get chatroom id
    cur.execute("SELECT id FROM chatroom")
    chatroom_id = cur.fetchall()[0][0]

    sender_id = '123'
    date_time_sent = datetime.datetime.now()
    message_text = 'some_text'

    cur.execute("INSERT INTO in_chatroom(student_id, uni_id, chatroom_id) VALUES(%(sender_id)s, %(uni_id)s, %(chatroom_id)s)",
                {"sender_id" : sender_id, "uni_id" : uni_id, "chatroom_id" : chatroom_id})

    cur.execute("INSERT INTO message(sender_id, chatroom_id, message_text, date_time_sent) VALUES(%(sender_id)s, %(chatroom_id)s, %(message_text)s, %(date_time_sent)s)",
                {"chatroom_id" : chatroom_id, "sender_id" : sender_id, "date_time_sent" : date_time_sent, "message_text" : message_text})
    
    res = chatroom.retrieve_messages(cur, chatroom_id)

    assert(json.loads(res) != {})

    #a = 1
    #assert(a == 1)

def test_save_message(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO student(email, password, salt, student_id) VALUES('a', 'a', 'a', '123')")
    cur.execute("INSERT INTO university values('NYU')")
    chatroom_name = 'a'
    uni_id = 'NYU'
    cur.execute("INSERT INTO chatroom(chatroom_name, uni_id) VALUES(%(chatroom_name)s, %(uni_id)s)", {"chatroom_name" : chatroom_name, "uni_id" : uni_id})
    
    #get chatroom id
    cur.execute("SELECT id FROM chatroom")
    chatroom_id = cur.fetchall()[0][0]

    sender_id = '123'
    cur.execute("INSERT INTO in_chatroom(student_id, uni_id, chatroom_id) VALUES(%(sender_id)s, %(uni_id)s, %(chatroom_id)s)",
                {"sender_id" : sender_id, "uni_id" : uni_id, "chatroom_id" : chatroom_id})
    
    chatroom.save_message(cur, '123', chatroom_id, 'some_text')
    cur.execute("SELECT message_text FROM message")

    text = cur.fetchall()[0][0]
    assert(text == 'some_text')

def test_generate_invite(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO student(email, password, salt, student_id, uni_id) VALUES('a', 'a', 'a', '123', 'NYU')") #invitee
    cur.execute("INSERT INTO student(email, password, salt, student_id, uni_id) VALUES('b', 'b', 'b', '567', 'NYU')") #inviter
    cur.execute("INSERT INTO student(email, password, salt, student_id, uni_id) VALUES('c', 'c', 'c', '442', 'NYU')") #onvitee 2
    cur.execute("INSERT INTO university values('NYU')")
    chatroom_name = 'chat'
    uni_id = 'NYU'
    cur.execute("INSERT INTO chatroom(chatroom_name, uni_id) VALUES(%(chatroom_name)s, %(uni_id)s)", {"chatroom_name" : chatroom_name, "uni_id" : uni_id})
    cur.execute("SELECT id FROM chatroom")
    chatroom_id = cur.fetchall()[0][0]
    #insert one of the users (the invite sender) into the chatroom
    cur.execute("INSERT INTO in_chatroom(student_id, uni_id, chatroom_id) VALUES('567', 'NYU', %(chatroom_id)s)", {"chatroom_id" : chatroom_id})


    #invite = json.loads(chatroom.generate_invite(cur, '123', chatroom_id))

    assert(chatroom.generate_invite(cur, '123', '567', chatroom_id, 'NYU') == True)
    assert(chatroom.generate_invite(cur, '442', '567', chatroom_id, 'NYU') == True)

    cur.execute("SELECT target_user_id FROM invite")
    res = cur.fetchall()
    res = [x[0] for x in res]

    assert(123 in res)
    assert(442 in res)

    #assert(invite["invite_id"] == invite_id)


def test_accept_invite(postgresql):
    cur = postgresql.cursor()

    cur.execute("INSERT INTO student(email, password, salt, student_id, uni_id) VALUES('a', 'a', 'a', '123', 'NYU')") #invitee
    cur.execute("INSERT INTO student(email, password, salt, student_id, uni_id) VALUES('b', 'b', 'b', '567', 'NYU')") #inviter
    cur.execute("INSERT INTO university values('NYU')")
    #chatroom_name = 'a'
    #uni_id = 'NYU'
    cur.execute("INSERT INTO chatroom(chatroom_name, uni_id) VALUES('ping pong club', 'NYU')")
    cur.execute("SELECT id FROM chatroom")
    chatroom_id = cur.fetchall()[0][0]

    cur.execute("INSERT INTO in_chatroom(student_id, uni_id, chatroom_id) VALUES('567', 'NYU', %(chatroom_id)s)",
                {"chatroom_id" : chatroom_id})

    cur.execute("INSERT INTO invite(invite_id, chatroom_id, invite_sender_id, target_user_id, uni_id) VALUES('abcdxyz123', %(chatroom_id)s, '567', '123', 'NYU')", 
                {"chatroom_id" : chatroom_id})

    #get invite id
    #cur.execute("SELECT invite_id FROM chatroom")
    cur.execute("SELECT invite_id FROM invite")
    invite_id = cur.fetchall()[0][0]
    assert(invite_id == 'abcdxyz123')

    cur.execute("SELECT student_id FROM student WHERE email = 'a'")
    student_id = cur.fetchall()[0][0]
    assert(str(student_id) == '123') 

    #invite_object = {"invite_id" : invite_id, "target_user" : student_id}
    #invite_object = json.dumps(invite_object)
    #chatroom.accept_invite(cur, invite_object, student_id)
    chatroom.accept_invite(cur, invite_id, student_id)

    
    #assert (res == True)

    cur.execute("SELECT student_id FROM in_chatroom")
    res = cur.fetchall()[0][0]
    #assert (res == student_id)


def test_get_chatrooms(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO student(email, password, salt, student_id, uni_id) VALUES('a', 'a', 'a', '123', 'NYU')")
    cur.execute("INSERT INTO university values('NYU')")

    cur.execute("INSERT INTO course VALUES('CS101', 'NYU')") #chatroom is automatically created via trigger
    cur.execute("INSERT INTO section(course_id, uni_id, section_id) VALUES('CS101', 'NYU', 'B')")
    cur.execute("INSERT INTO takes(student_id, uni_id, course_id, section_id) VALUES('123', 'NYU', 'CS101', 'B')")

    #student is automatically placed in the chatroom for the CS101 course (via trigger)
    
    ch_name = 'softball team'
    cur.execute("INSERT INTO chatroom(chatroom_name, uni_id) VALUES(%(ch_name)s, 'NYU')", {"ch_name" : ch_name})
    cur.execute("SELECT id FROM chatroom WHERE chatroom_name = %(ch_name)s", {"ch_name" : ch_name})
    ch_id = cur.fetchall()[0][0]
    
    cur.execute("INSERT INTO in_chatroom(student_id, uni_id, chatroom_id) VALUES('123', 'NYU', %(ch_id)s)", {"ch_id" : ch_id})

    res = chatroom.getChatrooms(cur, '123', 'NYU')
    assert(res["chatrooms"] == [(1, 'CS101'), (2, 'softball team')])

    

def a():
    a = 1
    assert(a == 1)
