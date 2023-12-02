from server import profiles
from db import make_db
from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"],port=8800
)
postgresql = factories.postgresql("postgresql_proc")

def test_request_profile(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    assert profiles.request_profile(cur,'abc123@nyu.edu') == True

def test_get_student_id(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    cur.execute(
        "INSERT INTO student (student_id, uni_id, email, password, salt) VALUES (123,'NYU','anyu@nyu.edu','p','s')"
    )
    assert profiles.get_student_uni_id(cur, 'anyu@nyu.edu') == (123, 'NYU')


def test_get_profile(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    cur.execute(
        "INSERT INTO student (student_id, uni_id, email, graduation_year, major, hobbies, interests, fname, lname,"
        "password, salt)"
        "VALUES (123,'NYU','anyu@nyu.edu',2023,'Physics', 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd','p','s')"
    )
    assert profiles.get_profile(cur, 'anyu@nyu.edu')['result'] == [(123, 'NYU', 'anyu@nyu.edu', 2023, 'Physics',
                                                                 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd')]
    assert profiles.get_profile(cur, 'bnyu@nyu.edu')['result'] == []


def test_edit_profile(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    cur.execute(
        "INSERT INTO student (email, password, salt) VALUES ('anyu@nyu.edu','p','s')"
    )  # password and salt has not null constraint, must fill out first

    # normal case
    profiles.edit_profile(cur, 'anyu@nyu.edu', 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd', 'anyu@nyu.edu')
    assert profiles.get_profile(cur, 'anyu@nyu.edu')['result'] == [(None, None, 'anyu@nyu.edu', None, None,
                                                                 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd')]

    # changing email
    profiles.edit_profile(cur, 'anyu@nyu.edu', 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd', 'bnyu@nyu.edu')
    assert profiles.get_profile(cur, 'bnyu@nyu.edu')['result'] == [(None, None, 'bnyu@nyu.edu', None, None,
                                                                 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd')]
