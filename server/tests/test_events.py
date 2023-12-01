from server import events
from db import make_db
from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql",make_db]
)
postgresql = factories.postgresql("postgresql_proc")

"""def test_get_student_id(postgresql):
    cur = postgresql.cursor()
    cur.execute(
        "INSERT INTO student (student_id, uni_id, email, password, salt) VALUES (123,'NYU','a@nyu.edu','p','s')"
    )
    assert profiles.get_student_uni_id(cur, 'a@nyu.edu') == (123, 'NYU')"""

def test_editEvent(postgresql):
    cur = postgresql.cursor()
    make_db(postgresql)
    # Valid chatroom.
    assert events.editEvent(cur,1,"TEST123",123456,"NYU","Testing theh function.","Test City",'(1,2)','2023-11-13 10:00:00','2023-11-13 12:00:00') == True
    # Invalid chatroom.
    assert events.editEvent(cur,23,"TEST123",123456,"NYU","Testing theh function.","Test City",'(1,2)','2023-11-13 10:00:00','2023-11-13 12:00:00') == False
   
def test_join_event(postgresql):
    cur = postgresql.cursor()
    make_db(postgresql)
    # join event made at start
    assert events.join_event(cur,1,123456,1) == True

def test_leave_event(postgresql):
    cur = postgresql.cursor()
    make_db(postgresql)
    events.join_event(cur,1,123456,1)
    assert events.leave_event(cur,123456,1) == True

def test_cancel_event(postgresql):
    cur = postgresql.cursor()
    make_db(postgresql)
    assert events.cancel_event(cur,123456,1) == True

def test_get_events(postgresql):
    cur = postgresql.cursor()
    make_db(postgresql)
    events.join_event(cur,1,123456,1)
    assert events.get_events(cur,123456,'NYU') == [(1,1,'Orientation',None,None,'Welcome!','370 Jay Street','2023-12-01 08:00:00','2023-12-01 10:00:00')]

def test_get_event(postgresql):
    cur = postgresql.cursor()
    make_db(postgresql)
    events.join_event(cur,1,123456,1)
    assert events.get_event(cur,123456,1,123456,'NYU') == [('Orientation',None,None,'abc123@nyu.edu','Welcome!','370 Jay Street','POINT(1.0,1.0)','2023-12-01 08:00:00','2023-12-01 10:00:00')]

def test_get_courses(postgresql):
    cur = postgresql.cursor()
    make_db(postgresql)
    # start
    assert events.get_courses(cur,123456,'NYU') == [('CS-UY 1234','A','08:00:00','10:00:00','2023-09-01','2023-12-31','2023',True,False,True,False,False,False,False)]

def test_has_conflict(postgresql):
    cur = postgresql.cursor()
    make_db(postgresql)
    events.join_event(cur,1,123456,1)
    assert events.has_conflict(cur,'2023-12-01 09:00:00','2023-12-01 10:00:00') == True


