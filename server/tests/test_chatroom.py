from server import chatroom

import random
import string
import datetime
import json

from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"], port=8500
)
postgresql = factories.postgresql("postgresql_proc")


def make_db(cur):
    cur.execute("INSERT INTO university VALUES ('NYU');")
    cur.execute(
        "INSERT INTO student VALUES (123456,'NYU','abc123@nyu.edu','A','Bb',NULL,NULL,NULL,NULL,'thePass','theSalt');")
    cur.execute(
        "INSERT INTO student VALUES (654321,'NYU','def456@nyu.edu','C','Dd',NULL,NULL,NULL,NULL,'thePass','theSalt');")
    cur.execute("INSERT INTO course VALUES ('CS-UY 1234','NYU');")
    cur.execute(
        "INSERT INTO section VALUES ('CS-UY 1234','NYU','A','08:00:00','10:00:00','2023-09-01','2023-12-31','2023',true,false,true,false,false,false,false);")
    cur.execute("INSERT INTO takes VALUES (123456,'NYU','CS-UY 1234','A');")
    cur.execute("INSERT INTO chatroom VALUES (1,'CS-UY 1234 Chatroom','NYU','CS-UY 1234');")
    cur.execute("INSERT INTO in_chatroom VALUES (123456,'NYU','CS-UY 1234',1);")
    cur.execute("INSERT INTO message VALUES (123456,1,'THIS IS A TEST MESSAGE!','2023-11-13 10:00:00');")
    cur.execute(
        "INSERT INTO event VALUES ('Orientation',123456,'NYU',1,'Welcome!','370 Jay Street',POINT(1.0,1.0),'2023-12-01 08:00:00','2023-12-01 10:00:00');")

def test_get_msg_update(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # start
    assert chatroom.get_msg_update(cur, 1,
                                   '2023-11-12 10:00:00') == '[[123456, 1, "THIS IS A TEST MESSAGE!", "2023-11-13T10:00:00"]]'


def test_retrieveMessages(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # start
    assert chatroom.retrieve_messages(cur,
                                      1) == '[[123456, 1, "THIS IS A TEST MESSAGE!", "2023-11-13T10:00:00", "A", "Bb", "abc123@nyu.edu"]]'


def test_saveMessage(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    assert chatroom.save_message(cur, 123456, 1, "Hello pytest!") is True


def test_createChatroom(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    assert chatroom.create_chatroom(cur, 123456, "Comp Sci Club", 'NYU') == 2


def test_getChatrooms(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # start
    assert (chatroom.getChatrooms(cur, 123456, 'NYU')['chatrooms'] ==
            [(1, "CS-UY 1234 Chatroom", False)])


def test_invite(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    chatroom.create_chatroom(cur, 123456, "Comp Sci Club", 'NYU')
    invite_id = chatroom.generate_invite(cur, 654321, 123456, 2, 'NYU')
    cur.execute("SELECT invite_id FROM invite WHERE invite_sender_id=123456 AND target_user_id=654321 AND uni_id='NYU'"
                "AND chatroom_id=2")
    result = cur.fetchall()
    assert result == [(invite_id,)]

    assert chatroom.accept_invite(cur, invite_id, 654321) == (2, "Comp Sci Club")
    cur.execute("SELECT student_id FROM in_chatroom WHERE student_id=654321 AND uni_id='NYU' AND course_id is NULL AND"
                " chatroom_id = 2")
    result = cur.fetchall()
    assert result == [(654321,)]

def test_get_chatroom_events(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # Get starter event id.
    cur.execute("SELECT event_id FROM event WHERE event_name='Orientation'")
    event_id = cur.fetchone()[0]
    assert chatroom.get_chatroom_events(cur,1)["events"] == '[["Orientation", 123456, "NYU", "Welcome!", "370 Jay Street", "(1,1)", "2023-12-01T08:00:00", "2023-12-01T10:00:00", '+ str(event_id)+']]'
