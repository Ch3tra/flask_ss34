from flask import Blueprint
from config import execute_query

apiD = Blueprint('apiD', __name__)

@apiD.route('/getAllProduct')
def getAllProduct():
    query = "SELECT productId,productName,discount,productPrice,image FROM product"
    products = execute_query(query)

    json_string = []
    for product in products:
        json_string.append(
            {
                'id': product['productId'],
                'name': product['productName'],
                'discount': product['discount'],
                'price': product['productPrice'],
                'image': product['image'],
            }
        )
    return json_string



