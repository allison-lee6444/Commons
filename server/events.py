import json
from fastapi import HTTPException
import datetime


def serialize_datetime(obj):
    if isinstance(obj, (datetime.datetime, datetime.time, datetime.date)):
        return obj.isoformat()


# Create a event.
def create_event(cur, chatroom_id, event_name, host_id, uni_id, description, loc_name, loc_coords, start_time,
                 end_time):
    start_time = ''.join(start_time.split('GMT')[:-1])
    end_time = ''.join(end_time.split('GMT')[:-1])
    format = '%a %b %d %Y %H:%M:%S '
    start_time = datetime.datetime.strptime(start_time, format)
    end_time = datetime.datetime.strptime(end_time, format)
    try:
        cur.execute('SELECT COUNT(*) FROM event')
        (event_id,) = cur.fetchone()
        event_id += 1
        cur.execute(
            "INSERT INTO Event VALUES (%(event_name)s,%(host_id)s,%(uni_id)s,%(chatroom_id)s,%(description)s,%(loc_name)s,%(loc_coords)s,"
            "%(startTime)s,%(endTime)s,%(event_id)s)",
            {'event_name': event_name, 'host_id': host_id, 'uni_id': uni_id, 'description': description,
             'loc_name': loc_name, 'event_id': event_id,
             'loc_coords': loc_coords, 'startTime': start_time, 'endTime': end_time, 'chatroom_id': chatroom_id}
        )
        cur.execute("INSERT INTO going_to_event VALUES (%(event_id)s, %(host_id)s, %(chatroom_id)s)",
                    {'event_id': event_id, 'host_id': host_id, 'chatroom_id': chatroom_id})
        cur.execute("COMMIT")
        return event_id
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# Edit a event.
def edit_event(cur, event_name, host_id, uni_id, description, loc_name, loc_coords, start_time, end_time,
               event_id):
    start_time = ''.join(start_time.split('GMT')[:-1])
    end_time = ''.join(end_time.split('GMT')[:-1])
    format = '%a %b %d %Y %H:%M:%S '
    start_time = datetime.datetime.strptime(start_time, format)
    end_time = datetime.datetime.strptime(end_time, format)
    try:
        cur.execute(
            "SELECT * FROM event WHERE event_id=%(event_id)s", {'event_id': event_id}
        )
        result = cur.fetchall()

        if len(result) != 0:
            cur.execute(
                "UPDATE event SET event_name=%(event_name)s,host_id=%(host_id)s,uni_id=%(uni_id)s,"
                "descript=%(description)s,location_name=%(loc_name)s,"
                "location_coordinates=%(loc_coords)s,start_time=%(start_time)s,end_time=%(end_time)s "
                "WHERE event_id=%(event_id)s",
                {
                    'event_name': event_name,
                    'host_id': host_id,
                    'uni_id': uni_id,
                    'description': description,
                    'loc_name': loc_name,
                    'loc_coords': loc_coords,
                    'start_time': start_time,
                    'end_time': end_time,
                    'event_id': event_id
                }
            )
            cur.execute("COMMIT")
            return {'result': True}

        return {'result': False}
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# When a student hits the "join event" button.
def join_event(cur, event_id, student_id, uni_id):
    try:
        cur.execute("INSERT INTO going_to_event VALUES (%(eventID)s,%(studentID)s,"
                    "(SELECT chatroom_id FROM event JOIN in_chatroom USING (chatroom_id) "
                    "WHERE event_id=%(eventID)s AND student_id=%(studentID)s AND event.uni_id=%(uni_id)s))",
                    {'studentID': student_id, 'eventID': event_id, 'uni_id': uni_id})
        cur.execute("COMMIT")
        return True
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# User decided to leave an event.
def leave_event(cur, student_id, event_id):
    parameters = {'studentID': student_id, 'eventID': event_id}
    try:
        # Check if the row even exists. This is necessary as it would return True still even if it didn't exist.
        cur.execute("SELECT * FROM going_to_event WHERE student_id = %(studentID)s AND event_id = %(eventID)s",
                    parameters
                    )
        result = cur.fetchall()

        if len(result) != 0:
            cur.execute("DELETE FROM going_to_event WHERE student_id = %(studentID)s AND event_id = %(eventID)s",
                        parameters
                        )
            cur.execute("COMMIT")
            return True
        return False
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# Host decided to cancel an event.
def cancel_event(cur, host_id, event_id):
    parameters = {'eventID': event_id, 'host_id': host_id}
    try:
        # Check if the row exists.
        cur.execute("SELECT * FROM event WHERE host_id = %(host_id)s AND event_id = %(eventID)s", parameters)
        resultE = cur.fetchall()

        if len(resultE) != 0:
            cur.execute("DELETE FROM event WHERE host_id = %(host_id)s AND event_id = %(eventID)s", parameters)
            cur.execute("COMMIT")

            cur.execute("SELECT * FROM going_to_event WHERE event_id = %(eventID)s", {'eventID': event_id})
            resultGTE = cur.fetchall()

            # If there are students going to the event, delete it from the table.
            if len(resultGTE) != 0:
                cur.execute("DELETE FROM going_to_event WHERE event_id = %(eventID)s", {'eventID': event_id})
                cur.execute("COMMIT")
            return True
        return False
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# Get a list of all events a user is participating in.
def get_events(cur, student_id, uni_id):
    try:
        cur.execute(
            "SELECT going_to_event.event_id,going_to_event.chatroom_id,"
            "event.event_name,host.fname,host.lname,host.email,event.descript,event.location_name,"
            "event.start_time,event.end_time"
            " FROM going_to_event LEFT JOIN event ON going_to_event.event_id = event.event_id "
            "JOIN student AS host ON event.host_id=host.student_id AND event.uni_id=host.uni_id "
            "WHERE going_to_event.student_id = %(student_id)s",
            {'student_id': student_id, 'uni_id': uni_id}
        )

        result = json.dumps(cur.fetchall(), default=serialize_datetime)
        return result
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


