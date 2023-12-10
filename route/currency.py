from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required
from config import execute_query

currencies = Blueprint('currencies', __name__)


# ** filter db and get all data and throw to currency list page
@currencies.route('/admin/currency')
@login_required
def currency():
    # Get the page number from the query parameters (default to 1 if not present)
    page = request.args.get('page', 1, type=int)

    # Define the number of records per page
    records_per_page = 6

    # Calculate the offset based on the current page
    offset = (page - 1) * records_per_page

    # Use the helper function to execute the query
    rows = execute_query("SELECT * FROM currency LIMIT %s OFFSET %s", (records_per_page, offset))

    # Get total count of records
    total_records_query = "SELECT COUNT(*) FROM currency"
    total_records_result = execute_query(total_records_query)

    # Extract the total count based on the structure of the result
    total_records = total_records_result[0][0] if isinstance(total_records_result[0], (list, tuple)) else \
        total_records_result[0]['COUNT(*)']

    total_pages = (total_records // records_per_page) + (total_records % records_per_page > 0)

    return render_template('admin/currency/index.html', rows=rows, page=page, total_pages=total_pages)


# ** load to add currency page
@currencies.route('/admin/add_currency')
@login_required
def add_currency():
    return render_template('admin/currency/add_currency.html')


# ** currency added to db
@currencies.route('/admin/currency_added', methods=['POST'])
@login_required
def currency_added():
    if request.method == "POST":
        try:
            name = request.form['name']
            code = request.form['code']
            symbol = request.form['symbol']
            rate = request.form['rate']

            query = "INSERT INTO currency (code,currencyName,currencySymbol,currencyRate) VALUES (%s,%s,%s,%s)"
            params = (code, name, symbol, rate)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/currency')
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** get currency detail from currency page filter db and throw to edit page
@currencies.route('/admin/edit_currency', methods=['GET', 'POST'])
@login_required
def edit_currency():
    if request.method == 'POST':
        cid = request.form.get("cid", None)
        page = request.form['page_id']

        # ** cid pass as parameter to prevent sql injection
        query = f"SELECT * FROM currency WHERE currencyId = %s"
        rows = execute_query(query, (cid,))

        return render_template('admin/currency/edit_currency.html', rows=rows, page=page)
    else:
        return redirect('/admin/currency')


# ** currency edit or update to db
@currencies.route('/admin/currency_edited', methods=['POST'])
@login_required
def currency_edited():
    if request.method == "POST":
        try:
            cid = request.form['cid']
            page_id = request.form['page_id']
            name = request.form['name']
            code = request.form['code']
            symbol = request.form['symbol']
            rate = request.form['rate']
            is_default = request.form['default']

            query = f"UPDATE currency SET " \
                    f"currencyName = %s, " \
                    f"code = %s, "\
                    f"currencySymbol = %s, " \
                    f"currencyRate = %s, " \
                    f"is_default = %s " \
                    f"WHERE currencyId = %s"
            params = (name, code, symbol, rate, is_default, cid)

            execute_query(query, params, is_insert=True)

            return redirect('/admin/currency?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"


# ** currency delete on db
@currencies.route('/admin/delete_currency', methods=['POST'])
@login_required
def delete_currency():
    if request.method == "POST":
        try:
            cid = request.form['cid']
            page_id = request.form['page_id']

            query = f"DELETE FROM currency WHERE currencyId = %s"
            execute_query(query, (cid,), is_insert=True)

            return redirect('/admin/currency?page=' + page_id)
        except Exception as e:
            return f"An error occurred: {str(e)}"
