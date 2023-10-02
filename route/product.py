from flask import Blueprint, render_template, request, redirect, current_app
from werkzeug.utils import secure_filename
import os
import sqlite3 as sql
from config import execute_query

products = Blueprint('products', __name__)


# ** filter db and get all data and throw to product list page
@products.route('/admin/product')
def product():
    # Get the page number from the query parameters (default to 1 if not present)
    page = request.args.get('page', 1, type=int)

    # Define the number of records per page
    records_per_page = 10

    # Calculate the offset based on the current page
    offset = (page - 1) * records_per_page

    # use inner to get category name from categories table according to category id in products table
    rows = execute_query(
        "SELECT products.*, categories.categoryName AS category_name FROM products INNER JOIN categories ON products.categoryId = categories.categoryId LIMIT ? OFFSET ?",
        (records_per_page, offset))

    # Calculate the total number of pages
    total_records = execute_query("SELECT COUNT(*) FROM products")[0][0]
    total_pages = (total_records // records_per_page) + (total_records % records_per_page > 0)

    return render_template('admin/product/index.html', rows=rows, page=page, total_pages=total_pages)


# ** load to add products page
@products.route('/admin/add_product')
def add_product():
    # fetch category names from the database
    query = "SELECT categoryId, categoryName FROM categories"
    categories = execute_query(query)

    return render_template('admin/product/add_product.html', categories=categories)


# ** product added to db
@products.route('/admin/product_added', methods=['POST'])
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

                query = "INSERT INTO products (productName,productDesc,productCost,categoryId,image) VALUES (?,?,?,?,?)"
                params = (name, description, cost, category, filename)
            else:
                query = "INSERT INTO products (productName,productDesc,productCost,categoryId) VALUES (?,?,?,?)"
                params = (name, description, cost, category)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/product')
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** product delete on db
@products.route('/admin/delete_product', methods=['POST'])
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

            query = f"DELETE FROM products WHERE productId = ?"
            execute_query(query, (pid,), is_insert=True)

            return redirect('/admin/product?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"
