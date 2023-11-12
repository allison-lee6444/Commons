from cursor import cur

def createFlashcard(chatroom_id, front_text, back_text):
    try:
        cur.execute(f"INSERT INTO flashcard(chatroom_id, front, back) VALUES({chatroom_id}, '{front_text}', '{back_text}')")
        return True
    except:
        return False
    
def deleteFlashcard(chatroom_id, front_text, back_text):
    try:
        cur.execute(f"DELETE FROM flashcard WHERE chatroom_id = {chatroom_id} AND front = '{front_text}' AND back = '{back_text}'")
        return True
    except:
        return False
    
