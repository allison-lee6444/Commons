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

def createProfile(student_id, uni_id, name, graduation_year, major, hobbies, interests):
    try:
        cur.execute('INSERT INTO student_profile VALUES(%s, %s, %s, %s, %s, %s, %s)', (student_id, uni_id, name, graduation_year, major, hobbies, interests))
    except:
        return False
    return True

class RootController(TGController):

    @expose('json')
    def createStudentProfile(self, student_id, uni_id, name, graduation_year, major, hobbies, interests):
        return {"result":createProfile(student_id, uni_id, name, graduation_year, major, hobbies, interests)}




config = AppConfig(minimal = True, root_controller = RootController())
application = config.make_wsgi_app()

print ("Serving on port 8070...")
server = make_server('', 8070, application)
server.serve_forever()