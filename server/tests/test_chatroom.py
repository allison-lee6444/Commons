from server import chatroom

import random
import string
import datetime
import json

from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"],port=8500
)
postgresql = factories.postgresql("postgresql_proc")

def make_db(cur):
    cur.execute("INSERT INTO university VALUES ('NYU');")
    cur.execute("INSERT INTO student VALUES (123456,'NYU','abc123@nyu.edu','A','Bb',NULL,NULL,NULL,NULL,'thePass','theSalt');")
    cur.execute("INSERT INTO course VALUES ('CS-UY 1234','NYU');")
    cur.execute("INSERT INTO section VALUES ('CS-UY 1234','NYU','A','08:00:00','10:00:00','2023-09-01','2023-12-31','2023',true,false,true,false,false,false,false);")
    cur.execute("INSERT INTO takes VALUES (123456,'NYU','CS-UY 1234','A');")
    cur.execute("INSERT INTO chatroom VALUES (DEFAULT,'CS-UY 1234 Chatroom','NYU','CS-UY 1234');")
    cur.execute("INSERT INTO in_chatroom VALUES (123456,'NYU','CS-UY 1234',1);")
    cur.execute("INSERT INTO message VALUES (123456,1,'THIS IS A TEST MESSAGE!','2023-11-13 10:00:00');")



def test_get_msg_update(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # start
    assert chatroom.get_msg_update(cur, 1, '2023-11-12 10:00:00') == '[[123456, 1, "THIS IS A TEST MESSAGE!", "2023-11-13T10:00:00"]]' 


def test_retrieveMessages(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # start
    assert chatroom.retrieveMessages(cur, 1) == '[[123456, 1, "THIS IS A TEST MESSAGE!", "2023-11-13T10:00:00", "A", "Bb", "abc123@nyu.edu"]]'


def test_saveMessage(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    assert chatroom.saveMessage(cur, 123456, 1, "Hello pytest!") == True


def test_createChatroom(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    assert chatroom.createChatroom(cur, 123456, "Comp Sci Club", 'NYU') == True


def test_getChatrooms(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # start
    assert chatroom.getChatrooms(cur, 123456, 'NYU')['chatrooms'] == [(1, "CS-UY 1234 Chatroom")]

