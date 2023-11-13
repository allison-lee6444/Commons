import requests
from cursor import cur
from fastapi import HTTPException

def request_profile(email):
    url = f"http://localhost:8008/getStudentProfile?email={email}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        profileData = data["profile"][0]
        profilesDict = {
            'student_id':profileData[0],
            'uni_id':profileData[1],
            'major':profileData[2],
            'graduation_year':profileData[3],
            'email':email
        }
        cur.execute("UPDATE student SET student_id=%(student_id)s, uni_id=%(uni_id)s, major=%(major)s, graduation_year=%(graduation_year)s WHERE email=%(email)s",profilesDict)
        cur.execute("COMMIT")
        
        return True
    else:
        return False

def edit_profile(email, hobbies, interests, fname, lname, new_email):
    try:
        cur.execute(
            "UPDATE student SET email=%(new_email)s WHERE email=%(email)s", {'email': email, 'new_email': new_email}
        )
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
            cur.execute(
                "INSERT INTO student(email, hobbies, interests, fname, lname) VALUES(%(new_email)s, %(hobbies)s,"
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
    cur.execute("COMMIT") # delete 
    return True


def get_profile(email):
    try:
        cur.execute("SELECT * FROM student WHERE email=%(email)s", {'email': email})
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )

    result = cur.fetchall()
    return {'result': result}
