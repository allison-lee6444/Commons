START TRANSACTION;

DROP TABLE IF EXISTS going_to_event;
DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS in_chatroom;
DROP TABLE IF EXISTS flashcard;
DROP TABLE IF EXISTS chatroom;
DROP TABLE IF EXISTS takes;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS university;;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS invite;

CREATE TABLE IF NOT EXISTS student(
    student_id bigint,
    uni_id varchar(255),
    email varchar(255) NOT NULL,
    fname varchar(255),
    lname varchar(255),
    graduation_year int,
    major varchar(255),
    hobbies text,
    interests text,
    password varchar(72) NOT NULL,
    salt varchar(72) NOT NULL,
    primary key(email),
    unique (student_id, uni_id)
);

CREATE TABLE IF NOT EXISTS university (
    id varchar(255) NOT NULL, --ex : "NYU"
    primary key(id)
);

CREATE TABLE IF NOT EXISTS course (
    id varchar(255) NOT NULL,
    uni_id varchar(255) NOT NULL,
    primary key(id, uni_id),
    foreign key(uni_id) REFERENCES university(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS section (
    course_id varchar(255) NOT NULL,
    uni_id varchar(255) NOT NULL,
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
    primary key(course_id, uni_id, section_id),
    foreign key (course_id, uni_id) REFERENCES course(id, uni_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS takes (
    student_id bigint NOT NULL,
    uni_id varchar(255) NOT NULL,
    course_id varchar(255) NOT NULL,
    section_id varchar(255) NOT NULL,
    primary key(student_id, uni_id, course_id),
    foreign key(student_id, uni_id) REFERENCES student(student_id, uni_id) ON DELETE CASCADE,
    foreign key(course_id, uni_id, section_id) REFERENCES section(course_id, uni_id, section_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chatroom(
    id SERIAL, --bigint SERIAL, --AUTO_INCREMENT,
    chatroom_name varchar(255) NOT NULL,
    uni_id varchar(255) NOT NULL,
    course_id varchar(255),
    primary key(id),
    foreign key(uni_id) REFERENCES university(id) ON DELETE CASCADE  
);

CREATE TABLE IF NOT EXISTS flashcard(
    id SERIAL,
    front text,
    back text,
    chatroom_id bigint NOT NULL,
    primary key(id, chatroom_id),
    foreign key(chatroom_id) REFERENCES chatroom(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS in_chatroom (
    --`email` varchar(255) NOT NULL,
    student_id bigint NOT NULL, --varchar(255) NOT NULL,
    uni_id varchar(255) NOT NULL,
    course_id varchar(255), --previously was NOT NULL
    chatroom_id bigint NOT NULL,
    primary key(student_id, chatroom_id),
    --primary key(`email`, `chatroom_id`),
    --foreign key(`email`) REFERENCES `student`(`email`) ON DELETE CASCADE,
    foreign key(student_id, uni_id, course_id) REFERENCES takes(student_id, uni_id, course_id) ON DELETE CASCADE,
    foreign key(chatroom_id) REFERENCES chatroom(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS invite(
    invite_id varchar(10),
    chatroom_id bigint,
    invite_sender_id bigint, --student id of the user who is sending the invite
    target_user_id bigint, --student id of the user who is being invited
    uni_id varchar(255),
    primary key(invite_id),
    foreign key(target_user_id, uni_id) REFERENCES student(student_id, uni_id),
    foreign key(invite_sender_id, uni_id) REFERENCES student(student_id, uni_id),
    foreign key(chatroom_id, invite_sender_id) REFERENCES in_chatroom(chatroom_id, student_id)
    --make sure the user sending the invite is in the chatroom
);

CREATE TABLE IF NOT EXISTS message (
    --`sender_email` varchar(255) NOT NULL,
    sender_id bigint NOT NULL,
    chatroom_id bigint NOT NULL,
    message_text text NOT NULL,
    date_time_sent timestamp NOT NULL, --datetime NOT NULL,
    primary key(sender_id, chatroom_id, date_time_sent), --(sender_email, chatroom_id, date_time_sent),
    foreign key(sender_id, chatroom_id) REFERENCES in_chatroom(student_id, chatroom_id) ON DELETE CASCADE
    --foreign key(`sender_email`, `chatroom_id`) REFERENCES `in_chatroom`(`email`, `chatroom_id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS game (
    game_id varchar(255), --the name of the game
    primary key(game_id)
);

CREATE TABLE IF NOT EXISTS player (
    game_id varchar(255) NOT NULL,
    --`email` varchar(255),
    player_id bigint NOT NULL,
    chatroom_id bigint NOT NULL,
    score bigint,
    --primary key(`game_id`, `email`),
    primary key(game_id, player_id, chatroom_id),
    foreign key(player_id, chatroom_id) REFERENCES in_chatroom(student_id, chatroom_id) ON DELETE CASCADE,
    foreign key(game_id) REFERENCES game(game_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS event(
    event_name varchar(255) NOT NULL,
    host_id bigint NOT NULL,
    uni_id varchar(255) NOT NULL, 
    chatroom_id bigint NOT NULL,
    descript text,
    location_name varchar(255) NOT NULL,
    location_coordinates point NOT NULL,
    --timeslot timestamp, --datetime,
    start_time timestamp,
    end_time timestamp,
    event_id SERIAL, --bigint SERIAL NOT NULL, --AUTO_INCREMENT NOT NULL,
    primary key(event_id),
    foreign key (host_id, uni_id) REFERENCES student(student_id, uni_id),
    foreign key (chatroom_id) REFERENCES chatroom(id)
    --primary key(`event_name`, `chtaroom_id`, `timeslot`, `location`),
    --foreign key `chatroom_id` REFERENCES `chatroom`(`id`)
);


CREATE TABLE IF NOT EXISTS going_to_event(
    event_id bigint NOT NULL,
    student_id bigint NOT NULL,
    chatroom_id bigint NOT NULL,
    primary key(event_id, student_id, chatroom_id),
    foreign key (student_id, chatroom_id) REFERENCES in_chatroom(student_id, chatroom_id) ON DELETE CASCADE,
    foreign key (event_id) REFERENCES event(event_id) ON DELETE CASCADE
);


COMMIT;