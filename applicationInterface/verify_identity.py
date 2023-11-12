from cursor import cur

#Verify a student's identity through their university institution
def verifyIdentity(student_id, uni_id, email, fname, lname, graduation_year):
    cur.execute(f"SELECT * FROM attends WHERE student_id='{student_id}' and uni_id='{uni_id}' and email='{email}'")
    result = cur.fetchall()
    if (len(result) == 0):
        return False
    else:
        cur.execute(f"INSERT INTO student_profile(student_id, uni_id, email, fname, lname, graduation_year) VALUES('{student_id}', '{uni_id}', '{email}', '{fname}', '{lname}', '{graduation_year}')")
        return True