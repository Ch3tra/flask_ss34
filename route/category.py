from flask import Blueprint, render_template, request, redirect, current_app
from werkzeug.utils import secure_filename
import os
import sqlite3 as sql
from config import execute_query

categories = Blueprint('categories', __name__)


# ** filter db and get all data and throw to category list page
@categories.route('/admin/category')
def category():
    # Get the page number from the query parameters (default to 1 if not present)
    page = request.args.get('page', 1, type=int)

    # Define the number of records per page
    records_per_page = 10

    # Calculate the offset based on the current page
    offset = (page - 1) * records_per_page

    # Use the helper function to execute the query
    rows = execute_query("SELECT * FROM categories LIMIT ? OFFSET ?", (records_per_page, offset))

    # Calculate the total number of pages
    total_records = execute_query("SELECT COUNT(*) FROM categories")[0][0]
    total_pages = (total_records // records_per_page) + (total_records % records_per_page > 0)

    return render_template('admin/category/index.html', rows=rows, page=page, total_pages=total_pages)


# ** load to add category page
@categories.route('/admin/add_category')
def add_category():
    return render_template('admin/category/add_category.html')


# ** category added to db
@categories.route('/admin/category_added', methods=['POST'])
def category_added():
    if request.method == "POST":
        try:
            name = request.form['name']
            description = request.form['description']

            query = "INSERT INTO categories (categoryName,categoryDesc) VALUES (?,?)"
            params = (name, description)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/category')
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** get category detail from student page or detail page to filter db and throw to edit page
@categories.route('/admin/edit_category', methods=['GET', 'POST'])
def edit_category():
    if request.method == 'POST':
        cid = request.form.get("cid", None)
        page = request.form['page_id']

        # ** cid pass as parameter to prevent sql injection
        query = f"SELECT * FROM categories WHERE categoryId = ?"
        rows = execute_query(query, (cid,))

        return render_template('admin/category/edit_category.html', rows=rows, page=page)
    else:
        return redirect('/admin/category')


# ** category edit or update to db
@categories.route('/admin/category_edited', methods=['POST'])
def category_edited():
    if request.method == "POST":
        try:
            cid = request.form['cid']
            page_id = request.form['page_id']
            name = request.form['name']
            description = request.form['description']

            query = f"UPDATE categories SET " \
                    f"categoryName = ?, " \
                    f"categoryDesc = ? " \
                    f"WHERE categoryId = ?"
            params = (name, description, cid)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/category?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** category delete on db
@categories.route('/admin/delete_category', methods=['POST'])
def delete_category():
    if request.method == "POST":
        try:
            cid = request.form['cid']
            page_id = request.form['page_id']

            query = f"DELETE FROM categories WHERE categoryId = ?"
            execute_query(query, (cid,), is_insert=True)

            return redirect('/admin/category?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"
