from server import profiles
from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"], port=8800
)
postgresql = factories.postgresql("postgresql_proc")


def make_db(cur):
    cur.execute(
        "INSERT INTO student (student_id, uni_id, email, graduation_year, major, hobbies, interests, fname, lname,"
        "password, salt)"
        "VALUES (123,'NYU','anyu@nyu.edu',2023,'Physics', 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd','p','s')"
    )


def test_is_verified(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    assert profiles.is_verified(cur, 'anyu@nyu.edu')['verified'] is True


def test_get_student_id(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    assert profiles.get_student_uni_id(cur, 'anyu@nyu.edu') == (123, 'NYU')


def test_get_profile(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    assert profiles.get_profile(cur, 'anyu@nyu.edu')['result'] == [(123, 'NYU', 'anyu@nyu.edu', 2023, 'Physics',
                                                                    'Chess, Sudoku', 'Math and science', 'Ab', 'Cd')]
    assert profiles.get_profile(cur, 'bnyu@nyu.edu')['result'] == []


def test_edit_profile(postgresql):
    cur = postgresql.cursor()
    make_db(cur)
    # normal case
    profiles.edit_profile(cur, 'anyu@nyu.edu', 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd', 'anyu@nyu.edu')
    assert profiles.get_profile(cur, 'anyu@nyu.edu')['result'] == [(123, 'NYU', 'anyu@nyu.edu', 2023, 'Physics',
                                                                    'Chess, Sudoku', 'Math and science', 'Ab', 'Cd')]

    # changing email
    profiles.edit_profile(cur, 'anyu@nyu.edu', 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd', 'bnyu@nyu.edu')
    assert profiles.get_profile(cur, 'bnyu@nyu.edu')['result'] == [(123, 'NYU', 'bnyu@nyu.edu', 2023, 'Physics',
                                                                    'Chess, Sudoku', 'Math and science', 'Ab', 'Cd')]
