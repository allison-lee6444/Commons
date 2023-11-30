from server import events
from db import make_db
from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"],
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
    # Invalid chatroom.
    assert events.editEvent(cur,23,"TEST123",123456,"NYU","Testing theh function.","Test City",'(1,2)','2023-11-13 10:00:00','2023-11-13 12:00:00') == False
    # Invalid user.
    assert events.editEvent(cur,1,"TEST123",126456,"NYU","Testing theh function.","Test City",'(1,2)','2023-11-13 10:00:00','2023-11-13 12:00:00') == False

def test_join_event(postgresql):
    pass

def test_leave_event(postgresql):
    pass

def test_cancel_event(postgresql):
    pass

def get_events(postgresql):
    pass

def get_event(postgresql):
    pass

def get_courses(postgresql):
    pass

def has_conflict(postgresql):
    pass