-- 3.1
INSERT INTO student
VALUES (
           33,
           'John',
           'Doe',
           '1999-01-01',
           'jdoe',
           1010,
           13,
           'EG2210'
       );

-- 3.2
INSERT INTO student (student_id,
                     first_name,
                     last_name,
                     birth_date,
                     login,
                     section_id,
                     year_result,
                     course_id)
VALUES (
           33,
           'Jane',
           'Doe',
           '1999-01-01',
           'jdoe',
           1010,
           13,
           'EG2210'
       );

-- 3.3

CREATE TABLE section_archives (
                                  section_id_archived INT PRIMARY KEY,
                                  section_name_archived VARCHAR(255) NOT NULL,
                                  delegate_id_archived INT
);

INSERT INTO section_archives
SELECT
    section_id,
    section_name,
    delegate_id
FROM section;

-- 3.4

INSERT INTO student (
    student_id,
    first_name,
    last_name,
    birth_date,
    section_id,
    year_result,
    course_id
) VALUES (
             34,
             'Alice',
             'Smith',
             '2000-02-02',
             (SELECT section_id FROM student WHERE last_name LIKE 'Reeves' LIMIT 1),
    14,
    'EG' || RIGHT(
    (
    SELECT c1.course_id FROM course c1
    JOIN professor p ON p.professor_id = c1.professor_id
    WHERE p.professor_name LIKE 'zidda'
    ), 4)
    );

-- 3.5

INSERT INTO section
SELECT 1530, 'Administration des SI', s.delegate_id
FROM section s
WHERE s.section_id = 1010;

-- 3.6

UPDATE student
SET course_id = 'EG2210'
WHERE student_id = 33;

-- 3.7

UPDATE student
set
    year_result = 18,
    last_name = 'Doe-Smith'
WHERE student_id = 34;

UPDATE student
set
    login = lower(
            LEFT(first_name, 1) || (SELECT last_name FROM student WHERE student_id = 34)
            )
WHERE student_id = 34;

-- 3.8

UPDATE student
set year_result = 15
WHERE section_id = 1010;

-- 3.9

UPDATE section
SET delegate_id = (SELECT student_id
                   FROM student
                   WHERE first_name = 'Keanu' AND last_name = 'Reeves');
-- 3.10

UPDATE section
SET delegate_id = (
    SELECT delegate_id
    FROM section
    WHERE section_id = 1320
),
    section_name = (
        SELECT section_name
        FROM section
        WHERE section_id = 1320
    )
WHERE section_id = 1530;

-- 3.11

UPDATE section
set delegate_id = student.student_id
    FROM section s2
    JOIN student ON s2.section_id = student.section_id
WHERE student.last_name = 'Milano' AND s2.section_id = section.section_id;

-- 3.12

DELETE FROM student WHERE student_id = 34;

-- 3.13

DELETE FROM student WHERE student_id = 33 OR (first_name = 'Kim' AND last_name = 'Basinger');

-- 3.14

DELETE FROM student WHERE year_result < 8;

-- 3.15

DELETE FROM course WHERE
    professor_id IS NULL
                      OR professor_id NOT IN (SELECT professor_id FROM professor);

-- 3.16

BEGIN TRANSACTION;

-- SET CONSTRAINTS ALL DEFERRED;
ALTER TABLE student DROP CONSTRAINT fk_student_section;
ALTER TABLE course DROP  CONSTRAINT fk_course_professor;
ALTER TABLE professor DROP CONSTRAINT fk_professor_section;

DELETE FROM section;
DELETE FROM professor;
DELETE FROM student;
DELETE from course;
DELETE FROM grade;

COMMIT TRANSACTION;










