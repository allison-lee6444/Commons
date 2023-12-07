START TRANSACTION;

DROP TABLE IF EXISTS takes CASCADE;
DROP TABLE IF EXISTS section CASCADE;
DROP TABLE IF EXISTS student CASCADE;
DROP TABLE IF EXISTS course CASCADE;

CREATE TABLE IF NOT EXISTS student (
    email varchar(255) NOT NULL,
    student_id bigint NOT NULL,
    uni_id varchar(255) NOT NULL,
    fname varchar(255),
    lname varchar(255),
    major varchar(255),
    graduation_year int,
    primary key(email, student_id, uni_id)
);

CREATE TABLE IF NOT EXISTS course (
    id varchar(255) NOT NULL,
    uni_id varchar(255) NOT NULL,
    primary key(id, uni_id)
);

CREATE TABLE IF NOT EXISTS section (
    course_id varchar(255) NOT NULL,
    section_id varchar(255) NOT NULL,
    uni_id varchar(255) NOT NULL,
    start_time time,
    end_time time,
    semStartDate date,
    semEndDate date,
    year varchar(255),
    meetsMon boolean,
    meetsTue boolean,
    meetsWed boolean,
    meetsThu boolean,
    meetsFri boolean,
    meetsSat boolean,
    meetsSun boolean,
    primary key(course_id, section_id, uni_id),
    foreign key (course_id, uni_id) REFERENCES course(id, uni_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS takes (
    student_id bigint NOT NULL,
    course_id varchar(255) NOT NULL,
    section_id varchar(255) NOT NULL,
    uni_id varchar(255) NOT NULL,
    primary key(student_id, course_id, uni_id),
    foreign key(course_id, section_id, uni_id) REFERENCES section(course_id, section_id, uni_id) ON DELETE CASCADE
);

INSERT INTO student VALUES ('abc123@nyu.edu',123456,'NYU','Bob','Smith','Computer Science',2023);
INSERT INTO student VALUES ('bbb@nyu.edu',888888,'NYU','Jack','Smith','Computer Science',2023);
INSERT INTO student VALUES ('ccc@nyu.edu',777777,'NYU','Jill','Smith','Computer Science',2023);
INSERT INTO student VALUES ('ddd@nyu.edu',666666,'NYU','John','Smith','Computer Science',2023);
INSERT INTO student VALUES ('allisonlee6444@gmail.com',555555,'NYU','Allison','Lee','Computer Science',2024);
INSERT INTO course VALUES ('CS-UY 1234','NYU');
INSERT INTO course VALUES ('CS-UY 9999','NYU');
INSERT INTO section VALUES ('CS-UY 1234','A','NYU','08:00:00','10:00:00','2023-09-01','2023-12-31','2023',True,False,True,False,False,False,False);
INSERT INTO section VALUES ('CS-UY 9999','A','NYU','10:00:00','12:00:00','2023-09-01','2023-12-31','2023',False,True,False,True,False,False,False);
INSERT INTO takes VALUES (123456,'CS-UY 1234','A','NYU');
INSERT INTO takes VALUES (555555,'CS-UY 1234','A','NYU');
INSERT INTO takes VALUES (555555,'CS-UY 9999','A','NYU');

COMMIT;