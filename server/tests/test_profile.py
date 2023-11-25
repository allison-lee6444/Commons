def test_get_student_id(postgresql):
    with open('database/create_tables.sql', 'r') as sqlfile:
        cur = postgresql.cursor()
        cur.execute(sqlfile.read())
    cur = postgresql.cursor()
    cur.execute(
        "INSERT INTO student (student_id, uni_id, email, password, salt) VALUES (123,'NYU','a@nyu.edu','p','s')"
    )
    cur.execute("SELECT student_id,uni_id FROM student WHERE email=%(email)s", {'email': 'a@nyu.edu'})
    result = cur.fetchone()
    assert result == (123, 'NYU')
