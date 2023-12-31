from flask import Flask, render_template
from flask_login import login_required

from route.apiFProduct import apiFD
from route.apiProduct import apiD
from route.auth import auths, login_manager
from route.pos import poss
from route.product import products
from route.student import students
from route.customer import customers
from route.user import users
from route.category import categories
from route.currency import currencies


app = Flask(__name__)


app.secret_key = 'ohboitakeiteasyss'  # Change this!

login_manager.init_app(app)
login_manager.login_view = "auths.login"

app.config['UPLOAD_FOLDER_STUDENT'] = 'static/img/student'
app.config['UPLOAD_FOLDER_PRODUCT'] = 'static/img/product'
app.config['UPLOAD_FOLDER_CUSTOMER'] = 'static/img/customer'
app.config['UPLOAD_FOLDER_USER'] = 'static/img/user'

app.register_blueprint(students)
app.register_blueprint(products)
app.register_blueprint(customers)
app.register_blueprint(currencies)
app.register_blueprint(users)
app.register_blueprint(categories)
app.register_blueprint(apiD)
app.register_blueprint(apiFD)
app.register_blueprint(poss)
app.register_blueprint(auths, url_prefix='/auth')


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


# ** get product detail from product page and throw to product detail page
@app.route('/product/<string:name>/<string:price>/<string:category>/<string:image>')
def product(name, price, category, image):
    return render_template('product_details.html', name=name, category=category, price=price, image=image)


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


if __name__ == '__main__':
    app.run()
