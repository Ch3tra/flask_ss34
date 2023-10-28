from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
import sqlite3 as sql
from config import execute_query

students = Blueprint('students', __name__)


# ** filter db and get all data and throw to student list page
@students.route('/admin/student')
@login_required
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
@login_required
def add_student():
    return render_template('admin/student/add_student.html')


# ** student added to db
@students.route('/admin/student_added', methods=['POST'])
@login_required
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

            image = request.files.get('image_upload')

            # check if user input image or not
            if image:
                # Check the file extension
                _, extension = os.path.splitext(image.filename)
                if extension.lower() not in ['.jpg', '.png', '.jfif']:
                    return 'Invalid file type. Only jpg, png, and jfif files are allowed.', 400

                # Check the file size (2MB = 2 * 1024 * 1024 bytes)
                if image.content_length > 2 * 1024 * 1024:
                    return 'File size is too large. The maximum file size is 2MB.', 400

                # Save the image to the uploads folder, with fisrtname_lastname.extension as the filename
                filename = secure_filename(f"{firstname}_{lastname}{extension}")
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER_STUDENT'], filename))

                query = "INSERT INTO students (firstName,lastName,birthday,gender,email,phoneNumber,subject,image) VALUES (?,?,?,?,?,?,?,?)"
                params = (firstname, lastname, birthday, gender, email, phone, subject, filename)
            else:
                query = "INSERT INTO students (firstName,lastName,birthday,gender,email,phoneNumber,subject) VALUES (?,?,?,?,?,?,?)"
                params = (firstname, lastname, birthday, gender, email, phone, subject)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/student')
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** get student detail from student page or detail page to filter db and throw to edit page
@students.route('/admin/edit_student', methods=['GET', 'POST'])
@login_required
def edit_student():
    if request.method == 'POST':
        student_sid = request.form.get("sid", None)
        page = request.form['page_id']

        # ** student_sid pass as parameter to prevent sql injection
        query = f"SELECT * FROM students WHERE sid = ?"
        rows = execute_query(query, (student_sid,))

        return render_template('admin/student/edit_student.html', rows=rows, page=page)
    else:
        return redirect('/admin/student')


# ** Student edit or update to db
@students.route('/admin/student_edited', methods=['POST'])
@login_required
def student_edited():
    if request.method == "POST":
        try:
            sid = request.form['sid']
            page_id = request.form['page_id']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            birthday = request.form['birthday']
            gender = request.form['gender']
            email = request.form['email']
            phone = request.form['phone']
            subject = request.form['subject']

            image = request.files.get('image_upload')

            # check if user input image or not
            if image:
                # Check the file extension
                _, extension = os.path.splitext(image.filename)
                if extension.lower() not in ['.jpg', '.png', '.jfif']:
                    return 'Invalid file type. Only jpg, png, and jfif files are allowed.', 400

                # Check the file size (2MB = 2 * 1024 * 1024 bytes)
                if image.content_length > 2 * 1024 * 1024:
                    return 'File size is too large. The maximum file size is 2MB.', 400

                # Get the old image filename from the database
                old_image_query = "SELECT image FROM students WHERE sid = ?"
                old_image_filename = execute_query(old_image_query, (sid,), is_insert=False)[0]['image']

                # Delete the old image file
                if old_image_filename:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER_STUDENT'], old_image_filename)
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)

                # Save the image to the uploads folder, with fisrtname_lastname.extension as the filename
                filename = secure_filename(f"{firstname}_{lastname}{extension}")
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER_STUDENT'], filename))

                query = f"UPDATE students SET " \
                        f"firstName = ?, " \
                        f"lastName = ?, " \
                        f"birthday = ?, " \
                        f"gender = ?, " \
                        f"email = ?, " \
                        f"phoneNumber = ?, " \
                        f"subject = ?, " \
                        f"image = ? " \
                        f"WHERE sid = ?"
                params = (firstname, lastname, birthday, gender, email, phone, subject, filename, sid)
            else:
                query = f"UPDATE students SET " \
                        f"firstName = ?, " \
                        f"lastName = ?, " \
                        f"birthday = ?, " \
                        f"gender = ?, " \
                        f"email = ?, " \
                        f"phoneNumber = ?, " \
                        f"subject = ? " \
                        f"WHERE sid = ?"
                params = (firstname, lastname, birthday, gender, email, phone, subject, sid)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/student?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** get student details from student page to filter db and throw to detail page
@students.route('/admin/detail_student', methods=['GET', 'POST'])
@login_required
def detail_student():
    if request.method == 'POST':
        student_sid = request.form.get("sid", None)
        page = request.form['page_id']

        # ** student_sid pass as parameter to prevent sql injection
        query = f"SELECT * FROM students WHERE sid = ?"
        rows = execute_query(query, (student_sid,))

        return render_template('admin/student/detail_student.html', rows=rows, page=page)
    else:
        return redirect('/admin/student')


# ** Student delete on db
@students.route('/admin/delete_student', methods=['POST'])
@login_required
def delete_student():
    if request.method == "POST":
        try:
            sid = request.form['sid']
            page_id = request.form['page_id']
            image = request.form['image_upload']

            # Delete the old image file if it's not the default image
            if image != 'default_img':
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER_STUDENT'], image)
                if os.path.isfile(image_path):
                    os.remove(image_path)

            query = f"DELETE FROM students WHERE sid = ?"
            execute_query(query, (sid,), is_insert=True)

            return redirect('/admin/student?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"
