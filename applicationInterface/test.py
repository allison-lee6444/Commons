import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="commons",
    #user="postgres",
    #password="root"
    user="commons_dev",
    password="commons_dev"
)

cur = conn.cursor()

def createProfile(student_id, uni_id, name, graduation_year, major, hobbies, interests):
    cur.execute(f"INSERT INTO student_profile VALUES(%s, %s, %s, %s, %s, %s, %s)", (student_id, uni_id, name, graduation_year, major, hobbies, interests))

uni_id = 'NYU'
cur.execute(f"INSERT INTO university VALUES(%s)", [uni_id])
cur.execute(f"SELECT * FROM university")
print(cur.fetchall())
#cur.execute(f"INSERT INTO student VALUES(%s, %s)", [('xyz@nyu.edu', 'pass')])
#cur.execute(f"INSERT INTO attends VALUES(%s, %s, %s)", [('xyz@nyu.edu', '75942890865', 'NYU')])
#createProfile(f"75942890865', 'NYU', 'XYZ', '2024', 'pre-med", 'kayacking', 'medicine')
   