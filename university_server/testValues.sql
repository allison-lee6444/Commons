INSERT INTO student VALUES ('abc123@nyu.edu',123456,'NYU','Bob','Smith','Computer Science',2023);
INSERT INTO student VALUES ('bbb@nyu.edu',888888,'NYU','Jack','Smith','Computer Science',2023);
INSERT INTO student VALUES ('ccc@nyu.edu',777777,'NYU','Jill','Smith','Computer Science',2023);
INSERT INTO student VALUES ('ddd@nyu.edu',666666,'NYU','John','Smith','Computer Science',2023);
INSERT INTO course VALUES ('CS-UY 1234','NYU');
INSERT INTO course VALUES ('CS-UY 9999','NYU');
INSERT INTO section VALUES ('CS-UY 1234','A','NYU','08:00:00','10:00:00','2023-09-01','2023-12-31','2023',True,False,True,False,False,False,False);
INSERT INTO section VALUES ('CS-UY 9999','A','NYU','10:00:00','12:00:00','2023-09-01','2023-12-31','2023',False,True,False,True,False,False,False);
INSERT INTO takes VALUES (123456,'CS-UY 1234','A','NYU');

INSERT INTO course VALUES ('FOOD-UE 1001','NYU');
INSERT INTO section VALUES ('FOOD-UE 1001','A','NYU','10:00:00','12:00:00','2023-09-01','2023-12-31','2023',false,false,false,false,true,false,false);