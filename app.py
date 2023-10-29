from flask import Flask, render_template, request, redirect, url_for
import randomname
import random
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from config import execute_query
from route.category import categories
from route.product import products
from route.student import students
from route.customer import customers
from route.user import users
from route.currency import currencies

app = Flask(__name__)

app.secret_key = 'admin'  # Change this!

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.config['UPLOAD_FOLDER_STUDENT'] = 'static/img/student'
app.config['UPLOAD_FOLDER_PRODUCT'] = 'static/img/product'
app.config['UPLOAD_FOLDER_CUSTOMER'] = 'static/img/customer'
app.config['UPLOAD_FOLDER_USER'] = 'static/img/user'

app.register_blueprint(students)
app.register_blueprint(products)
app.register_blueprint(categories)
app.register_blueprint(customers)
app.register_blueprint(users)
app.register_blueprint(currencies)


# ** create database
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
    return render_template('product_details.html', name=name, category=category, price_big=price_big,
                           price_small=price_small, image=image)


# ** handling 404
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error/404.html'), 404


# ** handling 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500


# ** admin page or dashboard
@app.route('/admin')
@login_required
def admin():
    return render_template('admin/index.html')


# ** register new admin user
@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Hash the password
        password_hash = generate_password_hash(password)

        # Insert the new user into the database
        sql = "INSERT INTO credential (username, password_hash) VALUES (?, ?)"
        execute_query(sql, (username, password_hash), "student_ss34.db", True)

        return redirect(url_for('admin'))
    return render_template('register.html')


class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def get(user_id):
        query = f"SELECT * FROM credential WHERE userId = ?"
        user_data = execute_query(query, (user_id,))
        if user_data:
            return User(user_data[0]['userId'], user_data[0]['username'], user_data[0]['password_hash'])

    def get_by_username(username):
        query = f"SELECT * FROM credential WHERE username = ?"
        user_data = execute_query(query, (username,))
        if user_data:
            return User(user_data[0]['userId'], user_data[0]['username'], user_data[0]['password_hash'])

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('protected'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')


@app.route('/protected')
@login_required
def protected():
    return render_template('admin/index.html')


if __name__ == '__main__':
    app.run()
