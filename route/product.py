from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
import sqlite3 as sql
from config import execute_query

products = Blueprint('products', __name__)


# ** filter db and get all data and throw to product list page
@products.route('/admin/product')
@login_required
def product():
    # Get the page number from the query parameters (default to 1 if not present)
    page = request.args.get('page', 1, type=int)

    # Define the number of records per page
    records_per_page = 6

    # Calculate the offset based on the current page
    offset = (page - 1) * records_per_page

    # use inner to get category name from categories table according to category id in products table
    rows = execute_query(
        "SELECT product.*, category.categoryName AS category_name FROM product LEFT JOIN category ON product.categoryId = category.categoryId LIMIT %s OFFSET %s",
        (records_per_page, offset))

    # Get total count of records
    total_records_query = "SELECT COUNT(*) FROM product"
    total_records_result = execute_query(total_records_query)

    # Extract the total count based on the structure of the result
    total_records = total_records_result[0][0] if isinstance(total_records_result[0], (list, tuple)) else \
        total_records_result[0]['COUNT(*)']

    total_pages = (total_records // records_per_page) + (total_records % records_per_page > 0)

    return render_template('admin/product/index.html', rows=rows, page=page, total_pages=total_pages)


# ** load to add products page
@products.route('/admin/add_product')
@login_required
def add_product():
    # fetch category names from the database
    query = "SELECT categoryId, categoryName FROM category"
    categories = execute_query(query)

    return render_template('admin/product/add_product.html', categories=categories)


# ** product added to db
@products.route('/admin/product_added', methods=['POST'])
@login_required
def product_added():
    if request.method == "POST":
        try:
            name = request.form['name']
            description = request.form['description']
            cost = request.form['cost']
            category = request.form['category']

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
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER_PRODUCT'], filename))

                query = "INSERT INTO product (productName,productDesc,productCost,categoryId,image) VALUES (%s,%s,%s,%s,%s)"
                params = (name, description, cost, category, filename)
            else:
                query = "INSERT INTO product (productName,productDesc,productCost,categoryId) VALUES (%s,%s,%s,%s)"
                params = (name, description, cost, category)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/product')
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** get student detail from product page or detail page to filter db and throw to edit page
@products.route('/admin/edit_product', methods=['GET', 'POST'])
@login_required
def edit_product():
    if request.method == 'POST':
        pid = request.form.get("pid", None)
        page = request.form['page_id']

        # Fetch all categories
        all_categories = execute_query("SELECT * FROM category")

        # ** student_sid pass as parameter to prevent sql injection
        query = f"SELECT product.*, category.categoryName AS category_name FROM product LEFT JOIN category ON product.categoryId = category.categoryId WHERE product.productId = %s"
        rows = execute_query(query, (pid,))

        return render_template('admin/product/edit_product.html', rows=rows, page=page, categories=all_categories)
    else:
        return redirect('/admin/product')


# ** Student edit or update to db
@products.route('/admin/product_edited', methods=['POST'])
@login_required
def product_edited():
    if request.method == "POST":
        try:
            pid = request.form['pid']
            page_id = request.form['page_id']
            name = request.form['name']
            description = request.form['description']
            cost = request.form['cost']
            category = request.form['category']

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
                old_image_query = "SELECT image FROM product WHERE productId = %s"
                old_image_filename = execute_query(old_image_query, (pid,), is_insert=False)[0]['image']

                # Delete the old image file
                if old_image_filename:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER_PRODUCT'], old_image_filename)
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)

                # Save the image to the upload folder, with name.extension as the filename
                filename = secure_filename(f"{name}{extension}")
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER_PRODUCT'], filename))

                query = f"UPDATE product SET " \
                        f"categoryId = %s, " \
                        f"productName = %s, " \
                        f"productDesc = %s, " \
                        f"productCost = %s, " \
                        f"image = %s " \
                        f"WHERE productId = %s"
                params = (category, name, description, cost, filename, pid)
            else:
                query = f"UPDATE product SET " \
                        f"categoryId = %s, " \
                        f"productName = %s, " \
                        f"productDesc = %s, " \
                        f"productCost = %s " \
                        f"WHERE productId = %s"
                params = (category, name, description, cost, pid)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/product?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** get product details from student page to filter db and throw to detail page
@products.route('/admin/detail_product', methods=['GET', 'POST'])
@login_required
def detail_product():
    if request.method == 'POST':
        pid = request.form.get("pid", None)
        page = request.form['page_id']

        # ** student_sid pass as parameter to prevent sql injection
        query = f"SELECT product.*, category.categoryName AS category_name FROM product LEFT JOIN category ON product.categoryId = category.categoryId WHERE product.productId = %s"
        rows = execute_query(query, (pid,))

        return render_template('admin/product/detail_product.html', rows=rows, page=page)
    else:
        return redirect('/admin/product')


# ** product delete on db
@products.route('/admin/delete_product', methods=['POST'])
@login_required
def delete_product():
    if request.method == "POST":
        try:
            pid = request.form['pid']
            page_id = request.form['page_id']
            image = request.form['image_upload']

            # Delete the old image file if it's not the default image
            if image != 'default_img':
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER_PRODUCT'], image)
                if os.path.isfile(image_path):
                    os.remove(image_path)

            query = f"DELETE FROM product WHERE productId = %s"
            execute_query(query, (pid,), is_insert=True)

            return redirect('/admin/product?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"
