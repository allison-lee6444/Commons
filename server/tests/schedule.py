from server import schedule

from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"],
)
postgresql = factories.postgresql("postgresql_proc")