from server import flashcard
import json

def test_create_flashcard(postgresql):
    with open('database/create_tables.sql', 'r') as sqlfile:
        cur = postgresql.cursor()
        cur.execute(sqlfile.read())
    cur = postgresql.cursor()

    cur.execute("INSERT INTO university values('NYU')")
    cur.execute("INSERT INTO chatroom(chatroom_name, uni_id) VALUES('some_chatroom', 'NYU')")

    cur.execute("SELECT id FROM chatroom")
    chatroom_id = cur.fetchall()[0][0]
    front_text = 'front'
    back_text = 'back'

    flashcard.createFlashcard(cur, chatroom_id, front_text, back_text)

    cur.execute("SELECT front FROM flashcard")
    get_front = cur.fetchall()[0][0]
    assert(get_front == 'front')

def test_delete_flashcard(postgresql):
    with open('database/create_tables.sql', 'r') as sqlfile:
        cur = postgresql.cursor()
        cur.execute(sqlfile.read())
    cur = postgresql.cursor()

    cur.execute("INSERT INTO university values('NYU')")
    cur.execute("INSERT INTO chatroom(chatroom_name, uni_id) VALUES('some_chatroom', 'NYU')")

    cur.execute("SELECT id FROM chatroom")
    chatroom_id = cur.fetchall()[0][0]
    front_text = 'front'
    back_text = 'back'

    cur.execute('INSERT INTO flashcard(front, back, chatroom_id) VALUES(%(front_text)s, %(back_text)s, %(chatroom_id)s)',
                {"front_text" : front_text, "back_text" : back_text, "chatroom_id" : chatroom_id})
    
    flashcard.deleteFlashcard(cur, chatroom_id, front_text, back_text)
    cur.execute('SELECT * FROM flashcard')
    card = cur.fetchall()

    assert(len(card)==0)

def test_get_flashcards(postgresql):
    with open('database/create_tables.sql', 'r') as sqlfile:
        cur = postgresql.cursor()
        cur.execute(sqlfile.read())
    cur = postgresql.cursor()
    cur.execute("INSERT INTO university values('NYU')")
    cur.execute("INSERT INTO chatroom(chatroom_name, uni_id) VALUES('some_chatroom', 'NYU')")

    cur.execute("SELECT id FROM chatroom")
    chatroom_id = cur.fetchall()[0][0]
    front_text = 'front'
    back_text = 'back'

    cur.execute('INSERT INTO flashcard(front, back, chatroom_id) VALUES(%(front_text)s, %(back_text)s, %(chatroom_id)s)',
                {"front_text" : front_text, "back_text" : back_text, "chatroom_id" : chatroom_id})
    
    test = flashcard.getFlashcards(cur, chatroom_id)
    test = json.loads(test)

    #a = 1
    #assert(a == 1)
    assert (test[0] == [1, 'front', 'back', 1])

def test_edit_flashcard(postgresql):
    with open('database/create_tables.sql', 'r') as sqlfile:
        cur = postgresql.cursor()
        cur.execute(sqlfile.read())
    cur = postgresql.cursor()

    cur.execute("INSERT INTO university values('NYU')")
    cur.execute("INSERT INTO chatroom(chatroom_name, uni_id) VALUES('some_chatroom', 'NYU')")

    cur.execute("SELECT id FROM chatroom")
    chatroom_id = cur.fetchall()[0][0]
    front_text = 'front'
    back_text = 'back'

    cur.execute('INSERT INTO flashcard(front, back, chatroom_id) VALUES(%(front_text)s, %(back_text)s, %(chatroom_id)s)',
                {"front_text" : front_text, "back_text" : back_text, "chatroom_id" : chatroom_id})
    
    # get flashcard id
    cur.execute("SELECT id FROM flashcard")
    flashcard_id = cur.fetchall()[0][0]
    
    flashcard.editFlashcard(cur, flashcard_id, 'abc', 'def')

    cur.execute("SELECT front, back FROM flashcard WHERE id = %(flashcard_id)s", {'flashcard_id' : flashcard_id})
    front, back = cur.fetchall()[0]

    assert(front == 'abc' and back == 'def')

