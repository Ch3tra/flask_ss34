from flask import Blueprint, render_template, request, redirect, current_app
from werkzeug.utils import secure_filename
import os
import sqlite3 as sql
from config import execute_query

users = Blueprint('users', __name__)


# ** filter db and get all data and throw to user list page
@users.route('/admin/user')
def user():
    # Get the page number from the query parameters (default to 1 if not present)
    page = request.args.get('page', 1, type=int)

    # Define the number of records per page
    records_per_page = 10

    # Calculate the offset based on the current page
    offset = (page - 1) * records_per_page

    # Use the helper function to execute the query
    rows = execute_query("SELECT * FROM users LIMIT ? OFFSET ?", (records_per_page, offset))

    # Calculate the total number of pages
    total_records = execute_query("SELECT COUNT(*) FROM users")[0][0]
    total_pages = (total_records // records_per_page) + (total_records % records_per_page > 0)

    return render_template('admin/user/index.html', rows=rows, page=page, total_pages=total_pages)


# ** load to add user page
@users.route('/admin/add_user')
def add_user():
    return render_template('admin/user/add_user.html')


# ** user added to db
@users.route('/admin/user_added', methods=['POST'])
def user_added():
    if request.method == "POST":
        try:
            name = request.form['name']
            status = request.form['status']

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

                # Save the image to the uploads folder, with name.extension as the filename
                filename = secure_filename(f"{name}{extension}")
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER_USER'], filename))

                query = "INSERT INTO users (userName,status, image) VALUES (?,?,?)"
                params = (name, status, filename)
            else:
                query = "INSERT INTO users (userName,status) VALUES (?,?)"
                params = (name, status)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/user')
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** get user detail from user page filter db and throw to edit page
@users.route('/admin/edit_user', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'POST':
        uid = request.form.get("uid", None)
        page = request.form['page_id']

        # ** cid pass as parameter to prevent sql injection
        query = f"SELECT * FROM users WHERE userId = ?"
        rows = execute_query(query, (uid,))

        return render_template('admin/user/edit_user.html', rows=rows, page=page)
    else:
        return redirect('/admin/user')


# ** user edit or update to db
@users.route('/admin/user_edited', methods=['POST'])
def user_edited():
    if request.method == "POST":
        try:
            uid = request.form['uid']
            page_id = request.form['page_id']
            name = request.form['name']
            status = request.form['status']

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
                old_image_query = "SELECT image FROM users WHERE userId = ?"
                old_image_filename = execute_query(old_image_query, (uid,), is_insert=False)[0]['image']

                # Delete the old image file
                if old_image_filename:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER_USER'], old_image_filename)
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)

                # Save the image to the uploads folder, with name.extension as the filename
                filename = secure_filename(f"{name}{extension}")
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER_USER'], filename))

                query = f"UPDATE users SET " \
                        f"userName = ?, " \
                        f"status = ?, " \
                        f"image = ? " \
                        f"WHERE userId = ?"
                params = (name, status, filename, uid)
            else:
                query = f"UPDATE users SET " \
                        f"userName = ?, " \
                        f"status = ? " \
                        f"WHERE userId = ?"
                params = (name, status, uid)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/user?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** user delete on db
@users.route('/admin/delete_user', methods=['POST'])
def delete_user():
    if request.method == "POST":
        try:
            uid = request.form['uid']
            page_id = request.form['page_id']
            image = request.form['image_upload']

            # Delete the old image file if it's not the default image
            if image != 'default_img':
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER_USER'], image)
                if os.path.isfile(image_path):
                    os.remove(image_path)

            query = f"DELETE FROM users WHERE userId = ?"
            execute_query(query, (uid,), is_insert=True)

            return redirect('/admin/user?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"
