import psycopg2
from datetime import datetime
import flashcard
import chatroom

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

univ_id = 'NYU'
#cur.execute(f"INSERT INTO university VALUES(%s)", [univ_id])
cur.execute(f"SELECT * FROM university")
print(cur.fetchall())

c_id = 'CS101'
#cur.execute(f"INSERT INTO course VALUES('{c_id}', '{univ_id}')")

"""
def create_chatroom(univ_id):
    cur.execute(f"INSERT INTO chatroom(uni_id) VALUES('{univ_id}')")

def create_chatroom_v2(univ_id, course_id):
    cur.execute(f"INSERT INTO chatroom(uni_id, course_id) VALUES('{univ_id}', '{course_id}')")


create_chatroom(univ_id)
cur.execute('SELECT * FROM chatroom')
print(cur.fetchall())
#create_chatroom_v2(univ_id, c_id)
"""

print(datetime.now())

field = 'a'
#cur.execute(f"INSERT INTO student(email, password, salt) VALUES('{field}', '{field}', '{field}')")
cur.execute('SELECT * FROM student')
print(cur.fetchall())
s_id = 1
chatroom_id = 10
#cur.execute(f"INSERT INTO attends(email, student_id, uni_id) VALUES('{field}', '{s_id}', '{univ_id}')")
#cur.execute(f"INSERT INTO in_chatroom(student_id, uni_id, chatroom_id) VALUES('{s_id}', '{univ_id}', '{chatroom_id}')")
"""
def saveMessage(sender_id, chatroomID, message_sent):
    date_time_sent = datetime.now()
    cur.execute(f"INSERT INTO message(sender_id, chatroom_id, message_text, date_time_sent) VALUES('{sender_id}', '{chatroomID}', '{message_sent}', '{date_time_sent}')")

saveMessage('1', '10', 'new message')
cur.execute(f"SELECT * FROM message")
print(cur.fetchall())


cur.execute(f"SELECT * FROM chatroom")
print(cur.fetchall())
"""



def createChatroom(user_id, chatroom_name, uni_id):
    cur.execute("INSERT INTO chatroom(chatroom_name, uni_id) VALUES(%(chatroom_name)s, %(uni_id)s)", {"chatroom_name" : chatroom_name, "uni_id" : uni_id})
    cur.execute("SELECT id FROM chatroom where chatroom_name = %(chatroom_name)s   AND uni_id = %(uni_id)s", {"chatroom_name" : chatroom_name, "uni_id" : uni_id})
    chatroom_id = cur.fetchall()[0][0]
    

#createChatroom("a", "Rubix Cube Club", "NYU")

flashcard.createFlashcard('7', 'abc', 'def')
print(flashcard.getFlashcards('7'))

import random
import string

invite_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
print(invite_id)

#cur.execute("INSERT INTO attends VALUES('a', '123', 'NYU')")
cur.execute("SELECT * FROM attends")
print(cur.fetchall()[0][0])

#cur.execute("INSERT INTO course VALUES('CS101', 'NYU')")
#cur.execute("INSERT INTO section VALUES('CS101', 'NYU', 'A')")
#cur.execute("INSERT INTO in_chatroom(student_id, uni_id, chatroom_id) VALUES('123', 'NYU', '7')")

print(chatroom.saveMessage('123', '7', 'hello'))
cur.execute("SELECT * FROM message")
print(cur.fetchall())