def get_event(cur, event_id, student_id, uni_id):
    try:
        cur.execute(
            "SELECT event_name, fname, lname, email, descript, location_name, location_coordinates, start_time, end_time"
            ",(SELECT COUNT(*)=1 FROM going_to_event WHERE event_id=%(event_id)s AND student_id=%(student_id)s)"
            " FROM event JOIN student ON (event.host_id=student.student_id AND event.uni_id=student.uni_id) JOIN "
            "in_chatroom USING (chatroom_id) "  
            " WHERE event_id=%(event_id)s AND in_chatroom.student_id=%(student_id)s AND in_chatroom.uni_id=%(uni_id)s",
            {"event_id": event_id, "student_id": student_id, "uni_id": uni_id}
        )
        result = cur.fetchall()

        if len(result) != 1:
            print(result)
            raise LookupError("Number of records does not equal 1")
        return json.dumps(result, default=serialize_datetime)
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# Get a list of all courses a user is in.
def get_courses(cur, student_id, uni_id):
    try:
        cur.execute(
            "SELECT section.course_id,section.section_id,section.start_time,section.end_time,"
            "section.semStartDate,section.semEndDate,section.year,section.meetsMon,section.meetsTue,"
            "section.meetsWed,section.meetsThu,section.meetsFri,section.meetsSat,section.meetsSun"
            " FROM takes LEFT JOIN section ON takes.uni_id = section.uni_id AND"
            " takes.course_id = section.course_id AND takes.section_id = section.section_id WHERE "
            "takes.student_id = %(student_id)s AND takes.uni_id = %(uni_id)s",
            {'student_id': student_id, 'uni_id': uni_id})
        result = json.dumps(cur.fetchall(), default=serialize_datetime)
        return result
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# Takes a DateTime object and returns a list of (CourseStartEpoch,CourseEndEpoch) for each course that meets on the same day.
def get_courses_meeting_on_same_day(cur, student_id, event_time):
    format = '%Y-%m-%d %H:%M:%S'
    output = []

    # Takes the DateTime and gets the day of the week.
    week_meet_day = 'meets' + event_time.strftime('%A')[:3]
    # Gets only the date from the Datetime obj.
    date = event_time.strftime('%Y-%m-%d')

    # Select (CourseStartTime,CourseEndTime) if a course meets on the same day of the week as the event and the event occurs during the
    # semester.
    # <<< [TEST - UNCOMMENT AFTER TEST] >>>
    try:
        week_meet_day = 'section.meets' + event_time.strftime('%A')[:3]
        cur.execute(
            f"SELECT section.start_time,section.end_time FROM takes LEFT JOIN section ON takes.uni_id = section.uni_id AND "
            f"takes.course_id = section.course_id AND takes.section_id = section.section_id"
            f" WHERE takes.student_id = %(studentID)s AND {week_meet_day} = true "
            f"AND section.semStartDate < %(date)s AND section.semEndDate > %(date)s",
            {'studentID': student_id, 'date': date}
        )
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
        # <<< [TEST - UNCOMMENT AFTER TEST] >>>
    result = cur.fetchall()  # <<< [TEST - UNCOMMENT AFTER TEST] >>>
    # result = [("07:00:00","07:59:59"),("15:00:00","16:00:00"),("16:30:00","18:30:00")] # <<< [TEST - DELETE AFTER TEST] >>>

    # For all course times, add them to the date of the event, convert them to epoch time, and add it to the output list.
    # If an event occurs during the semester, and the event day of the week is on the same day as when a class meets, there may be a conflict.
    for time in result:
        course_start_time = date + " " + time[0].strftime('%H:%M:%S')
        course_start_epoch = (datetime.datetime.strptime(course_start_time, format)).timestamp()
        course_end_time = date + " " + time[1].strftime('%H:%M:%S')
        course_end_epoch = (datetime.datetime.strptime(course_end_time, format)).timestamp()
        output.append((course_start_epoch, course_end_epoch))
    return output


