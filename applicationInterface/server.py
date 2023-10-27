import json

import psycopg2
import bcrypt
import tg
from tg import expose, TGController, AppConfig
from wsgiref.simple_server import make_server

# Create database connection.
conn = psycopg2.connect(
    host="localhost",
    database="commons",
    user="commons_dev",
    password="commons_dev"
)
"""
user="commons_dev",
password="commons_dev"
"""

# Create cursor to interact with the database.
cur = conn.cursor()


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

# Check if a specific chatroom has had any new messages since the provided time.
def checkForMessages(chatroomID,dateTime):
    try:
        cur.execute(f"SELECT * FROM message WHERE chatroom_id = {chatroomID} and date_time_sent > {dateTime}")
        result = json.dumps(cur.fetchall())
        return result
    except:
        return {"noNewMessages":True}

# Main controller class.
class RootController(TGController):
    def _before(self, *remainder, **params):
        tg.response.headers.update({'Access-Control-Allow-Origin': '*'})

    # Method to handle user authentication requests.
    @expose('json')
    def authenticateUserSignIn(self, email, password):
        return {"result": verifyAccount(email, password)}

    # Method to handle new user registration.
    @expose('json')
    def registerNewUser(self, email, password):
        return {"result": registerAccount(email, password)}

    # Method to create student profile
    @expose('json')
    def editStudentProfile(self,email, hobbies, interests, fname, lname,new_email):
        print(email, hobbies, interests, fname, lname,new_email)
        return {
            "result": editProfile(email,hobbies, interests, fname, lname,new_email)}

    # Method to retrieve data of a student profile for a particular student
    @expose('json')
    def getStudentProfileData(self, email):
        return retrieveProfileData(email)
    
    # Method used by the front-end to check if there are any new messages.
    @expose('json')
    def newMesages(self,chatroomID,dateTime):
        return checkForMessages(chatroomID,dateTime)


config = AppConfig(minimal=True, root_controller=RootController())
application = config.make_wsgi_app()

print("Serving on port 8060...")
server = make_server('', 8060, application)
server.serve_forever()
