from server import chatroom

from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"],
)
postgresql = factories.postgresql("postgresql_proc")

def test_get_msg_update(postgresql):
    pass

def test_retrieveMessages(postgresql):
    pass

def test_saveMessage(postgresql):
    pass

def test_createChatroom(postgresql):
    pass

def test_getChatrooms(postgresql):
    pass