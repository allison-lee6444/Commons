def make_db(cur):
    cur.execute("INSERT INTO student VALUES (123456,'NYU','abc123@nyu.edu',NULL,NULL,NULL,NULL,NULL,NULL,'thePass','theSalt');")
    cur.execute("INSERT INTO university VALUES ('NYU');")
    cur.execute("INSERT INTO course VALUES ('CS-UY 1234','NYU');")
    cur.execute("INSERT INTO section VALUES ('CS-UY 1234','NYU','A','08:00:00','10:00:00','2023-09-01','2023-12-31','2023',True,False,True,False,False,False,False);")
    cur.execute("INSERT INTO takes VALUES (123456,'NYU','CS-UY 1234','A');")
    cur.execute("INSERT INTO chatroom VALUES (DEFAULT,'CS-UY 1234 Chatroom','NYU','CS-UY 1234');")
    cur.execute("INSERT INTO flashcard VALUES (DEFAULT,'Front!','Back!',1);")
    cur.execute("INSERT INTO in_chatroom VALUES (123456,'NYU','CS-UY 1234',1);")
    cur.execute("INSERT INTO message VALUES (123456,1,'THIS IS A TEST MESSAGE!','2023-11-13 10:00:00');")
    cur.execute("INSERT INTO game VALUES ('THE NYU GAME');")
    cur.execute("INSERT INTO player VALUES ('THE NYU GAME',123456,1,100);")
    cur.execute("INSERT INTO event VALUES ('Orientation',123456,'NYU',1,'Welcome!','370 Jay Street',POINT(123,456));")

