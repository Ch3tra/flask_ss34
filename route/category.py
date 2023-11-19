from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required
from config import execute_query

categories = Blueprint('categories', __name__)


# ** filter db and get all data and throw to category list page
@categories.route('/admin/category')
@login_required
def category():
    # Get the page number from the query parameters (default to 1 if not present)
    page = request.args.get('page', 1, type=int)

    # Define the number of records per page
    records_per_page = 3

    # Calculate the offset based on the current page
    offset = (page - 1) * records_per_page

    # Use the helper function to execute the query
    rows = execute_query("SELECT * FROM category LIMIT %s OFFSET %s", (records_per_page, offset))

    # Get total count of records
    total_records_query = "SELECT COUNT(*) FROM category"
    total_records_result = execute_query(total_records_query)

    # Extract the total count based on the structure of the result
    total_records = total_records_result[0][0] if isinstance(total_records_result[0], (list, tuple)) else \
        total_records_result[0]['COUNT(*)']

    total_pages = (total_records // records_per_page) + (total_records % records_per_page > 0)

    return render_template('admin/category/index.html', rows=rows, page=page, total_pages=total_pages)


# ** load to add category page
@categories.route('/admin/add_category')
@login_required
def add_category():
    return render_template('admin/category/add_category.html')


# ** category added to db
@categories.route('/admin/category_added', methods=['POST'])
@login_required
def category_added():
    if request.method == "POST":
        try:
            name = request.form['name']
            description = request.form['description']

            query = "INSERT INTO category (categoryName,categoryDesc) VALUES (%s,%s)"
            params = (name, description)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/category')
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** get category detail from category page filter db and throw to edit page
@categories.route('/admin/edit_category', methods=['GET', 'POST'])
@login_required
def edit_category():
    if request.method == 'POST':
        cid = request.form.get("cid", None)
        page = request.form['page_id']

        # ** cid pass as parameter to prevent sql injection
        query = f"SELECT * FROM category WHERE categoryId = %s"
        rows = execute_query(query, (cid,))

        return render_template('admin/category/edit_category.html', rows=rows, page=page)
    else:
        return redirect('/admin/category')


# ** category edit or update to db
@categories.route('/admin/category_edited', methods=['POST'])
@login_required
def category_edited():
    if request.method == "POST":
        try:
            cid = request.form['cid']
            page_id = request.form['page_id']
            name = request.form['name']
            description = request.form['description']

            query = f"UPDATE category SET " \
                    f"categoryName = %s, " \
                    f"categoryDesc = %s " \
                    f"WHERE categoryId = %s"
            params = (name, description, cid)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/category?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** category delete on db
@categories.route('/admin/delete_category', methods=['POST'])
@login_required
def delete_category():
    if request.method == "POST":
        try:
            cid = request.form['cid']
            page_id = request.form['page_id']

            query = f"DELETE FROM category WHERE categoryId = %s"
            execute_query(query, (cid,), is_insert=True)

            return redirect('/admin/category?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"
