from flask import Blueprint
from config import execute_query

apiD = Blueprint('apiD', __name__)

@apiD.route('/getAllProduct')
def getAllProduct():
    query = "SELECT * FROM pproduct"
    products = execute_query(query)

    json_string = []
    for product in products:
        json_string.append(
            {
                'id': product['id'],
                'name': product['name'],
                'discount': product['discount'],
                'price': product['price'],
                'image': product['image'],
            }
        )
    return json_string



