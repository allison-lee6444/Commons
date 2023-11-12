from cursor import cur

#Import student schedules
def ImportStudentSchedule(values):
    #values is a dictionary structured like this:
    # {'student_id' : 2363839, 'uni_id' : 'NYU', 'schedule' : [['CS1223', 'A'], ['CS554', 'B']]}
    # so values['schedule'] is a list of tuples which contain a course id and a section id
    try:
        student_id = values['student_id']
        uni_id = values['uni_id']
        for entry in values['schedule']:
            course_id = entry[0]
            section_id = entry[1]
            cur.execute("INSERT INTO takes(student_id, uni_id, course_id, section_id) VALUES(%(student_id)s, %(uni_id)s, %(course_id)s, %(section_id)s)", {"student_id" : student_id, "uni_id" : uni_id, "course_id" : course_id, "section_id" : section_id})
        return True
    except:
        return False