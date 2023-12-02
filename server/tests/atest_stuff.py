import test
import cursor
import events

def test_test():
    assert test.add(1,2) == 3

def test_editEvent():
    # Valid chatroom.
    assert events.editEvent(cursor.cur,1,"TEST123",123456,"NYU","Testing theh function.","Test City",'(1,2)','2023-11-13 10:00:00','2023-11-13 12:00:00') == True
   
def test_join_event():
    # join event made at start
    assert events.join_event(cursor.cur,1,123456,1) == True