import psycopg2
import bcrypt
from tg import expose, TGController, AppConfig
from wsgiref.simple_server import make_server

# Create database connection.
conn = psycopg2.connect(
    host="localhost",
    database="commons",
    user="commons_dev",
    password="commons_dev"
)

# Create cursor to interact with the database.
cur = conn.cursor()

# Verify if an account already exists.
def verifyAccount(username,password):
    # Hash the password we receive.
    hashedPassword = password # Test
    #hashedPassword = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())

    # Check if we find a username and password that matches.
    try:
        cur.execute("SELECT * FROM test WHERE id=%s and number=%s",(username,hashedPassword)) # Test
        #cur.execute("SELECT * FROM Students WHERE username=%s and password=%s",(username,hashedPassword))
        result = cur.fetchall()
    except:
        return False

    # Returns true if authentication was a success.
    if len(result) != 0:
        return True
    # False otherwise.
    return False

# Register a new account.
def registerAccount(username,password):
    # Check if the username exists, if it does return false.
    try:
        cur.execute("SELECT * FROM test WHERE id=%s",(username)) # Test
        #cur.execute("SELECT * FROM Students WHERE username=%s",(username))
        result = cur.fetchall()
    except:
        return False
    if len(result) != 0:
        return False
    
    hashedPassword = password # Test
    #hashedPassword = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
    try:
        cur.execute("INSERT INTO test VALUES (%s,%s)",(username,hashedPassword)) # Test
        #cur.execute("INSERT INTO Students VALUES (%s,%s)",(username,hashedPassword))
    except:
        return False
    return True

# Main controller class.
class RootController(TGController):

    # Method to handle user authentication requests.
    @expose('json')
    def authenticateUserSignIn(self, username, password):
        return {"authenticationResult":verifyAccount(username,password)}

    # Method to handle new user registration.
    @expose('json')
    def registerNewUser(self, username, password):
        return {"registrationResult":registerAccount(username,password)}
    
config = AppConfig(minimal = True, root_controller = RootController())
application = config.make_wsgi_app()

print ("Serving on port 8070...")
server = make_server('', 8070, application)
server.serve_forever()