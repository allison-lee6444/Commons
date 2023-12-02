"""import json
from cursor import cur
from chatroom import *
from events import *
from identity import *
from schedule import *"""

"""
print("=== START: Test 3 ===")
print("")
print()
print("=== END: Test 3 ===")
"""

def add(a,b):
    return a+b

"""# 3 Test Students / Should fail for subsequent tests.
try:
    cur.execute("INSERT INTO student VALUES('a@nyu.edu','A','SALT')")
    cur.execute("INSERT INTO student VALUES('b@nyu.edu','B','SALT')")
    cur.execute("INSERT INTO student VALUES('c@nyu.edu','C','SALT')")
    cur.execute("INSERT INTO attends VALUES ('a@nyu.edu',111111,'NYU')")
    cur.execute("INSERT INTO attends VALUES ('b@nyu.edu',222222,'NYU')")
    cur.execute("INSERT INTO attends VALUES ('c@nyu.edu',333333,'NYU')")
    cur.execute("INSERT INTO takes VALUES(111111,'NYU','CS-UY 1234','A')")
    cur.execute("INSERT INTO takes VALUES(222222,'NYU','CS-UY 1234','A')")
    cur.execute("INSERT INTO takes VALUES(333333,'NYU','CS-UY 1234','A')")
    cur.execute("INSERT INTO in_chatroom VALUES (111111,'NYU','CS-UY 1234',1)")
    cur.execute("INSERT INTO in_chatroom VALUES (222222,'NYU','CS-UY 1234',1)")
    cur.execute("INSERT INTO in_chatroom VALUES (333333,'NYU','CS-UY 1234',1)")
except Exception as e:
    print(e)

# Chatroom - Complete

print("=== START: Test 1 ===")
print("Will return a JSON if successful.")
print(get_msg_update(1,'2023-11-13 08:00:00'))
print("=== END: Test 1 ===")

print()

print("=== START: Test 2 ===")
print("Save a new message!")
print()
cur.execute("SELECT * FROM Message")
print("Message:")
print(cur.fetchall())
print()
print("Expected: True and new message saved.")
#cur.execute("DELETE FROM message WHERE sender_id=123456 AND chatroom_id=1")
print(saveMessage(123456,1,"TESTING SAVE TO CHAT 1."))
print()
cur.execute("SELECT * FROM Message")
print("Message:")
print(cur.fetchall())
print()

print("=== END: Test 2 ===")

print()

print("=== START: Test 3 ===")
print("Should return all messages in the chatroom.")
print(retrieveMessages(1))
print("=== END: Test 3 ===")

print()

print("=== START: Test 4 ===")
print("Get chatrooms is not functional yet.")
print()
print("=== END: Test 4 ===")

print()

# Events - Complete

print("=== START: Test 5 ===")
print("Creating an insert, will return true if successful.")
try:
    cur.execute("DELETE FROM Event WHERE event_name='TEST123'")
except:
    print("ERROR: Something went wrong when trying to remove the entry.")
print(create_event("TEST123",123456,"NYU","Testing the function.","Test City",'(1,2)','2023-11-13 10:00:00','2023-11-13 12:00:00'))
print("=== END: Test 5 ===")

print()

print("=== START: Test 6 ===")
print("Attempting to join sample event created by insert query, will return true if successful and should show up as added in table.")
print(join_event(1,123456,1))
cur.execute("SELECT * FROM going_to_event")
print(cur.fetchall())
print("=== END: Test 6 ===")

print()

print("=== START: Test 7 ===")
print("Leave event.  Should return true and be removed from table.")
print(delete_event(123456,1))
cur.execute("SELECT * FROM going_to_event")
print(cur.fetchall())
print("=== END: Test 7 ===")

print()

print("=== START: Test 8 ===")
cur.execute("SELECT event_id FROM event WHERE event_name='TEST123'")
eventID = cur.fetchall()[0]
join_event(eventID,123456,1)
join_event(eventID,111111,1)
join_event(eventID,222222,1)
join_event(eventID,333333,1)
cur.execute("SELECT * FROM Event")
print("Event:")
print(cur.fetchall())
print("Going_To_Event:")
cur.execute("SELECT * FROM going_to_event")
print(cur.fetchall())
print("---")
print("Cancel event, should remove event from table and all attendees and return true.")
print(cancel_event(123456,eventID))
cur.execute("SELECT * FROM Event")
print("Event:")
print(cur.fetchall())
print("Going_To_Event:")
cur.execute("SELECT * FROM going_to_event")
print(cur.fetchall())
print("=== END: Test 8 ===")

print()

print("=== START: Test 9 ===")
join_event(1,123456,1)
print("Should return a JSON of events a student is in.")
print(get_event(123456))
print("=== END: Test 9 ===")

print()

print("=== START: Test 10 ===")
print("Should return a JSON of courses a student is in.")
print(get_courses(123456))
print("=== END: Test 10 ===")

print()

print("=== START: Test 11 ===")
try: # Should only run once.
    delete_event(123456,654321)
    delete_event(123456,1)
except:
    pass
create_event("PARTY!!!",123456,"NYU","Testing the function. Party!","Test City",'(1,2)','2023-11-13 10:00:00','2023-11-13 12:00:00')
cur.execute("SELECT event_id FROM event WHERE event_name='PARTY!!!'")
id = cur.fetchall()[0][0]
join_event(id,123456,1)
print("Should return true or false if there is a conflict.")
print("Courses:")
print(get_courses(123456))
print("Events:")
print(get_event(123456))
print("---")
print()
print("Expected: True - During class.")
print(has_conflict('2023-11-13 08:00:00','2023-11-13 09:00:00',123456))
print()
print("Expected: False - Before class.")
print(has_conflict('2023-11-13 07:00:00','2023-11-13 07:30:00',123456))
print()
print("Expected: True - During party.")
print(has_conflict('2023-11-13 10:10:00','2023-11-13 10:30:00',123456))
print()
print("Expected: False - After party.")
print(has_conflict('2023-11-13 15:00:00','2023-11-13 17:00:00',123456))
print()
print("Expected: True - Overlap with class.")
print(has_conflict('2023-11-13 05:00:00','2023-11-13 8:10:00',123456))
print()
print("Expected: True - Overlap with class and party.")
print(has_conflict('2023-11-13 08:30:00','2023-11-13 10:20:00',123456))
print()
print("Expected: True - Overlap with party.")
print(has_conflict('2023-11-13 11:30:00','2023-11-13 13:20:00',123456))
print("=== END: Test 11 ===")

# Identity

print("=== START: Test 12 ===")
print("Identity verification from fake server.")
print()
print("Expected: True")
print(request_identity_verification('abc123@nyu.edu',123456))
print()
print("Expected: False")
print(request_identity_verification('notARealStudent@nyu.edu',777777))
print("=== END: Test 12 ===")

# Schedule

print("=== START: Test 13 ===")
cur.execute("DELETE FROM takes WHERE student_id=123456")
print("Import schedule.")
print()
cur.execute("SELECT * FROM takes")
print("Takes:")
print(cur.fetchall())
print()
print("Expected: Table to have 1 row for 123456 and true.")
print()
print(request_schedule(123456))
print()
print("Takes:")
cur.execute("SELECT * FROM takes")
print(cur.fetchall())
print("=== END: Test 13 ===")"""

   