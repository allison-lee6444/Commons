START TRANSACTION;

DROP TABLE IF EXISTS `student`;
DROP TABLE IF EXISTS `university`;
DROP TABLE IF EXISTS `attends`;
DROP TABLE IF EXISTS `course`;
DROP TABLE IF EXISTS `takes`;
DROP TABLE IF EXISTS `message`;
DROP TABLE IF EXISTS `chatroom`;
DROP TABLE IF EXISTS `in_chatroom`;
DROP TABLE IF EXISTS `game`;
DROP TABLE IF EXISTS `player`;
DROP TABLE IF EXISTS `event`;
DROP TABLE IF EXISTS `going_to_event`;


CREATE TABLE IF NOT EXISTS `student` (
    `email` varchar(255) NOT NULL,
    --`id`bigint NOT NULL AUTO_INCREMENT,
    `password` varchar(50) NOT NULL,
    primary key(`email`);
);

CREATE TABLE IF NOT EXISTS `university` (
    `id` varchar(255), --ex : "NYU"
    primary key(`id`);
);

CREATE TABLE IF NOT EXISTS `attends` (
    `email` varchar(255) NOT NULL,
    `student_id` bigint NOT NULL,
    `uni_id` varchar(255) NOT NULL,
    primary key(`student_id`, `uni_id`),
    foreign key(`email`) REFERENCES `student`(`email`) ON DELETE CASCADE,
    foreign key(`uni_id`) REFERENCES `university`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `course` (
    `id` varchar(255) NOT NULL,
    `uni_id` varchar(255) NOT NULL,
    primary key(`id`, `uni_id`),
    foreign key(`uni_id`) REFERENCES `university`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `takes` (
    `student_id` bigint NOT NULL,
    `uni_id` varchar(255) NOT NULL,
    `course_id` varchar(255) NOT NULL,
    primary key(`student_id`, `uni_id`, `course_id`),
    foreign key(`student_id`, `uni_id`) REFERENCES `attends`(`student_id`, `uni_id`) ON DELETE CASCADE,
    foreign key(`course_id`, `uni_id`) REFERENCES `course`(`id`, `uni_id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `chatroom`(
    `id` bigint AUTO_INCREMENT,
    `uni_id` varchar(255) NOT NULL,
    `course_id` varchar(255) NOT NULL,
    primary key(`id`),
    foreign key(`course_id`, `uni_id`) REFERENCES `course`(`id`, `uni_id`) ON DELETE CASCADE
  
);

CREATE TABLE IF NOT EXISTS `in_chatroom` (
    --`email` varchar(255) NOT NULL,
    `student_id` varchar(255) NOT NULL,
    `uni_id` varchar(255) NOT NULL,
    `course_id` varchar(255) NOT NULL,
    `chatroom_id` bigint NOT NULL,
    primary key(`student_id`, `chatroom_id`),
    --primary key(`email`, `chatroom_id`),
    --foreign key(`email`) REFERENCES `student`(`email`) ON DELETE CASCADE,
    foreign key(`student_id`, `uni_id`, `course_id`) REFERENCES `takes`(`student_id`, `uni_id`, `course_id`) ON DELETE CASCADE,
    foreign key(`chatroom_id`) REFERENCES `chatroom`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `message` (
    --`sender_email` varchar(255) NOT NULL,
    `sender_id` bigint NOT NULL,
    `chatroom_id` bigint NOT NULL,
    `message_text` text NOT NULL,
    `date_time_sent` datetime NOT NULL,
    primary key(`sender_email`, `chatroom_id`, `date_time_sent`),
    foreign key(`sender_id`, `chatroom_id`) REFERENCES `in_chatroom`(`student_id`, `chatroom_id`) ON DELETE CASCADE
    --foreign key(`sender_email`, `chatroom_id`) REFERENCES `in_chatroom`(`email`, `chatroom_id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `game` (
    `game_id` varchar(255), --the name of the game
    primary key(`game_id`)
);

CREATE TABLE IF NOT EXISTS `player` (
    `game_id` varchar(255) NOT NULL,
    --`email` varchar(255),
    `player_id` bigint NOT NULL,
    `chatroom_id` bigint NOT NULL,
    `score` bigint,
    --primary key(`game_id`, `email`),
    primary key(`game_id`, `player_id`, `chatroom_id`),
    foreign key(`player_id`, `chatroom_id`) REFERENCES `in_chatroom`(`student_id`, `chatroom_id`) ON DELETE CASCADE,
    foreign key(`game_id`) REFERENCES `game`(`game_id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `event`(
    `event_name` varchar(255) NOT NULL,
    --`chatroom_id` bigint NOT NULL,
    `description` text,
    `location` varchar(255) NOT NULL,
    `timeslot` datetime,
    `event_id` bigint AUTO_INCREMENT NOT NULL,
    primary key(`event_id`),
    --primary key(`event_name`, `chtaroom_id`, `timeslot`, `location`),
    --foreign key `chatroom_id` REFERENCES `chatroom`(`id`)
);

CREATE TABLE IF NOT EXISTS `going_to_event`(
    `event_id` bigint NOT NULL,
    `student_id` bigint NOT NULL,
    `chatroom_id` bigint NOT NULL,
    primary key(`event_id`, `student_id`, `chatroom_id`),
    foreign key (`student_id`, `chatroom_id`) REFERENCES `in_chatroom`(`student_id`, `chatroom_id`) ON DELETE CASCADE
);




COMMIT;