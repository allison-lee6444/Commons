START TRANSACTION;

DROP TABLE IF EXISTS takes;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS course;

CREATE TABLE IF NOT EXISTS student (
    email varchar(255) NOT NULL,
    student_id bigint NOT NULL,
    primary key(email, student_id)
);

CREATE TABLE IF NOT EXISTS course (
    id varchar(255) NOT NULL,
    primary key(id)
);

CREATE TABLE IF NOT EXISTS section (
    course_id varchar(255) NOT NULL,
    section_id varchar(255) NOT NULL,
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
    primary key(course_id, section_id),
    foreign key (course_id) REFERENCES course(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS takes (
    student_id bigint NOT NULL,
    course_id varchar(255) NOT NULL,
    section_id varchar(255) NOT NULL,
    primary key(student_id, course_id),
    foreign key(course_id, section_id) REFERENCES section(id, section_id) ON DELETE CASCADE
);

COMMIT;