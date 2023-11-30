import datetime
from ..server.cursor import cur

# Go through the takes table, identify which courses are old based on semester end date, and delete them from takes.
def del_old_courses():
    cur.execute("SELECT * FROM takes")

# Ask university_server for the student's schedule, if the current date is during the semester, add it to takes.
def add_new_courses():
    pass

del_old_courses()
add_new_courses()