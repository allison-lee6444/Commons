import datetime
from cursor import cur
from schedule import request_schedule

# Go through the takes table, identify which courses are old based on semester end date, and delete them from takes.
def del_old_courses():
    print("Starting schedule deletion.")
    currentDate = datetime.datetime.now().strftime('%Y-%m-%d')
    cur.execute(
        "DELETE FROM takes WHERE (SELECT section.semEndDate FROM section WHERE section.course_id = takes.course_id"
        " AND section.section_id = takes.section_id) < %(currentDate)s",{'currentDate':currentDate}
    )
    print("Schedule deletion complete.")

# Ask university_server for the student's schedule (only if they are verified), if the current date is during the semester, add it to takes.
def add_new_courses():
    print("Starting schedule import.")
    # Get a list of student emails that have been verified (and had their schedule imported already).
    cur.execute("SELECT email FROM student WHERE student_id IS NOT NULL;")
    result = cur.fetchall()
    emails = [i[0] for i in result]

    # Go through email and call the same function used to import their schedule when they first register.
    # Assumption: University server will have the current schedule for the student.
    for email in emails:
        status = request_schedule(cur,email)
        if not status:
            print("Error importing schedule for student with email: "+email)
    print("Schedule import complete.")

del_old_courses()
add_new_courses()
print("Utility complete.")