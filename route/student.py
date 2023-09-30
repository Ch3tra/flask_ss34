from flask import Blueprint, render_template, request, redirect
import sqlite3 as sql

students = Blueprint('students', __name__)


# ** filter db and get all data and throw to student list page
@students.route('/admin/student')
def student():
    con = sql.connect("student_ss34.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # Get the page number from the query parameters (default to 1 if not present)
    page = request.args.get('page', 1, type=int)

    # Define the number of records per page
    records_per_page = 10

    # Calculate the offset based on the current page
    offset = (page - 1) * records_per_page

    cur.execute("select * from students LIMIT ? OFFSET ?", (records_per_page, offset))
    rows = cur.fetchall()

    # Calculate the total number of pages
    cur.execute("SELECT COUNT(*) FROM students")
    total_records = cur.fetchone()[0]
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

            with sql.connect("student_ss34.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (firstName,lastName,birthday,gender,email,phoneNumber,subject) VALUES (?,?,?,?,?,?,?)",
                            (firstname,lastname,birthday,gender,email,phone,subject))
                con.commit()
                msg = "Record successfully added"
                return redirect('/admin/student')
        except:
            con.rollback()
            msg = "error in insert operation"


# ** get student detail from student page or detail page to filter db and throw to edit page
@students.route('/admin/edit_student', methods=['GET', 'POST'])
def edit_student():
    if request.method == 'POST':
        student_sid = request.form.get("sid", None)
        con = sql.connect("student_ss34.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute(f"select * from students where sid ='{student_sid}'")
        rows = cur.fetchall()
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

            with sql.connect("student_ss34.db") as con:
                cur = con.cursor()
                cur.execute(f"update students set "
                            f"firstName = '{firstname}', "
                            f"lastName = '{lastname}', "
                            f"birthday = '{birthday}', "
                            f"gender = '{gender}', "
                            f"email = '{email}', "
                            f"phoneNumber = '{phone}', "
                            f"subject = '{subject}' "
                            f"where sid = '{sid}'")
                con.commit()
                msg = "Record successfully updated"
                return redirect('/admin/student')
        except:
            con.rollback()
            msg = "error in insert operation"


# ** get student details from student page to filter db and throw to detail page
@students.route('/admin/detail_student', methods=['GET', 'POST'])
def detail_student():
    if request.method == 'POST':
        student_sid = request.form.get("sid", None)
        con = sql.connect("student_ss34.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute(f"select * from students where sid ='{student_sid}'")
        rows = cur.fetchall()
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