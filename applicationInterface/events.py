from cursor import cur
import datetime

# Create a new event.
def createEvent(eventName,hostID,description,locName,locCoord,startTime,endTime,eventID):
    try:
        cur.execute(f"INSERT INTO Event VALUES ('{eventName}',{hostID},'{description}','{locName}',{locCoord},{startTime},{endTime},{eventID})")
        return True
    except: 
        return False

# When a student hits the "join event" button.
def studentJoinEvent(eventID,studentID,chatroomID):
    try:
        cur.execute(f"INSERT INTO going_to_event VALUES ({eventID},{studentID},{chatroomID})")
        return True
    except:
        return False

# User decided to leave an event.
def deleteEvent(studentID,eventID):
    try:
        cur.execute(f"DELETE FROM going_to_event WHERE student_id = {studentID} AND event_id = {eventID}")
        return True
    except:
        return False

# Host decided to cancel an event.
def cancelEvent(hostID,eventID):
    try:
        cur.execute(f"DELETE FROM event WHERE host_id = {hostID} AND event_id = {eventID}")

        cur.execute(f"SELECT student_id FROM going_to_event WHERE event_id = {eventID}")
        result = cur.fetchall()
        for student in result:
            deleteEvent(student[0],eventID)

        return True
    except:
        return False

# Get a list of all events a user is participating in.
def getUserEvents(studentID):
    try:
        cur.execute(f"SELECT * FROM going_to_event LEFT JOIN event ON going_to_event.event_id = event.event_id WHERE going_to_event.studentID = {studentID}")
        result = cur.fetchall()
        return result
    except:
        return False

# Get a list of all courses a user is in.
def getUserCourses(studentID):
    try:
        cur.execute(f"SELECT * FROM takes LEFT JOIN section ON takes.uni_id = section.uni_id AND takes.course_id = section.course_id AND takes.section_id = section.section_id WHERE takes.student_id = {studentID}")
        result = cur.fetchall()
        return result
    except:
        return False

# Takes a DateTime object and returns a list of (CourseStartEpoch,CourseEndEpoch) for each course that meets on the same day.
def courseDataToEpoch(studentID,dateTimeObj):
    format = '%Y-%m-%d %H:%M:%S'
    output = []

    # Used to convert a day of the week to the name of the column that stores whether or not a course meets on that day.
    dayToCol = {
        "Monday":"meetsMon",
        "Tuesday":"meetsTue",
        "Wednesday":"meetsWed",
        "Thursday":"meetsThu",
        "Friday":"meetsFri",
        "Saturday":"meetsSat",
        "Sunday":"meetsSun"
    }

    # Takes the DateTime and gets the day of the week.
    dayOfWeek = dateTimeObj.strftime('%A')
    # Gets only the date from the Datetime obj.
    date = dateTimeObj.strftime('%Y-%m-%d')

    # Select (CourseStartTime,CourseEndTime) if a course meets on the same day of the week as the event and the event occurs during the
    # semester.
    # <<< [TEST - UNCOMMENT AFTER TEST] >>>
    query = (
        f"SELECT section.start_time,section.end_time"
        f" FROM takes LEFT JOIN section ON takes.uni_id = section.uni_id"
        f" AND takes.course_id = section.course_id AND takes.section_id = section.section_id WHERE "
        f"takes.student_id = {studentID} AND section.{dayToCol[dayOfWeek]} = 'True' AND section.semStartDate < "
        f"{date} AND section.semEndDate > {date}"
    )
    # <<< [TEST - UNCOMMENT AFTER TEST] >>>
    cur.execute(query) #<<< [TEST - UNCOMMENT AFTER TEST] >>>
    result = cur.fetchall() #<<< [TEST - UNCOMMENT AFTER TEST] >>>
    #result = [("07:00:00","07:59:59"),("15:00:00","16:00:00"),("16:30:00","18:30:00")] # <<< [TEST - DELETE AFTER TEST] >>>

    # For all course times, add them to the date of the event, convert them to epoch time, and add it to the output list.
    # If an event occurs during the semester, and the event day of the week is on the same day as when a class meets, there may be a conflict.
    for time in result:
        courseStartTime = date+" "+time[0]
        courseStartEpoch = (datetime.datetime.strptime(courseStartTime, format)).timestamp()
        courseEndTime = date+" "+time[1]
        courseEndEpoch = (datetime.datetime.strptime(courseEndTime, format)).timestamp()
        output.append((courseStartEpoch,courseEndEpoch))
    return output

# For a given event's start/end times and a student, return True if the student has a time conflict.  False otherwise.
def identifiedTimeConflict(startTime,endTime,studentID):
    format = '%Y-%m-%d %H:%M:%S'

    # > Convert start/end time of event into DateTime obj.
    eventStartDateTime = datetime.datetime.strptime(startTime, format)
    eventEndDateTime = datetime.datetime.strptime(endTime, format)

    # > Take the start/end DateTimes of the event and convert them into epoch values.
    startEpoch = eventStartDateTime.timestamp()
    endEpoch = eventEndDateTime.timestamp()

    # > Get all events the student is in as a list of tuples of type (EventStartEpoch,EventEndEpoch).
    cur.execute(f"SELECT event.start_time,event.end_time FROM going_to_event LEFT JOIN event ON going_to_event.event_id = event.event_id WHERE going_to_event.studentID = {studentID}") #<<< [TEST - UNCOMMENT AFTER TEST] >>>
    eventResult = cur.fetchall() #<<< [TEST - UNCOMMENT AFTER TEST] >>>
    #eventResult = [("2023-11-03 07:00:00","2023-11-03 08:30:00"),("2023-11-03 15:00:00","2023-11-03 16:00:00"),("2023-11-04 10:00:00","2023-11-04 12:00:00")] # <<< [TEST - DELETE AFTER TEST] >>>

    # Go though eventResult (ex: [("YYYY-MM-DD HH:mm:ss", "YYYY-MM-DD HH:mm:ss"), ...]) and convert them into epoch values.
    for i in range(len(eventResult)):
        newStart = (datetime.datetime.strptime(eventResult[i][0], format)).timestamp()
        newEnd = (datetime.datetime.strptime(eventResult[i][1], format)).timestamp()
        eventResult[i] = (newStart,newEnd)

    # > Get all courses the student is in as a list of tuples of type (CourseStartEpoch,CourseEndEpoch).
    courseResult = []
    courseResult.extend(courseDataToEpoch(studentID,eventStartDateTime))
    # If the event is on different dates ...
    eventStartDate = eventStartDateTime.strftime('%Y-%m-%d')
    eventEndDate = eventEndDateTime.strftime('%Y-%m-%d')
    if (eventStartDate != eventEndDate):
        courseResult.extend(courseDataToEpoch(studentID,eventEndDateTime))

    # > Go through the scheduled events/courses on the same days as the event and see if a conflict exists.
    schedule = eventResult + courseResult
    for i in schedule:
        if (startEpoch <= i[1]) and (endEpoch >= i[0]):
            return True
    return False