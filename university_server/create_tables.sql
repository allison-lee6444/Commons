START TRANSACTION;

DROP TABLE IF EXISTS takes;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS course;

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

COMMIT;