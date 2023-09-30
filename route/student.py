from flask import Blueprint, render_template, request, redirect
import sqlite3 as sql
from config import execute_query

students = Blueprint('students', __name__)


# ** filter db and get all data and throw to student list page
@students.route('/admin/student')
def student():
    # Get the page number from the query parameters (default to 1 if not present)
    page = request.args.get('page', 1, type=int)

    # Define the number of records per page
    records_per_page = 10

    # Calculate the offset based on the current page
    offset = (page - 1) * records_per_page

    # Use the helper function to execute the query
    rows = execute_query("SELECT * FROM students LIMIT ? OFFSET ?", (records_per_page, offset))

    # Calculate the total number of pages
    total_records = execute_query("SELECT COUNT(*) FROM students")[0][0]
    total_pages = (total_records // records_per_page) + (total_records % records_per_page > 0)

    return render_template('admin/student/index.html', rows=rows, page=page, total_pages=total_pages)


# ** load to add student page
@students.route('/admin/add_student')
def add_student():
    return render_template('admin/student/add_student.html')


# ** student added to db
@students.route('/admin/student_added', methods=['POST'])
def student_added():
    if request.method == "POST":
        try:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            birthday = request.form['birthday']
            gender = request.form['gender']
            email = request.form['email']
            phone = request.form['phone']
            subject = request.form['subject']

            # ** using execute_query function from config.py with is_insert=True, so commit will be executed if insert is correct
            query = "INSERT INTO students (firstName,lastName,birthday,gender,email,phoneNumber,subject) VALUES (?,?,?,?,?,?,?)"
            params = (firstname, lastname, birthday, gender, email, phone, subject)
            execute_query(query, params, is_insert=True)

            msg = "Record successfully added"
            return redirect('/admin/student')
        except:
            msg = "error in insert operation"


# ** get student detail from student page or detail page to filter db and throw to edit page
@students.route('/admin/edit_student', methods=['GET', 'POST'])
def edit_student():
    if request.method == 'POST':
        student_sid = request.form.get("sid", None)

        # ** student_sid pass as parameter to prevent sql injection
        query = f"SELECT * FROM students WHERE sid = ?"
        rows = execute_query(query, (student_sid,))

        return render_template('admin/student/edit_student.html', rows=rows)
    else:
        return render_template('admin/student/index.html')


# ** Student edit or update to db
@students.route('/admin/student_edited', methods=['POST'])
def student_edited():
    if request.method == "POST":
        try:
            sid = request.form['sid']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            birthday = request.form['birthday']
            gender = request.form['gender']
            email = request.form['email']
            phone = request.form['phone']
            subject = request.form['subject']

            query = f"UPDATE students SET " \
                    f"firstName = ?, " \
                    f"lastName = ?, " \
                    f"birthday = ?, " \
                    f"gender = ?, " \
                    f"email = ?, " \
                    f"phoneNumber = ?, " \
                    f"subject = ? " \
                    f"WHERE sid = ?"

            # ** all data pass as parameter to prevent sql injection
            params = (firstname, lastname, birthday, gender, email, phone, subject, sid)
            execute_query(query, params, is_insert=True)

            msg = "Record successfully updated"
            return redirect('/admin/student')
        except:
            msg = "error in insert operation"


# ** get student details from student page to filter db and throw to detail page
@students.route('/admin/detail_student', methods=['GET', 'POST'])
def detail_student():
    if request.method == 'POST':
        student_sid = request.form.get("sid", None)

        # ** student_sid pass as parameter to prevent sql injection
        query = f"SELECT * FROM students WHERE sid = ?"
        rows = execute_query(query, (student_sid,))

        return render_template('admin/student/detail_student.html', rows=rows)
    else:
        return render_template('admin/student/index.html')


# ** Student delete on db
@students.route('/admin/delete_student', methods=['POST'])
def delete_student():
    if request.method == "POST":
        try:
            sid = request.form['sid']
            with sql.connect("student_ss34.db") as con:
                cur = con.cursor()
                cur.execute(f"DELETE FROM students WHERE sid = '{sid}'")
                con.commit()
                msg = "Record successfully deleted"
                return redirect('/admin/student')
        except:
            con.rollback()
            msg = "error in insert operation"
