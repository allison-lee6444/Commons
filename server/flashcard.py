from cursor import cur

def createFlashcard(chatroom_id, front_text, back_text):
    try:
        cur.execute("INSERT INTO flashcard(chatroom_id, front, back) VALUES(%(chatroom_id)s, %(front_text)s, %(back_text)s)", {"chatroom_id" : chatroom_id, "front_text" : front_text, "back_text" : back_text})
        return True
    except:
        return False
    
def deleteFlashcard(chatroom_id, front_text, back_text):
    try:
        cur.execute("DELETE FROM flashcard WHERE chatroom_id = %(chatroom_id)s AND front = %(front_text)s AND back = %(back_text)s", {"chatroom_id" : chatroom_id, "front_text" : front_text, "back_text" : back_text})
        return True
    except:
        return False
    
