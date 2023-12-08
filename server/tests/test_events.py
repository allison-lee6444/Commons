from server import events
from pytest_postgresql import factories
from dateutil.parser import parse
import datetime

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"], port=8600
)
postgresql = factories.postgresql("postgresql_proc")


def make_db(cur):
    cur.execute("INSERT INTO university VALUES ('NYU');")
    cur.execute(
        "INSERT INTO student VALUES (123456,'NYU','abc123@nyu.edu',NULL,NULL,NULL,NULL,NULL,NULL,'thePass','theSalt');")
    cur.execute("INSERT INTO course VALUES ('CS-UY 1234','NYU');")
    cur.execute(
        "INSERT INTO section VALUES ('CS-UY 1234','NYU','A','08:00:00','10:00:00','2023-09-01','2023-12-31','2023',true,false,true,false,false,false,false);")
    cur.execute("INSERT INTO takes VALUES (123456,'NYU','CS-UY 1234','A');")
    cur.execute("INSERT INTO chatroom VALUES (DEFAULT,'CS-UY 1234 Chatroom','NYU','CS-UY 1234');")
    cur.execute("INSERT INTO in_chatroom VALUES (123456,'NYU','CS-UY 1234',1);")
    cur.execute(
        "INSERT INTO event VALUES ('Orientation',123456,'NYU',1,'Welcome!','370 Jay Street',POINT(1.0,1.0),'2023-12-01 08:00:00','2023-12-01 10:00:00');")


def test_create_event(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # Valid chatroom.
    assert events.create_event(cur, 1, "TEST123", 123456, "NYU", "Testing theh function.", "Test City", '(1,2)',
                            '2023-11-13 10:00:00', '2023-11-13 12:00:00') is True


def test_join_event(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # join event made at start
    cur.execute("SELECT event_id FROM event WHERE event_name='Orientation';")
    event_id = cur.fetchall()[0][0]
    assert events.join_event(cur, 1, 123456, event_id) == True


def test_leave_event(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    events.join_event(cur, 1, 123456, 1)
    assert events.leave_event(cur, 123456, 1) == True


def test_cancel_event(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    assert events.cancel_event(cur, 123456, 1) == True


def test_get_events(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    cur.execute("SELECT event_id FROM event WHERE event_name='Orientation';")
    event_id = cur.fetchall()[0][0]
    events.join_event(cur, 1, 123456, event_id)
    assert events.get_events(cur, 123456,
                             'NYU') == '[[%(event_id)s, 1, "Orientation", null, null, "Welcome!", "370 Jay Street", "2023-12-01T08:00:00", "2023-12-01T10:00:00"]]' % {
               'event_id': event_id}


def test_get_event(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    cur.execute("SELECT event_id FROM event WHERE event_name='Orientation';")
    event_id = cur.fetchall()[0][0]
    events.join_event(cur, 1, 123456, event_id)
    assert events.get_event(cur, event_id, 1, 123456,
                            'NYU') == '[["Orientation", null, null, "abc123@nyu.edu", "Welcome!", "370 Jay Street", "(1,1)", "2023-12-01T08:00:00", "2023-12-01T10:00:00"]]'


def test_get_courses(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # start
    assert events.get_courses(cur, 123456,
                              'NYU') == '[["CS-UY 1234", "A", "08:00:00", "10:00:00", "2023-09-01", "2023-12-31", "2023", true, false, true, false, false, false, false]]'


def test_has_conflict(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    events.join_event(cur, 1, 123456, 1)
    format = '%a %b %d %Y %H:%M:%S GMT%z ('
    dt1 = parse('2023-12-01 09:00:00-0500').strftime(format)
    dt2 = parse('2023-12-01 10:00:00-0500').strftime(format)
    dt3 = parse('2023-12-04 08:00:00-0500').strftime(format)
    dt4 = parse('2023-12-04 10:00:00-0500').strftime(format)

    # conflict with an event
    assert events.has_conflict(cur, dt1, dt2, 123456) is True
    # conflict with a class
    assert events.has_conflict(cur, dt3, dt4, 123456) is True

def test_edit_event(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # Get starter event id.
    cur.execute("SELECT event_id FROM event WHERE event_name='Orientation'")
    event_id = cur.fetchone()[0]
    # Update this event.  See if it returns true.
    assert events.edit_event(cur,1,'Not Orientation',123456,'NYU','Welcome to not orientation!','Rogers Hall','(1.0,1.0)','2023-12-20 08:00:00','2023-12-20 12:00:00',event_id)["result"] == True
    # See if it updated.
    cur.execute("SELECT event_name FROM event WHERE event_id=%(event_id)s",{'event_id':event_id})
    assert cur.fetchall()[0][0] == 'Not Orientation'

