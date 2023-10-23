START TRANSACTION;

CREATE OR REPLACE FUNCTION auto_create_course_chatroom() RETURNS TRIGGER AS $$
    BEGIN
        --after insert into course --> insert those values into chatroom db
        IF (TG_OP = 'INSERT') THEN 
            INSERT INTO chatroom(course_id, uni_id) VALUES(NEW.id, NEW.uni_id);
        END IF;
        RETURN NULL; --this is an AFTER trigger
    END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trig_auto_create_course_chatroom
AFTER INSERT ON course
    FOR EACH ROW EXECUTE FUNCTION auto_create_course_chatroom();

CREATE OR REPLACE FUNCTION auto_add_or_remove_student_chatroom() RETURNS TRIGGER AS $$
    BEGIN
        --after insert on takes
        IF (TG_OP = 'INSERT') THEN
            INSERT INTO in_chatroom(student_id, uni_id, course_id, chatroom_id) VALUES(
                NEW.student_id, NEW.uni_id, NEW.course_id,
                (SELECT id from chatroom WHERE uni_id = NEW.uni_id AND course_id = NEW.course_id)
            );
            

        --after delete on takes (ex: student drops a class)
        ELSIF (TG_OP = 'DELETE') THEN
            DELETE FROM in_chatroom WHERE student_id = OLD.student_id AND uni_id = OLD.uni_id AND course_id = OLD.course_id;

        END IF;

        RETURN NULL; --this is an AFTER trigger
    END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trig_add_student_chatroom
AFTER INSERT ON takes
    FOR EACH ROW EXECUTE FUNCTION auto_add_or_remove_student_chatroom();

CREATE OR REPLACE TRIGGER trig_remove_student_chatroom
AFTER DELETE ON takes
    FOR EACH ROW EXECUTE FUNCTION auto_add_or_remove_student_chatroom();

COMMIT;