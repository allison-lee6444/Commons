from server import request_uni
from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"], port=8900
)
postgresql = factories.postgresql("postgresql_proc")


def make_db(cur):
    cur.execute("INSERT INTO university VALUES ('NYU');")
    cur.execute(
        "INSERT INTO student VALUES (123456,'NYU','abc123@nyu.edu',NULL,NULL,NULL,NULL,NULL,NULL,'thePass','theSalt');")
    cur.execute("INSERT INTO course VALUES ('CS-UY 1234','NYU');")
    cur.execute(
        "INSERT INTO section VALUES ('CS-UY 1234','NYU','A','08:00:00','10:00:00','2023-09-01','2023-12-31','2023',true,false,true,false,false,false,false);")


def test_request_schedule(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    assert request_uni.request_schedule(cur, 'abc123@nyu.edu') is True


def test_request_profile(postgresql):
    cur = postgresql.cursor()
    make_db(cur)

    assert request_uni.request_profile(cur, 'abc123@nyu.edu') is True

def test_get_courses_sections(postgresql):
    cur = postgresql.cursor()
    make_db(cur)

    assert request_uni.request_courses_sections(cur) is True
