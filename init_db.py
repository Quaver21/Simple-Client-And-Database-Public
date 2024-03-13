# Name: init_db.py
# Author: Jay Buckwalter rf29850
#
# This file is used to initialize the database and enter initial data
#

import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Creating initial students
cur.execute("INSERT INTO students (_id, _name, _credits) VALUES (?, ?, ?)", (387, 'John Walker', 93))
cur.execute("INSERT INTO students (_id, _name, _credits) VALUES (?, ?, ?)", (209, 'David Jameson', 87))
cur.execute("INSERT INTO students (_id, _name, _credits) VALUES (?, ?, ?)", (101, 'Emma Wells', 57))
cur.execute("INSERT INTO students (_id, _name, _credits) VALUES (?, ?, ?)", (190, 'Nisha Singh ', 92))
cur.execute("INSERT INTO students (_id, _name, _credits) VALUES (?, ?, ?)", (978, 'Jack Thompson ', 100))
cur.execute("INSERT INTO students (_id, _name, _credits) VALUES (?, ?, ?)", (350, 'Ben Joseph ', 79))
cur.execute("INSERT INTO students (_id, _name, _credits) VALUES (?, ?, ?)", (270, 'Kate Jimpson', 68))

# Creating initial instructors
cur.execute("INSERT INTO instructors (_id, _name, _department) VALUES (?, ?, ?)", (456, 'Jim George', 'Statistics'))
cur.execute("INSERT INTO instructors (_id, _name, _department) VALUES (?, ?, ?)", (589, 'Kevin Mathews', 'Information Systems'))
cur.execute("INSERT INTO instructors (_id, _name, _department) VALUES (?, ?, ?)", (821, 'John Sullins ', 'Health Sciences'))
cur.execute("INSERT INTO instructors (_id, _name, _department) VALUES (?, ?, ?)", (954, 'William Robertson ', 'Physics'))
cur.execute("INSERT INTO instructors (_id, _name, _department) VALUES (?, ?, ?)", (673, 'Sandra Wilson ', 'Biology'))
cur.execute("INSERT INTO instructors (_id, _name, _department) VALUES (?, ?, ?)", (535, 'Donna Joseph', 'Computer Science'))
cur.execute("INSERT INTO instructors (_id, _name, _department) VALUES (?, ?, ?)", (990, 'Natalia Smith ', 'Chemistry'))

# Creating initial courses
cur.execute("INSERT INTO courses (_id, _title, _instructor_id) VALUES (?, ?, ?)", (9076, 'Software Engineering', 535))
cur.execute("INSERT INTO courses (_id, _title, _instructor_id) VALUES (?, ?, ?)", (1028, 'Organic Chemistry I ', 990))
cur.execute("INSERT INTO courses (_id, _title, _instructor_id) VALUES (?, ?, ?)", (7654, 'Health Informatics', 821))
cur.execute("INSERT INTO courses (_id, _title, _instructor_id) VALUES (?, ?, ?)", (8721, 'Database Systems', 589))

# Creating intial grades and links between students/courses
cur.execute("INSERT INTO student_courses (_grade, _student_id, _course_id) VALUES (?, ?, ?)", (100, 387, 9076))
cur.execute("INSERT INTO student_courses (_grade, _student_id, _course_id) VALUES (?, ?, ?)", (56, 209, 1028))
cur.execute("INSERT INTO student_courses (_grade, _student_id, _course_id) VALUES (?, ?, ?)", (81, 101, 7654))
cur.execute("INSERT INTO student_courses (_grade, _student_id, _course_id) VALUES (?, ?, ?)", (77, 190, 9076))
cur.execute("INSERT INTO student_courses (_grade, _student_id, _course_id) VALUES (?, ?, ?)", (10, 978, 1028))
cur.execute("INSERT INTO student_courses (_grade, _student_id, _course_id) VALUES (?, ?, ?)", (95, 350, 8721))
cur.execute("INSERT INTO student_courses (_grade, _student_id, _course_id) VALUES (?, ?, ?)", (88, 270, 8721))

connection.commit()
connection.close()