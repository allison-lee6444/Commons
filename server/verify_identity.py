# Verify a student's identity through their university institution

# AL: how??? arent we just blindly accepting inputs? are there plans to use the verification functions i have written
# verification.py??

def verifyIdentity(cur, student_id, uni_id, email, fname, lname, graduation_year):
    cur.execute("SELECT * FROM attends WHERE student_id=%(student_id)s and uni_id=%(uni_id)s and email=%(email)s",
                {"student_id": student_id, "uni_id": uni_id, "email": email})
    result = cur.fetchall()
    if (len(result) == 0):
        return False
    else:
        cur.execute(
            "INSERT INTO student(student_id, uni_id, email, fname, lname, graduation_year) "
            "VALUES(%(student_id)s, %(uni_id)s, %(email)s, %(fname)s, %(lname)s, %(graduation_year)s)",
            {"student_id": student_id, "uni_id": uni_id, "email": email, "fname": fname, "lname": lname,
             "graduation_year": graduation_year})
        return True
