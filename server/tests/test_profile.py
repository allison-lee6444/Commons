from server import profiles


def test_get_student_id(postgresql):
    with open('database/create_tables.sql', 'r') as sqlfile:
        cur = postgresql.cursor()
        cur.execute(sqlfile.read())
    cur = postgresql.cursor()
    cur.execute(
        "INSERT INTO student (student_id, uni_id, email, password, salt) VALUES (123,'NYU','a@nyu.edu','p','s')"
    )
    assert profiles.get_student_uni_id(cur, 'a@nyu.edu') == (123, 'NYU')
