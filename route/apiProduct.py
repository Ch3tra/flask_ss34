from flask import Blueprint
from database import connection, text

apiD = Blueprint('apiD', __name__)


@apiD.route('/getAllProduct')
def getAllProduct():
    products = connection.execute(text('select * from pproduct'))
    connection.commit()

    json_string = []
    for product in products:
        json_string.append(
            {
                'id': product.id,
                'name': product.name,
                'discount': product.discount,
                'price': product.price,
                'image': product.image,
            }
        )
    return json_string


