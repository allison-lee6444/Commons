from fastapi import HTTPException

from cursor import cur
import datetime


# Create a new event.
def create_event(event_name, host_id, description, loc_name, loc_coords, start_time, end_time, event_id):
    try:
        cur.execute(
            "INSERT INTO Event VALUES (%(event_name)s,%(host_id)s,%(description)s,%(loc_name)s,%(loc_coords)s,"
            "%(startTime)s,%(endTime)s,%(eventID)s)",
            {'event_name': event_name, 'host_id': host_id, 'description': description, 'loc_name': loc_name,
             'loc_coords': loc_coords, 'startTime': start_time, 'endTime': end_time, 'eventID': event_id}
        )
        return True
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# When a student hits the "join event" button.
def join_event(event_id, student_id, chatroom_id):
    try:
        cur.execute("INSERT INTO going_to_event VALUES (%(eventID)s,%(studentID)s,%(chatroomID)s)",
                    {'studentID': student_id, 'eventID': event_id, 'chatroomID': chatroom_id})
        return True
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# User decided to leave an event.
def delete_event(student_id, event_id):
    try:
        cur.execute("DELETE FROM going_to_event WHERE student_id = %(studentID)s AND event_id = %(eventID)s",
                    {'studentID': student_id, 'eventID': event_id})
        return True
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# Host decided to cancel an event.
def cancel_event(host_id, event_id):
    try:
        cur.execute(
            "DELETE FROM event WHERE host_id = %(host_id)s AND event_id = %(eventID)s",
            {'eventID': event_id, 'host_id': host_id}
        )

        cur.execute("SELECT student_id FROM going_to_event WHERE event_id = %(eventID)s", {'eventID': event_id})
        result = cur.fetchall()
        for student in result:
            delete_event(student[0], event_id)
        return True
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )


# Get a list of all events a user is participating in.
def get_event(student_id):
    try:
        cur.execute(
            "SELECT * FROM going_to_event LEFT JOIN event ON going_to_event.event_id = event.event_id "
            "WHERE going_to_event.studentID = %(studentID)s", {'studentID': student_id}
        )
        result = cur.fetchall()
        return result
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )

# Get a list of all courses a user is in.
def get_courses(student_id):
    try:
        cur.execute(
            "SELECT * FROM takes LEFT JOIN section ON takes.uni_id = section.uni_id AND"
            " takes.course_id = section.course_id AND takes.section_id = section.section_id WHERE "
            "takes.student_id = %(student_id)s",
            {'student_id': student_id})
        result = cur.fetchall()
        return result
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )

# Takes a DateTime object and returns a list of (CourseStartEpoch,CourseEndEpoch) for each course that meets on the same day.
def get_courses_meeting_on_same_day(student_id, event_time):
    format = '%Y-%m-%d %H:%M:%S'
    output = []

    # Used to convert a day of the week to the name of the column that stores whether or not a course meets on that day.
    day_to_col = {
        "Monday": "meetsMon",
        "Tuesday": "meetsTue",
        "Wednesday": "meetsWed",
        "Thursday": "meetsThu",
        "Friday": "meetsFri",
        "Saturday": "meetsSat",
        "Sunday": "meetsSun"
    }

    # Takes the DateTime and gets the day of the week.
    day_of_week = event_time.strftime('%A')
    # Gets only the date from the Datetime obj.
    date = event_time.strftime('%Y-%m-%d')

    # Select (CourseStartTime,CourseEndTime) if a course meets on the same day of the week as the event and the event occurs during the
    # semester.
    # <<< [TEST - UNCOMMENT AFTER TEST] >>>
    try:
        cur.execute(
            "SELECT section.start_time,section.end_time FROM takes LEFT JOIN section ON takes.uni_id = section.uni_id AND "
            "takes.course_id = section.course_id AND takes.section_id = section.section_id"
            " WHERE takes.student_id = %(studentID)s AND section.%(day_col)s is true "
            "AND section.semStartDate < %(date)s AND section.semEndDate > %(date)s",
            {'studentID': student_id, 'day_col': day_to_col[day_of_week], 'date': date}
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
        course_start_time = date + " " + time[0]
        course_start_epoch = (datetime.datetime.strptime(course_start_time, format)).timestamp()
        course_end_time = date + " " + time[1]
        course_end_epoch = (datetime.datetime.strptime(course_end_time, format)).timestamp()
        output.append((course_start_epoch, course_end_epoch))
    return output


# For a given event's start/end times and a student, return True if the student has a time conflict.  False otherwise.
def has_conflict(start_time, end_time, student_id):
    format = '%Y-%m-%d %H:%M:%S'

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
            "ON going_to_event.event_id = event.event_id WHERE going_to_event.studentID = %(studentID)s",
            {'studentID': student_id}
        )
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    event_result = cur.fetchall()  # <<< [TEST - UNCOMMENT AFTER TEST] >>>
    # event_result = [("2023-11-03 07:00:00","2023-11-03 08:30:00"),("2023-11-03 15:00:00","2023-11-03 16:00:00"),("2023-11-04 10:00:00","2023-11-04 12:00:00")] # <<< [TEST - DELETE AFTER TEST] >>>

    # Go through event_result (ex: [("YYYY-MM-DD HH:mm:ss", "YYYY-MM-DD HH:mm:ss"), ...]) and convert them into epoch values.
    for i in range(len(event_result)):
        new_start = (datetime.datetime.strptime(event_result[i][0], format)).timestamp()
        new_end = (datetime.datetime.strptime(event_result[i][1], format)).timestamp()
        event_result[i] = (new_start, new_end)

    # > Get all courses the student is in as a list of tuples of type (CourseStartEpoch,CourseEndEpoch).
    course_result = []
    course_result.extend(get_courses_meeting_on_same_day(student_id, event_start_date_time))
    # If the event is on different dates ...
    event_start_date = event_start_date_time.strftime('%Y-%m-%d')
    event_end_date = event_end_date_time.strftime('%Y-%m-%d')
    if event_start_date != event_end_date:
        course_result.extend(get_courses_meeting_on_same_day(student_id, event_end_date_time))

    # > Go through the scheduled events/courses on the same days as the event and see if a conflict exists.
    schedule = event_result + course_result
    for i in schedule:
        if (start_epoch <= i[1]) and (end_epoch >= i[0]):
            return True
    return False
