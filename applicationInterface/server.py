import psycopg2
import bcrypt
import json

from tg import expose, TGController, AppConfig
from wsgiref.simple_server import make_server

# Create database connection.
conn = psycopg2.connect(
    host="localhost",
    database="commons",
    #user="postgres",
    #password="root"
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
def verifyAccount(email,password):
    # Hash the password we receive.
    #hashedPassword = password # Test

    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode('utf8'), salt)


    # Check if we find a username and password that matches.
    try:
        #cur.execute("SELECT * FROM test WHERE id=%s and number=%s",(username,hashedPassword)) # Test

        cur.execute(f"SELECT * FROM student WHERE email={email} and password={hashedPassword}")

        result = cur.fetchall()
    except:
        return False

    # Returns true if authentication was a success.
    if len(result) != 0:
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
    hashedPassword = bcrypt.hashpw(password.encode('utf8'), salt)
    try:
        # cur.execute("INSERT INTO test VALUES (%s,%s)",(username,hashedPassword)) # Test
        cur.execute(f"INSERT INTO Student VALUES ('{email}','{hashedPassword}')")

    except:
        return False
    return True

def createProfile(student_id, uni_id, name, graduation_year, major, hobbies, interests):
    try:
        cur.execute(f"INSERT INTO student_profile VALUES('{student_id}', '{uni_id}', '{name}', '{graduation_year}', '{major}', '{hobbies}', '{interests}')")

    except:
        return False
    return True

def retrieveProfileData(student_id, uni_id):

    cur.execute(f"SELECT * FROM student_profile WHERE student_id = '{student_id}' AND uni_id = '{uni_id}'")
    result = cur.fetchall()
    result = json.dumps(result)
    return result


# Main controller class.
class RootController(TGController):

    # Method to handle user authentication requests.
    @expose('json')
    def authenticateUserSignIn(self, email, password):
        return {"result":verifyAccount(email,password)}

    # Method to handle new user registration.
    @expose('json')
    def registerNewUser(self, email, password):
        return {"result":registerAccount(email,password)}
    
    #Method to create student profile
    @expose('json')
    def createStudentProfile(self, student_id, uni_id, name, graduation_year, major, hobbies, interests):
        return {"result":createProfile(student_id, uni_id, name, graduation_year, major, hobbies, interests)}
    
    #Method to retrieve data of a student profile for a particular student
    @expose('json')
    def getStudentProfileData(self, student_id, uni_id):
        return {"result":retrieveProfileData(student_id, uni_id)}

    
config = AppConfig(minimal = True, root_controller = RootController())
application = config.make_wsgi_app()

print ("Serving on port 8070...")
server = make_server('', 8070, application)

server.serve_forever()

