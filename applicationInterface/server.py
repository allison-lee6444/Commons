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

def createProfile(email, name):
    try:
        cur.execute(f"INSERT INTO student_profile VALUES('{email}','{name}')")
    except:
        return False
    return True

def retrieveProfileData(email):
    cur.execute(f"SELECT * FROM student_profile WHERE email = '{email}'")
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
    def createStudentProfile(self, email, name):
        return {"result":createProfile(email, name)}
    
    #Method to retrieve data of a student profile for a particular student
    @expose('json')
    def getStudentProfileData(self, email):
        return {"result":retrieveProfileData(email)}

    
config = AppConfig(minimal = True, root_controller = RootController())
application = config.make_wsgi_app()

print ("Serving on port 8070...")
server = make_server('', 8070, application)
server.serve_forever()