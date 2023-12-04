import datetime
import requests
from server import cursor
from server import schedule 

# Update student major and graduation year if it has changed.
def update_outdated_profiles(cur):
    print("Starting profile update.")
    # Get all students with a verified profile.
    cur.execute(
        "SELECT student_id,major,graduation_year FROM student WHERE student_id IS NOT NULL AND "
        "major IS NOT NULL AND graduation_year IS NOT NULL;"
    )
    result = cur.fetchall()

    for student in result:
        id = student[0]
        major = student[1]
        gradYear = student[2]

        url = f"http://localhost:8008/checkProfile?studentID={id}&major='{major}'&gradYear={gradYear}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "error" not in data:
                # There was a profile change, update our DB.
                if "no_profile_change" not in data:
                    print(data)
                    newMajor = data["major"]
                    newGradYear = data["graduation_year"]

                    cur.execute(
                        "UPDATE student SET major=%(newMajor)s, graduation_year=%(newGradYear)s "
                        "WHERE student_id=%(id)s",{'newMajor':newMajor,'newGradYear':newGradYear,'id':id}
                    )
            else:
                print("WARNING: An error was found in a request to university server.")
        else:
            print("WARNING: At least one request to university server failed. Error: "+str(response.status_code))
            print("Re-run the 'update_outdates_profiles' function to try again.\n")

    print("Completed profile update.")

# Go through the takes table, identify which courses are old based on semester end date, and delete them from takes.
def del_old_courses(cur):
    print("Starting schedule deletion.")
    currentDate = datetime.datetime.now().strftime('%Y-%m-%d')
    cur.execute(
        "DELETE FROM takes WHERE (SELECT section.semEndDate FROM section WHERE section.course_id = takes.course_id"
        " AND section.section_id = takes.section_id) < %(currentDate)s",{'currentDate':currentDate}
    )
    print("Schedule deletion complete.")

# Ask university_server for the student's schedule (only if they are verified), if the current date is during the semester, add it to takes.
# Assumption: University has up to date data.
def add_new_courses(cur):
    print("Starting schedule import.")
    # Get a list of student emails that have been verified (and had their schedule imported already).
    cur.execute("SELECT email FROM student WHERE student_id IS NOT NULL;")
    result = cur.fetchall()
    emails = [i[0] for i in result]

    # Go through email and call the same function used to import their schedule when they first register.
    # Assumption: University server will have the current schedule for the student.
    for email in emails:
        status = schedule.request_schedule(cur,email)
        if not status:
            print("Error importing schedule for student with email: "+email)
    print("Schedule import complete.")

update_outdated_profiles(cursor.cur)
del_old_courses(cursor.cur)
add_new_courses(cursor.cur)
print("Utility complete.")