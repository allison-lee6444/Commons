from cursor import cur
from fastapi import HTTPException


def edit_profile(email, hobbies, interests, fname, lname, new_email):
    try:
        cur.execute(
            "UPDATE student SET email=%(new_email)s WHERE email=%(email)s", {'email': email, 'new_email': new_email}
        )
        cur.execute("SELECT * FROM student_profile WHERE email=%(email)s", {'email': email})
        result = cur.fetchall()

        if len(result) != 0:
            cur.execute(
                "UPDATE student_profile SET email=%(new_email)s,hobbies=%(hobbies)s,interests=%(interests)s,"
                "fname=%(fname)s,lname=%(lname)s WHERE email=%(email)s",
                {'email': email, 'new_email': new_email, 'hobbies': hobbies, 'interests': interests, 'fname': fname,
                 'lname': lname}
            )
        else:
            cur.execute(
                "INSERT INTO student_profile(email, hobbies, interests, fname, lname) VALUES(%(new_email)s, %(hobbies)s,"
                "%(interests)s, %(fname)s, %(lname)s)",
                {'new_email': new_email, 'hobbies': hobbies, 'interests': interests, 'fname': fname,
                 'lname': lname}
            )
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    return True


def get_profile(email):
    try:
        cur.execute("SELECT * FROM student_profile WHERE email=%(email)s", {'email': email})
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )

    result = cur.fetchall()
    return {'result': result}
