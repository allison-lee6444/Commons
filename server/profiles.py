from fastapi import HTTPException

student_uni_id_cache = {}  # need to solve the race condition by too frequent call of get_student_uni_id


def is_verified(cur, email):
    return {'verified': get_student_uni_id(cur, email) != (None, None)}


def edit_profile(cur, email, hobbies, interests, fname, lname, new_email):
    try:
        cur.execute("SELECT * FROM student WHERE email=%(email)s", {'email': email})
        result = cur.fetchall()

        if len(result) != 0:
            cur.execute(
                "UPDATE student SET email=%(new_email)s,hobbies=%(hobbies)s,interests=%(interests)s,"
                "fname=%(fname)s,lname=%(lname)s WHERE email=%(email)s",
                {'email': email, 'new_email': new_email, 'hobbies': hobbies, 'interests': interests, 'fname': fname,
                 'lname': lname}
            )
        else:
            raise LookupError('Cannot find an account associated with this email address')
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    cur.execute("COMMIT")
    return True


def get_profile(cur, email):
    try:
        cur.execute("SELECT student_id, uni_id, email, graduation_year, major, hobbies, interests, fname, lname"
                    " FROM student WHERE email=%(email)s", {'email': email})
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    result = cur.fetchall()
    return {'result': result}


def get_student_uni_id(cur, email):
    if email in student_uni_id_cache:  # cache hit!
        return student_uni_id_cache[email]

    try:
        cur.execute("SELECT student_id, uni_id FROM student WHERE email=%(email)s", {'email': email})
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    result = cur.fetchone()
    student_uni_id_cache[email] = result
    return result
