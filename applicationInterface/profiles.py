import json
from cursor import cur

def editProfile(email, hobbies, interests, fname, lname, new_email):
    try:
        cur.execute(f"SELECT * FROM student_profile WHERE email='{email}'")
        result = cur.fetchall()

        if len(result) != 0:
            cur.execute(
                f"UPDATE student_profile SET email='{new_email}',hobbies='{hobbies}',interests='{interests}',fname='{fname}',lname='{lname}' WHERE email='{email}'"
            )
        else:
            cur.execute(
                f"INSERT INTO student_profile(email, hobbies, interests, fname, lname) VALUES('{email}', '{hobbies}', '{interests}', '{fname}', '{lname}')"
            )
    except:
        return False
    return True

def retrieveProfileData(email):
    cur.execute(f"SELECT * FROM student_profile WHERE email='{email}'")
    result = cur.fetchall()
    result = json.dumps(result)
    return result