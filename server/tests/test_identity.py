from server import identity
from db import make_db
from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql",make_db]
)
postgresql = factories.postgresql("postgresql_proc")

def test_verify_uni_email():
    cur = postgresql.cursor()
    make_db(postgresql)
    # uses inserts for fake server sql
    assert identity.verify_uni_email(cur,'abc123@nyu.edu')['emailExists'] == True 

def test_retrieve_verification_status():
    cur = postgresql.cursor()
    make_db(postgresql)
    assert identity.retrieve_verification_status(cur,'abc123@nyu.edu')['verified'] == False

