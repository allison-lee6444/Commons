import psycopg2
import bcrypt
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
    hashedPassword = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())

    # Check if we find a username and password that matches.
    try:
        #cur.execute("SELECT * FROM test WHERE id=%s and number=%s",(username,hashedPassword)) # Test
        cur.execute("SELECT * FROM student WHERE email=%s and password=%s",(email,hashedPassword))
        result = cur.fetchall()
    except:
        return False

    # Returns true if authentication was a success.
    if len(result) != 0:
        return True
    # False otherwise.
    return False

# Register a new account.
def registerAccount(email,password):
    # Check if the username exists, if it does return false.
    try:
        #cur.execute("SELECT * FROM test WHERE id=%s",(username)) # Test
        cur.execute("SELECT * FROM Students WHERE email=%s",(email))
        result = cur.fetchall()
    except:
        return False
    if len(result) != 0:
        return False
    
    hashedPassword = password # Test
    #hashedPassword = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
    try:
        #cur.execute("INSERT INTO test VALUES (%s,%s)",(username,hashedPassword)) # Test
        cur.execute("INSERT INTO Students VALUES (%s,%s)",(email,hashedPassword))
    except:
        return False
    return True

def createProfile(student_id, uni_id, name, graduation_year, major, hobbies, interests):
    try:
        cur.execute('INSERT INTO student_profile VALUES(%s, %s, %s, %s, %s, %s, %s)', (student_id, uni_id, name, graduation_year, major, hobbies, interests))
    except:
        return False
    return True

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
    
    @expose('json')
    def createStudentProfile(self, student_id, uni_id, name, graduation_year, major, hobbies, interests):
        return {"result":createProfile(student_id, uni_id, name, graduation_year, major, hobbies, interests)}
    
config = AppConfig(minimal = True, root_controller = RootController())
application = config.make_wsgi_app()

print ("Serving on port 8070...")
server = make_server('', 8070, application)
server.serve_forever()