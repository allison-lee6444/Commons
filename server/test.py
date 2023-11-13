import json
from cursor import cur
from chatroom import *
from events import *
from identity import *
from schedule import *

# Need to add default serial function to chatroom and remove eventID from createEvent.

# Chatroom

print("=== START: Test 1 ===")
print(checkForMessages(1,'2023-11-13 08:00:00'))
print("=== END: Test 1 ===")

# Events

print("=== START: Test 1 ===")
print(createEvent("TEST123",123456,"Teting the function.","Test City","POINT(1,2)","10:00:00","12:00:00",))
print("=== END: Test 1 ===")

# Identity

# Schedule

   