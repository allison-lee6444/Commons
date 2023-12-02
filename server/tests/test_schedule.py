from server import schedule
from db import make_db
from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"],port=8900
)
postgresql = factories.postgresql("postgresql_proc")

def test_request_schedule(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    cur.execute("DELETE FROM takes WHERE student_id=123456;")
    assert schedule.request_schedule(cur,'abc123@nyu.edu') == True


