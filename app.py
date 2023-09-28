from flask import Flask, render_template, request, redirect
import randomname
import random
import sqlite3 as sql

app = Flask(__name__)

# ** create database
# conn = sql.connect('flask_ss34.db')
# conn.execute('CREATE TABLE students (name TEXT, gender TEXT, email TEXT, address TEXT)')
# conn.close()

# conn = sql.connect('student_ss34.db')
# conn.execute('''
# CREATE TABLE students (
#     sid INTEGER PRIMARY KEY AUTOINCREMENT,
#     firstName TEXT NOT NULL,
#     lastName TEXT NOT NULL,
#     birthday TEXT NOT NULL,
#     gender TEXT NOT NULL,
#     email TEXT NOT NULL,
#     phoneNumber TEXT NOT NULL,
#     subject TEXT NOT NULL
# )
# ''')
# conn.close()


@app.route('/')
@app.route('/home')
def home():
    filter_category = request.args.get('filter_category', default="all", type=str)
    products = []
    categories = [
        {
            'id': 1,
            'name': 'gaming',
        },
        {
            'id': 2,
            'name': 'professional',
        },
        {
            'id': 3,
            'name': 'office',
        },
        {
            'id': 4,
            'name': 'old-School',
        },
        {
            'id': 5,
            'name': 'weird-One',
        }
    ]

    for item in range(20):
        category = random.choice(categories)
        products.append({
            'id': 1,
            'name': randomname.get_name(noun=('gaming', 'design')),
            'price_big': 79,
            'price_small': 99,
            'category': category['name'],
        })

    product_filter = []
    if filter_category == 'all' or filter_category == '':
        product_filter = products
    else:
        for item in products:
            if item['category'] == filter_category:
                product_filter.append(item)

    return render_template('index.html', products=product_filter, category=categories, filter_category=filter_category)


# ** get product detail from product page and throw to product detail page
@app.route('/product/<string:name>/<string:price_big>/<string:price_small>/<string:category>/<string:image>')
def product(name, price_big, price_small, category, image):
    return render_template('product_details.html', name=name, category=category, price_big=price_big, price_small=price_small, image=image)


# ** admin page or dashboard
@app.route('/admin')
def admin():
    return render_template('admin/index.html')


# ** filter db and get all data and throw to student list page
@app.route('/admin/student')
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
@app.route('/admin/add_student')
def add_student():
    return render_template('admin/student/add_student.html')


# ** student added to db
@app.route('/admin/student_added', methods=['POST'])
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
@app.route('/admin/edit_student', methods=['GET', 'POST'])
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
@app.route('/admin/student_edited', methods=['POST'])
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
@app.route('/admin/detail_student', methods=['GET', 'POST'])
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
@app.route('/admin/delete_student', methods=['POST'])
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


if __name__ == '__main__':
    app.run()
