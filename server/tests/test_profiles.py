from server import profiles

from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc(
    load=["database/create_tables.sql"],
    port=7000
)
postgresql = factories.postgresql("postgresql_proc")

def test_request_profile(postgresql):
    pass

def test_get_student_id(postgresql):
    cur = postgresql.cursor()
    cur.execute(
        "INSERT INTO student (student_id, uni_id, email, password, salt) VALUES (123,'NYU','a@nyu.edu','p','s')"
    )
    assert profiles.get_student_uni_id(cur, 'a@nyu.edu') == (123, 'NYU')


def test_get_profile(postgresql):
    cur = postgresql.cursor()
    cur.execute(
        "INSERT INTO student (student_id, uni_id, email, graduation_year, major, hobbies, interests, fname, lname,"
        "password, salt)"
        "VALUES (123,'NYU','a@nyu.edu',2023,'Physics', 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd','p','s')"
    )
    assert profiles.get_profile(cur, 'a@nyu.edu')['result'] == [(123, 'NYU', 'a@nyu.edu', 2023, 'Physics',
                                                                 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd')]
    assert profiles.get_profile(cur, 'b@nyu.edu')['result'] == []


def test_edit_profile(postgresql):
    cur = postgresql.cursor()
    cur.execute(
        "INSERT INTO student (email, password, salt) VALUES ('a@nyu.edu','p','s')"
    )  # password and salt has not null constraint, must fill out first

    # normal case
    profiles.edit_profile(cur, 'a@nyu.edu', 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd', 'a@nyu.edu')
    assert profiles.get_profile(cur, 'a@nyu.edu')['result'] == [(None, None, 'a@nyu.edu', None, None,
                                                                 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd')]

    # changing email
    profiles.edit_profile(cur, 'a@nyu.edu', 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd', 'b@nyu.edu')
    assert profiles.get_profile(cur, 'b@nyu.edu')['result'] == [(None, None, 'b@nyu.edu', None, None,
                                                                 'Chess, Sudoku', 'Math and science', 'Ab', 'Cd')]
