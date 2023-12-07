import json
from fastapi import HTTPException


def createFlashcard(cur, chatroom_id, front_text, back_text):
    try:
        cur.execute(
            "INSERT INTO flashcard(chatroom_id, front, back) VALUES(%(chatroom_id)s, %(front_text)s, %(back_text)s)",
            {"chatroom_id": chatroom_id, "front_text": front_text, "back_text": back_text})
        cur.execute("COMMIT")
        return True
    except:
        return False


def deleteFlashcard(cur, chatroom_id, front_text, back_text):
    try:
        cur.execute(
            "DELETE FROM flashcard WHERE chatroom_id = %(chatroom_id)s AND front = %(front_text)s AND back = %(back_text)s",
            {"chatroom_id": chatroom_id, "front_text": front_text, "back_text": back_text})
        cur.execute("COMMIT")

        return True
    except:
        return False


def getFlashcards(cur, chatroom_id):
    try:
        cur.execute("SELECT * FROM flashcard WHERE chatroom_id = %(chatroom_id)s", {'chatroom_id': chatroom_id})
        return (json.dumps(cur.fetchall()))
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )
    
def editFlashcard(cur, flashcard_id, new_front, new_back):
    try:
        cur.execute("UPDATE flashcard SET front = %(new_front)s, back = %(new_back)s WHERE id = %(flashcard_id)s", 
                    {"new_front" : new_front, "new_back" : new_back, "flashcard_id" : flashcard_id})
    except BaseException as e:
        print(f'Exception: {e}')
        raise HTTPException(
            status_code=500,
            detail="Database Error",
        )   
