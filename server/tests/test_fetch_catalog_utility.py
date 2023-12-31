from server.utility import fetch_catalog_utility
from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(

    load=["database/create_tables.sql"],port=9100

)
postgresql = factories.postgresql("postgresql_proc")

def make_db(cur):
    cur.execute("INSERT INTO student VALUES (123456,'NYU','abc123@nyu.edu',NULL,NULL,NULL,NULL,NULL,NULL,'thePass','theSalt');")
    cur.execute("INSERT INTO university VALUES ('NYU');")
    cur.execute("INSERT INTO course VALUES ('CS-UY 1234','NYU');")
    cur.execute("INSERT INTO section VALUES ('CS-UY 1234','NYU','A','08:00:00','10:00:00','2023-09-01','2023-12-31','2023',true,false,true,false,false,false,false);")
    cur.execute("INSERT INTO takes VALUES (123456,'NYU','CS-UY 1234','A');")
    cur.execute("INSERT INTO chatroom VALUES (DEFAULT,'CS-UY 1234 Chatroom','NYU','CS-UY 1234');")
    cur.execute("INSERT INTO flashcard VALUES (DEFAULT,'Front!','Back!',1);")
    cur.execute("INSERT INTO in_chatroom VALUES (123456,'NYU','CS-UY 1234',1);")
    cur.execute("INSERT INTO message VALUES (123456,1,'THIS IS A TEST MESSAGE!','2023-11-13 10:00:00');")
    cur.execute("INSERT INTO game VALUES ('THE NYU GAME');")
    cur.execute("INSERT INTO player VALUES ('THE NYU GAME',123456,1,100);")
    cur.execute("INSERT INTO event VALUES ('Orientation',123456,'NYU',1,'Welcome!','370 Jay Street',POINT(1.0,1.0),'2023-12-01 08:00:00','2023-12-01 10:00:00');")
    cur.execute("INSERT INTO student(student_id,uni_id,email,password,salt) VALUES(111111,'NYU','a@nyu.edu','A','SALT')")
    cur.execute("INSERT INTO student(student_id,uni_id,email,password,salt) VALUES(222222,'NYU','b@nyu.edu','B','SALT')")
    cur.execute("INSERT INTO student(student_id,uni_id,email,password,salt) VALUES(333333,'NYU','c@nyu.edu','C','SALT')")
    cur.execute("INSERT INTO takes VALUES(111111,'NYU','CS-UY 1234','A')")
    cur.execute("INSERT INTO takes VALUES(222222,'NYU','CS-UY 1234','A')")
    cur.execute("INSERT INTO takes VALUES(333333,'NYU','CS-UY 1234','A')")
    cur.execute("INSERT INTO in_chatroom VALUES (111111,'NYU','CS-UY 1234',1)")
    cur.execute("INSERT INTO in_chatroom VALUES (222222,'NYU','CS-UY 1234',1)")
    cur.execute("INSERT INTO in_chatroom VALUES (333333,'NYU','CS-UY 1234',1)")

def test_fetch_catalog(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    fetch_catalog_utility.fetch_catalog(cur)
    cur.execute("SELECT * FROM course WHERE id='FOOD-UE 1001'")
    assert cur.fetchall() == [('FOOD-UE 1001','NYU')]
    cur.execute("SELECT course_id,section_id FROM section WHERE course_id='FOOD-UE 1001'")
    assert cur.fetchall() == [('FOOD-UE 1001','A')]
 