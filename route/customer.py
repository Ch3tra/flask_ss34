from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
from config import execute_query

customers = Blueprint('customers', __name__)


# ** filter db and get all data and throw to customer list page
@customers.route('/admin/customer')
@login_required
def customer():
    # Get the page number from the query parameters (default to 1 if not present)
    page = request.args.get('page', 1, type=int)

    # Define the number of records per page
    records_per_page = 10

    # Calculate the offset based on the current page
    offset = (page - 1) * records_per_page

    # Use the helper function to execute the query
    rows = execute_query("SELECT * FROM customer LIMIT %s OFFSET %s", (records_per_page, offset))

    # Get total count of records
    total_records_query = "SELECT COUNT(*) FROM customer"
    total_records_result = execute_query(total_records_query)

    # Extract the total count based on the structure of the result
    total_records = total_records_result[0][0] if isinstance(total_records_result[0], (list, tuple)) else \
        total_records_result[0]['COUNT(*)']

    total_pages = (total_records // records_per_page) + (total_records % records_per_page > 0)

    return render_template('admin/customer/index.html', rows=rows, page=page, total_pages=total_pages)


# ** load to add customer page
@customers.route('/admin/add_customer')
@login_required
def add_customer():
    return render_template('admin/customer/add_customer.html')


# ** customer added to db
@customers.route('/admin/customer_added', methods=['POST'])
@login_required
def customer_added():
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
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER_CUSTOMER'], filename))

                query = "INSERT INTO customer (customerName,status, image) VALUES (%s,%s,%s)"
                params = (name, status, filename)
            else:
                query = "INSERT INTO customer (customerName,status) VALUES (%s,%s)"
                params = (name, status)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/customer')
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** get customer detail from customer page filter db and throw to edit page
@customers.route('/admin/edit_customer', methods=['GET', 'POST'])
@login_required
def edit_customer():
    if request.method == 'POST':
        cid = request.form.get("cid", None)
        page = request.form['page_id']

        # ** cid pass as parameter to prevent sql injection
        query = f"SELECT * FROM customer WHERE customerId = %s"
        rows = execute_query(query, (cid,))

        return render_template('admin/customer/edit_customer.html', rows=rows, page=page)
    else:
        return redirect('/admin/customer')


# ** customer edit or update to db
@customers.route('/admin/customer_edited', methods=['POST'])
@login_required
def customer_edited():
    if request.method == "POST":
        try:
            cid = request.form['cid']
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
                old_image_query = "SELECT image FROM customer WHERE customerId = %s"
                old_image_filename = execute_query(old_image_query, (cid,), is_insert=False)[0]['image']

                # Delete the old image file
                if old_image_filename:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER_CUSTOMER'], old_image_filename)
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)

                # Save the image to the uploads folder, with name.extension as the filename
                filename = secure_filename(f"{name}{extension}")
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER_CUSTOMER'], filename))

                query = f"UPDATE customer SET " \
                        f"customerName = %s, " \
                        f"status = %s, " \
                        f"image = %s " \
                        f"WHERE customerId = %s"
                params = (name, status, filename, cid)
            else:
                query = f"UPDATE customer SET " \
                        f"customerName = %s, " \
                        f"status = %s " \
                        f"WHERE customerId = %s"
                params = (name, status, cid)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/customer?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** customer delete on db
@customers.route('/admin/delete_customer', methods=['POST'])
@login_required
def delete_customer():
    if request.method == "POST":
        try:
            cid = request.form['cid']
            page_id = request.form['page_id']
            image = request.form['image_upload']

            # Delete the old image file if it's not the default image
            if image != 'default_img':
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER_CUSTOMER'], image)
                if os.path.isfile(image_path):
                    os.remove(image_path)

            query = f"DELETE FROM customer WHERE customerId = %s"
            execute_query(query, (cid,), is_insert=True)

            return redirect('/admin/customer?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"

