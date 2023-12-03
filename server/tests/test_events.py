from server import events
from db import make_db
from pytest_postgresql import factories
import datetime

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"],port=8600
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
    make_db(cur)
    # Valid chatroom.
    assert events.editEvent(cur,1,"TEST123",123456,"NYU","Testing theh function.","Test City",'(1,2)','2023-11-13 10:00:00','2023-11-13 12:00:00') == True
   
def test_join_event(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # join event made at start
    cur.execute("SELECT event_id FROM event WHERE event_name='Orientation';")
    event_id = cur.fetchall()[0][0]
    assert events.join_event(cur,1,123456,event_id) == True

def test_leave_event(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    events.join_event(cur,1,123456,1)
    assert events.leave_event(cur,123456,1) == True

def test_cancel_event(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    assert events.cancel_event(cur,123456,1) == True

def test_get_events(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    cur.execute("SELECT event_id FROM event WHERE event_name='Orientation';")
    event_id = cur.fetchall()[0][0]
    events.join_event(cur,1,123456,event_id)
    assert events.get_events(cur,123456,'NYU') == '[[%(event_id)s, 1, "Orientation", null, null, "Welcome!", "370 Jay Street", "2023-12-01T08:00:00", "2023-12-01T10:00:00"]]' % {'event_id':event_id}

def test_get_event(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    cur.execute("SELECT event_id FROM event WHERE event_name='Orientation';")
    event_id = cur.fetchall()[0][0]
    events.join_event(cur,1,123456,event_id)
    assert events.get_event(cur,event_id,1,123456,'NYU') == '[["Orientation", null, null, "abc123@nyu.edu", "Welcome!", "370 Jay Street", "(1,1)", "2023-12-01T08:00:00", "2023-12-01T10:00:00"]]'

def test_get_courses(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # start
    assert events.get_courses(cur,123456,'NYU') == '[["CS-UY 1234", "A", "08:00:00", "10:00:00", "2023-09-01", "2023-12-31", "2023", true, false, true, false, false, false, false]]'

def test_has_conflict(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    events.join_event(cur,1,123456,1)
    assert events.has_conflict(cur,'2023-12-01 09:00:00','2023-12-01 10:00:00',123456) == True