# For a given event's start/end times and a student, return True if the student has a time conflict.  False otherwise.
def has_conflict(cur, start_time, end_time, student_id, event_id):
    start_time = ''.join(start_time.split('GMT')[:-1])
    end_time = ''.join(end_time.split('GMT')[:-1])
    format = '%a %b %d %Y %H:%M:%S '

    # > Convert start/end time of event into DateTime obj.
    event_start_date_time = datetime.datetime.strptime(start_time, format)
    event_end_date_time = datetime.datetime.strptime(end_time, format)

    # > Take the start/end DateTimes of the event and convert them into epoch values.
    start_epoch = event_start_date_time.timestamp()
    end_epoch = event_end_date_time.timestamp()

    # > Get all events the student is in as a list of tuples of type (EventStartEpoch,EventEndEpoch).
    try:
        cur.execute(
            "SELECT event.start_time,event.end_time FROM going_to_event LEFT JOIN event "
            "ON going_to_event.event_id = event.event_id WHERE going_to_event.student_id = %(student_id)s"
            " AND event.event_id<>%(event_id)s",
            {'student_id': student_id, 'event_id': event_id}
        )
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    event_result = cur.fetchall()  # <<< [TEST - UNCOMMENT AFTER TEST] >>>
    # event_result = [("2023-11-03 07:00:00","2023-11-03 08:30:00"),("2023-11-03 15:00:00","2023-11-03 16:00:00"),("2023-11-04 10:00:00","2023-11-04 12:00:00")] # <<< [TEST - DELETE AFTER TEST] >>>
    # Go through event_result (ex: [(datetime_ob, datetime_obj), ...] and convert them into epoch values.
    for i in range(len(event_result)):
        new_start = (datetime.datetime.strptime(event_result[i][0].strftime(format), format)).timestamp()
        new_end = (datetime.datetime.strptime(event_result[i][1].strftime(format), format)).timestamp()
        event_result[i] = (new_start, new_end)

    # > Get all courses the student is in as a list of tuples of type (CourseStartEpoch,CourseEndEpoch).
    course_result = []
    course_result.extend(get_courses_meeting_on_same_day(cur, student_id, event_start_date_time))
    print(course_result)
    # If the event is on different dates ...
    event_start_date = event_start_date_time.strftime('%Y-%m-%d')
    event_end_date = event_end_date_time.strftime('%Y-%m-%d')
    if event_start_date != event_end_date:
        course_result.extend(get_courses_meeting_on_same_day(cur, student_id, event_end_date_time))

    # > Go through the scheduled events/courses on the same days as the event and see if a conflict exists.
    schedule = event_result + course_result
    for i in schedule:
        if (start_epoch <= i[1]) and (end_epoch >= i[0]):
            return True
    return False
