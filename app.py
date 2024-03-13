# Name: app.py
# Author: Jay Buckwalter rf29850
# Date: 10/12/2023
#
# This page handles all API requests
# Whenever a link is clicked, this program will access the database to acquire any required information
# And call the correct page on the frontend, sending that information along to the frontend
#

import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

# Sets up a connection to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Getter for a single student
def get_student(student_id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE _id = ?', (student_id,)).fetchone()
    conn.close()
    if student is None:
        abort(404)
    return student

# Getter for a single instructor
def get_instructor(instructor_id):
    conn = get_db_connection()
    instructor = conn.execute('SELECT * FROM instructors WHERE _id = ?', (instructor_id,)).fetchone()
    conn.close()
    if instructor is None:
        abort(404)
    return instructor

# Getter for a single course
def get_course(course_id):
    conn = get_db_connection()
    course = conn.execute('SELECT * FROM courses WHERE _id = ?', (course_id,)).fetchone()
    conn.close()
    if course is None:
        abort(404)
    return course

# Getter for all of a student's courses
def get_student_courses(student_id):
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses JOIN student_courses ON courses._id = student_courses._course_id WHERE student_courses._student_id = ?', (student_id,)).fetchall()
    conn.close()
    return courses

# Getter for all of a course's students
def get_course_students(course_id):
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students JOIN student_courses ON students._id = student_courses._student_id WHERE student_courses._course_id = ?', (course_id,)).fetchall()
    conn.close()
    return students

# Getter for a course's instructor
def get_course_instructor(course_id):
    conn = get_db_connection()
    instructor = conn.execute('SELECT * FROM instructors JOIN courses ON instructors._id = courses._instructor_id WHERE courses._id = ?', (course_id,)).fetchone()
    conn.close()
    if instructor is None:
        abort(404)
    return instructor

# Getter for an instructor's courses
def get_instructor_courses(instructor_id):
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses JOIN instructors ON instructors._id = courses._instructor_id WHERE instructors._id = ?', (instructor_id,)).fetchall()
    conn.close()
    return courses

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TAGxnXGm9kpVOsuS'

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Students API --------------------------------
# Page that displays all students
@app.route('/students')
def list_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('list_students.html', students=students)

# Page that display details about one student
@app.route('/students/<int:student_id>')
def student(student_id):
    student = get_student(student_id)
    courses = get_student_courses(student_id)
    return render_template('student.html', student=student, courses=courses)

# Page for creating new students
@app.route('/students/create', methods=('GET', 'POST'))
def create_student():
    if request.method == 'POST':
        name = request.form['name']
        credits = request.form['credits']

        if not name:
            flash('Name is required!')
        elif not credits:
            flash('Credits is required!')
        elif not credits.isdigit():
            flash('Credits must be an integer!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO students (_name, _credits) VALUES (?, ?)', (name, credits))
            conn.commit()
            conn.close()
            return redirect(url_for('list_students'))

    return render_template('create_student.html')

# Page for editing existing students
@app.route('/students/<int:student_id>/edit', methods=('GET', 'POST'))
def edit_student(student_id):
    student = get_student(student_id)
    courses = get_student_courses(student_id)
    conn = get_db_connection()
    otherCourses = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        credits = request.form['credits']

        if not name:
            flash('Name is required!')
        elif not credits:
            flash('Credits is required!')
        elif not credits.isdigit():
            flash('Credits must be an integer!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE students SET _name = ?, _credits = ? WHERE _id = ?', (name, credits, student_id))
            conn.commit()
            conn.close()
            return redirect(url_for('list_students'))

    return render_template('edit_student.html', student=student, courses=courses, otherCourses=otherCourses)

# Page for entering a student's grade for a course
@app.route('/students/<int:student_id>/edit/add<int:course_id>', methods=('GET', 'POST'))
def add_student_course(student_id, course_id):
    if request.method == 'POST':
        grade = request.form['grade']
        if not grade:
            flash('grade is required!')
        elif not grade.isdigit():
            flash('grade must be an integer')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO student_courses (_grade, _student_id, _course_id) VALUES (?, ?, ?)', (grade, student_id, course_id))
            conn.commit()
            conn.close()
            return redirect(url_for('edit_student', student_id=student_id))
    return render_template('edit_grade.html')

# API request to remove a student from a course
@app.route('/students/<int:student_id>/edit/delete<int:course_id>', methods=('POST',))
def delete_student_course(student_id, course_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM student_courses WHERE _student_id = ? AND _course_id = ?', (student_id, course_id))
    conn.commit()
    conn.close()
    return redirect(url_for('edit_student', student_id=student_id))

# API request to delete a student
@app.route('/students/<int:student_id>/delete', methods=('POST',))
def delete_student(student_id):
    student = get_student(student_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE _id = ?', (student_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(student['_name']))
    return redirect(url_for('list_students'))

# Instructors API --------------------------------
# Page that display all instructors
@app.route('/instructors')
def list_instructors():
    conn = get_db_connection()
    instructors = conn.execute('SELECT * FROM instructors').fetchall()
    conn.close()
    return render_template('list_instructors.html', instructors=instructors)

# Page that displays details about a particular instructor
@app.route('/instructors/<int:instructor_id>')
def instructor(instructor_id):
    instructor = get_instructor(instructor_id)
    courses = get_instructor_courses(instructor_id)
    return render_template('instructor.html', instructor=instructor, courses=courses)

# Page for creating new studnets
@app.route('/instructors/create', methods=('GET', 'POST'))
def create_instructor():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']

        if not name:
            flash('Title is required!')
        elif not department:
            flash('Instructor ID is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO instructors (_name, _department) VALUES (?, ?)', (name, department))
            conn.commit()
            conn.close()
            return redirect(url_for('list_instructors'))

    return render_template('create_instructor.html')

# Page for editing existing students
@app.route('/instructors/<int:instructor_id>/edit', methods=('GET', 'POST'))
def edit_instructor(instructor_id):
    instructor = get_instructor(instructor_id)

    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']

        if not name:
            flash('Title is required!')
        elif not department:
            flash('Instructor ID is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE instructors SET _name = ?, _department = ? WHERE _id = ?', (name, department, instructor_id))
            conn.commit()
            conn.close()
            return redirect(url_for('list_instructors'))

    return render_template('edit_instructor.html', instructor=instructor)

# API request to delete an instructor
@app.route('/instructors/<int:instructor_id>/delete', methods=('POST',))
def delete_instructor(instructor_id):
    instructor = get_instructor(instructor_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM instructors WHERE _id = ?', (instructor_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(instructor['_name']))
    return redirect(url_for('list_instructors'))

# Courses API --------------------------------
# Page that displays all courses
@app.route('/courses')
def list_courses():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()
    return render_template('list_courses.html', courses=courses)

# Page that displays details about a course
@app.route('/courses/<int:course_id>')
def course(course_id):
    course = get_course(course_id)
    students = get_course_students(course_id)
    instructor = get_course_instructor(course_id)
    return render_template('course.html', course=course, students=students, instructor=instructor)

# Page that for creating new coruses
@app.route('/courses/create', methods=('GET', 'POST'))
def create_course():
    if request.method == 'POST':
        title = request.form['title']
        instructor_id = request.form['instructor_id']

        if not title:
            flash('Title is required!')
        elif not instructor_id:
            flash('Instructor ID is required!')
        elif not instructor_id.isdigit():
            flash('Instructor ID must be an integer')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO courses (_title, _instructor_id) VALUES (?, ?)', (title, instructor_id))
            conn.commit()
            conn.close()
            return redirect(url_for('list_courses'))

    return render_template('create_course.html')

# Page for editing existing courses
@app.route('/courses/<int:course_id>/edit', methods=('GET', 'POST'))
def edit_course(course_id):
    course = get_course(course_id)

    if request.method == 'POST':
        title = request.form['title']
        instructor_id = request.form['instructor_id']

        if not title:
            flash('Title is required!')
        elif not instructor_id:
            flash('Instructor ID is required!')
        elif not instructor_id.isdigit():
            flash('Instructor ID must be an integer!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE courses SET _title = ?, _instructor_id = ? WHERE _id = ?', (title, instructor_id, course_id))
            conn.commit()
            conn.close()
            return redirect(url_for('list_courses'))

    return render_template('edit_course.html', course=course)

# API request to delete a course
@app.route('/courses/<int:course_id>/delete', methods=('POST',))
def delete_course(course_id):
    course = get_course(course_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM courses WHERE _id = ?', (course_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(course['_title']))
    return redirect(url_for('list_courses'))