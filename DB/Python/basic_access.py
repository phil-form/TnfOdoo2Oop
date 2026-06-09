import psycopg2 as pg

# conn = pg.connect(
#     "dbname=postgres user=app password=1234 host=localhost port=5435"
# )

with pg.connect("dbname=postgres user=app password=1234 host=localhost port=5435") as conn:
    cur = conn.cursor()

    cur.execute("select * from student")
    print(cur.fetchall())
    try:
        cur.execute("INSERT INTO student VALUES (2, 'Jane', 'Smith', '2020-02-02', 'jsmith', 1010, 13, 'EG2210')")
    except pg.IntegrityError:
        conn.rollback()
    else:
        conn.commit()

    # Ne JAMAIS faire confiance à l'utilisateur !!!!
    student_name = "'; DROP TABLE student; --"
    # cur.execute("SELECT * FROM student WHERE first_name = '" + student_name + "'")
    # SELECT * FROM student WHERE first_name = ''; DROP TABLE student; --'
    # conn.commit()
    # print(cur.fetchall())

    cur.execute("select * from student WHERE last_name = %s", (student_name,))
    # SELECT * FROM student WHERE first_name = '\'; DROP TABLE student; --\''
    print(cur.fetchall())
