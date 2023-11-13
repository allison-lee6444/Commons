import json
from cursor import cur,serialize_datetime

# Check if a specific chatroom has had any new messages since the provided time.
def checkForMessages(chatroomID,dateTime):
    try:
        cur.execute(f"SELECT * FROM message WHERE chatroom_id = {chatroomID} and date_time_sent > '{dateTime}'")
        result = json.dumps(cur.fetchall(),default=serialize_datetime)
        return result
    except:
        return {"noNewMessages":True}