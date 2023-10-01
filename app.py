from flask import Flask, render_template, request
import randomname
import random
from route.student import students

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img/student'

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


app.register_blueprint(students)


if __name__ == '__main__':
    app.run()
