from server import identity
from db import make_db
from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"],port=8700
)
postgresql = factories.postgresql("postgresql_proc")

# Removed as this was made before we verified email by verification code.
"""def test_verify_uni_email(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # uses inserts for fake server sql
    assert identity.verify_uni_email('abc123@nyu.edu') == '{"emailExists":True}'
"""
def test_retrieve_verification_status(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    assert identity.retrieve_verification_status(cur,'abc123@nyu.edu')['verified'] == True

