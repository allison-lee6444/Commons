
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Backend Functions
from authentication import *
from chatroom import *
from events import *
from profiles import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
"""
user="commons_dev",
password="commons_dev"
"""

# Create cursor to interact with the database.
cur = conn.cursor()

sessionid_dict = {}  # key: sessionid, value: email


# Verify if an account already exists.
def verifyAccount(email, password):
    # Check if we find a username and password that matches.
    try:
        cur.execute("SELECT salt FROM student WHERE email=%(email)s", {'email': email})
        salt = cur.fetchall()[0][0]
        hashedPassword = bcrypt.hashpw(password.encode('utf8'), salt.encode('utf8')).decode('utf8')
        # cur.execute("SELECT * FROM test WHERE id=%s and number=%s",(username,hashedPassword)) # Test
        cur.execute("SELECT * FROM student WHERE email=%(email)s and password=%(password)s",
                    {'email': email, 'password': hashedPassword})
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
    cur.execute("SELECT * FROM Student WHERE email=%(email)s", {'email': email})
    result = cur.fetchall()

    if len(result) != 0:
        return False

    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode('utf8'), salt).decode('utf8')
    salt = salt.decode('utf8')
    try:
        # cur.execute("INSERT INTO test VALUES (%s,%s)",(username,hashedPassword)) # Test
        cur.execute("INSERT INTO Student VALUES (%(email)s,%(hashedPassword)s,%(salt)s)",
                    {'email': email, 'hashedPassword': hashedPassword, 'salt': salt})
    except:
        return False
    cur.execute("SELECT * FROM Student WHERE email=%(email)s", {'email': email})
    result = cur.fetchall()
    return True


def editProfile(email, hobbies, interests, fname, lname, new_email):
    try:
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
    except:
        return False
    return True


def retrieveProfileData(email):
    cur.execute("SELECT * FROM student_profile WHERE email=%(email)s", {'email': email})
    result = cur.fetchall()
    result = json.dumps(result)
    return result


# Check if a specific chatroom has had any new messages since the provided time.
def checkForMessages(chatroomID, dateTime):
    try:
        cur.execute("SELECT * FROM message WHERE chatroom_id = %(chatroomID)s and date_time_sent > %(dateTime)s",
                    {"chatroomID": chatroomID, "dateTime": dateTime})
        result = json.dumps(cur.fetchall())
        return result
    except:
        return {"noNewMessages": True}


def changePassword(email, current_pw, new_pw):
    if not verifyAccount(email, current_pw):
        return False

    cur.execute("SELECT salt FROM student WHERE email=%(email)s", {'email': email})
    salt = cur.fetchall()[0][0]
    hashedPassword = bcrypt.hashpw(new_pw.encode('utf8'), salt.encode('utf8')).decode('utf8')

    try:
        cur.execute("UPDATE student SET password=%(hashedPassword)s WHERE email=%(email)s",
                    {'email': email, 'hashedPassword': hashedPassword})
    except:
        return False
    return True


# Main controller class.
class RootController(RestController):
    def _before(self, *remainder, **params):
        tg.response.headers.update({'Access-Control-Allow-Origin': '*'})

    @staticmethod
    def is_method(method):
        def inner(func):
            def wrapper(*args, **kwargs):
                if method == tg.request.method:
                    return func(*args, **kwargs)
                else:
                    print(f"Expect request method {method}, received {tg.request.method} instead")
                    return {"result": False}

            return wrapper

        return inner

    @staticmethod
    def check_session_id(id):
        if id in sessionid_dict:
            return sessionid_dict[id]
        else:
            return None

    # Method to handle user authentication requests.
    @expose('json')
    def authenticateUserSignIn(self, email, password):
        result = verifyAccount(email, password)
        token = 0
        if result:
            token = secrets.token_urlsafe(20)
            sessionid_dict[token] = email
        return {"result": result, "sessionid": token}

    # Method to handle new user registration.
    @expose('json')
    @is_method('POST')
    def registerNewUser(self, email, password):
        result = registerAccount(email, password)
        token = 0
        if result:
            token = secrets.token_urlsafe(20)
            sessionid_dict[token] = email
            editProfile(email, '', '', '', '', email)
        return {"result": result, "sessionid": token}

    # Method to create student profile
    @expose('json')
    @is_method('POST')
    def editStudentProfile(self, sessionid, hobbies, interests, fname, lname, new_email):
        email = self.check_session_id(sessionid)
        if email is None:
            return {"result": False}

        if email != new_email:
            sessionid_dict[sessionid] = new_email

        return {
            "result": editProfile(email, hobbies, interests, fname, lname, new_email)}

    # Method to change password
    @expose('json')
    @is_method('POST')
    def changePassword(self, sessionid, current_pw, new_pw):
        email = self.check_session_id(sessionid)
        if email is None:
            return {"result": False}

        return {"result": changePassword(email, current_pw, new_pw)}

    # Method to retrieve data of a student profile for a particular student
    @expose('json')
    def getStudentProfileData(self, sessionid):
        email = self.check_session_id(sessionid)
        return retrieveProfileData(email)

    # Method used by the front-end to check if there are any new messages.
    @expose('json')
    def newMesages(self, chatroomID, dateTime):
        return checkForMessages(chatroomID, dateTime)


config = MinimalApplicationConfigurator()
config.update_blueprint({
    'root_controller': RootController(),
})
application = config.make_wsgi_app()
print("Serving on port 8060...")

server = make_server('', 8060, application)

server.serve_forever()
