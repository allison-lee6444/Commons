from server import staff_utility
from db import make_db
from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"],port=9000
)
postgresql = factories.postgresql("postgresql_proc")

def test_del_old_courses(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # Last year.
    cur.execute("INSERT INTO section VALUES ('CS-UY 1234','NYU','Y','08:00:00','10:00:00','2022-09-01','2022-12-31','2022',true,false,true,false,false,false,false);")
    cur.execute("SELECT * FROM takes WHERE student_id=123456;")
    expected = cur.fetchall()
    cur.execute("INSERT INTO takes VALUES (123456,'NYU','CS-UY 1234','Y');")
    staff_utility.del_old_courses() # This should delete the course we just added.
    # Call this query again, it should not show a course from section Y.
    cur.execute("SELECT * FROM takes WHERE student_id=123456;")
    result = cur.fetchall()
    assert result == expected 

def test_add_new_courses(postgresql):
    pass