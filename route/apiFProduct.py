from flask import Blueprint, request, jsonify
from config import execute_query

apiFD = Blueprint('apiFD', __name__)


@apiFD.route('/getAllFProduct')
def getAllFProduct():
    filter_category = request.args.get('filter_category', default='all', type=str)

    query = """
        SELECT p.id, p.name, p.price, c.name AS category
        FROM pproduct p
        JOIN pcategory c ON p.cid = c.id
    """

    if filter_category != 'all':
        query += " WHERE c.name = %s"
        products = execute_query(query, (filter_category,))
    else:
        products = execute_query(query)

    json_data = []
    json_data_cate = []

    for product in products:
        json_data.append({
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'category': product['category']
        })

    return jsonify(products=json_data)
