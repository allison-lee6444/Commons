from server import staff_utility  # AL: why are we pushing a test for a nonexistent file?
from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"], port=9000
)
postgresql = factories.postgresql("postgresql_proc")


# AL: shorten this as u need it
def make_db(cur):
    cur.execute(
        "INSERT INTO student VALUES (123456,'NYU','abc123@nyu.edu',NULL,NULL,NULL,NULL,NULL,NULL,'thePass','theSalt');")
    cur.execute("INSERT INTO university VALUES ('NYU');")
    cur.execute("INSERT INTO course VALUES ('CS-UY 1234','NYU');")
    cur.execute(
        "INSERT INTO section VALUES ('CS-UY 1234','NYU','A','08:00:00','10:00:00','2023-09-01','2023-12-31','2023',true,false,true,false,false,false,false);")
    cur.execute("INSERT INTO takes VALUES (123456,'NYU','CS-UY 1234','A');")
    cur.execute("INSERT INTO flashcard VALUES (DEFAULT,'Front!','Back!',1);")
    cur.execute("INSERT INTO message VALUES (123456,1,'THIS IS A TEST MESSAGE!','2023-11-13 10:00:00');")
    cur.execute("INSERT INTO game VALUES ('THE NYU GAME');")
    cur.execute("INSERT INTO player VALUES ('THE NYU GAME',123456,1,100);")
    cur.execute(
        "INSERT INTO event VALUES ('Orientation',123456,'NYU',1,'Welcome!','370 Jay Street',POINT(1.0,1.0),'2023-12-01 08:00:00','2023-12-01 10:00:00');")
    cur.execute(
        "INSERT INTO student(student_id,uni_id,email,password,salt) VALUES(111111,'NYU','a@nyu.edu','A','SALT')")
    cur.execute(
        "INSERT INTO student(student_id,uni_id,email,password,salt) VALUES(222222,'NYU','b@nyu.edu','B','SALT')")
    cur.execute(
        "INSERT INTO student(student_id,uni_id,email,password,salt) VALUES(333333,'NYU','c@nyu.edu','C','SALT')")
    cur.execute("INSERT INTO takes VALUES(111111,'NYU','CS-UY 1234','A')")
    cur.execute("INSERT INTO takes VALUES(222222,'NYU','CS-UY 1234','A')")
    cur.execute("INSERT INTO takes VALUES(333333,'NYU','CS-UY 1234','A')")


def test_del_old_courses(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # Last year.
    cur.execute(
        "INSERT INTO section VALUES ('CS-UY 1234','NYU','Y','08:00:00','10:00:00','2022-09-01','2022-12-31','2022',true,false,true,false,false,false,false);")
    cur.execute("SELECT * FROM takes WHERE student_id=123456;")
    expected = cur.fetchall()
    cur.execute("INSERT INTO takes VALUES (123456,'NYU','CS-UY 1234','Y');")
    staff_utility.del_old_courses()  # This should delete the course we just added.
    # Call this query again, it should not show a course from section Y.
    cur.execute("SELECT * FROM takes WHERE student_id=123456;")
    result = cur.fetchall()
    assert result == expected


def test_add_new_courses(postgresql):
    pass
