import bcrypt
from fastapi import HTTPException

from cursor import cur

def check_login(email, password):
    # Check if we find a username and password that matches.
    try:
        cur.execute("SELECT salt FROM student WHERE email=%(email)s", {'email': email})
        salt = cur.fetchall()[0][0]
        hashed_password = bcrypt.hashpw(password.encode('utf8'), salt.encode('utf8')).decode('utf8')
        # cur.execute("SELECT * FROM test WHERE id=%s and number=%s",(username,hashed_password)) # Test
        cur.execute("SELECT * FROM student WHERE email=%(email)s and password=%(password)s",
                    {'email': email, 'password': hashed_password})
        result = cur.fetchall()
    except BaseException as e:
        print(f'Exception: {e}')
        return False

    # Should only have 1 account
    if len(result) == 1:
        return True
    return False


# Register a new account.
def register_account(email, password):
    # Check if the username exists, if it does return false.
    cur.execute("SELECT * FROM student WHERE email=%(email)s", {'email': email})
    result = cur.fetchall()

    if len(result) != 0:
        return False

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf8'), salt).decode('utf8')
    salt = salt.decode('utf8')
    try:
        cur.execute("INSERT INTO student (email, password, salt) VALUES (%(email)s,%(hashed_password)s,%(salt)s)",
                    {'email': email, 'hashed_password': hashed_password, 'salt': salt})
        cur.execute("SELECT * FROM student WHERE email=%(email)s", {'email': email})

    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    return True


def change_password(email, current_pw, new_pw):
    if not check_login(email, current_pw):
        return False

    cur.execute("SELECT salt FROM student WHERE email=%(email)s", {'email': email})
    salt = cur.fetchall()[0][0]
    hashed_password = bcrypt.hashpw(new_pw.encode('utf8'), salt.encode('utf8')).decode('utf8')

    try:
        cur.execute("UPDATE student SET password=%(hashed_password)s WHERE email=%(email)s",
                    {'email': email, 'hashed_password': hashed_password})
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    return True

