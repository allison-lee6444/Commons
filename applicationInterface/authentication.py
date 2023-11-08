import bcrypt
from cursor import cur

# Verify if an account already exists.
def verifyAccount(email, password):
    # Check if we find a username and password that matches.
    try:
        cur.execute(f"SELECT * FROM student WHERE email='{email}'")
        cur.execute(f"SELECT salt FROM student WHERE email='{email}'")
        salt = cur.fetchall()[0][0]
        hashedPassword = bcrypt.hashpw(password.encode('utf8'), salt.encode('utf8')).decode('utf8')
        # cur.execute("SELECT * FROM test WHERE id=%s and number=%s",(username,hashedPassword)) # Test
        cur.execute(f"SELECT * FROM student WHERE email='{email}' and password='{hashedPassword}'")
        result = cur.fetchall()
    except:
        return False

    # Returns true if authentication was a success.
    if len(result) == 1:
        return True
    # False otherwise.
    return False


# Register a new account.
def registerAccount(email, password):
    # Check if the username exists, if it does return false.
    cur.execute(f"SELECT * FROM Student WHERE email='{email}'")
    result = cur.fetchall()

    if len(result) != 0:
        return False

    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode('utf8'), salt).decode('utf8')
    salt = salt.decode('utf8')
    try:
        # cur.execute("INSERT INTO test VALUES (%s,%s)",(username,hashedPassword)) # Test
        cur.execute(f"INSERT INTO Student VALUES ('{email}','{hashedPassword}','{salt}')")
    except:
        return False
    cur.execute(f"SELECT * FROM Student WHERE email='{email}'")
    result = cur.fetchall()
    print(result)
    return True