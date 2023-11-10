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

   