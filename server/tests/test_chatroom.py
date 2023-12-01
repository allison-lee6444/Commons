from server import chatroom
from db import make_db
from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql",make_db]
)
postgresql = factories.postgresql("postgresql_proc")

def test_get_msg_update(postgresql):
    cur = postgresql.cursor()
    # start
    assert chatroom.get_msg_update(cur,1,'2023-11-12 10:00:00') == [(123456,1,'THIS IS A TEST MESSAGE!','2023-11-13 10:00:00')]

def test_retrieveMessages(postgresql):
    cur = postgresql.cursor()
    # start
    assert chatroom.retrieveMessages(cur,1) == [(123456,1,'THIS IS A TEST MESSAGE!','2023-11-13 10:00:00')]

def test_saveMessage(postgresql):
    cur = postgresql.cursor()
    assert chatroom.saveMessage(cur,123456,1,"Hello pytest!") == True

def test_createChatroom(postgresql):
    cur = postgresql.cursor()
    assert chatroom.createChatroom(cur,123456,"Comp Sci Club",'NYU') == True

def test_getChatrooms(postgresql):
    cur = postgresql.cursor()
    # start
    assert chatroom.getChatrooms(cur,123456) == [(1,"CS-UY 1234 Chatroom")]

