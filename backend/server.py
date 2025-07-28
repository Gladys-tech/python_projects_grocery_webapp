from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
from flask_cors import CORS
import mysql.connector
import json

import products_dao
import orders_dao
import uom_dao
import expenses_dao
import profits_dao

app = Flask(__name__)
CORS(app)

connection = get_sql_connection()

@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getProducts', methods=['GET'])
def get_products():
    response = products_dao.get_all_products(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getOrderDetails/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    # response = orders_dao.get_order_details(connection, order_id)
    # response = jsonify(response)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    results = orders_dao.get_order_details(connection, order_id)
    
    if results:
        response = jsonify(results)
    else:
        response = jsonify({'error': 'No order details found for order_id: {}'.format(order_id)}), 404
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/editProduct', methods=['PUT'])
def edit_product():
    # request_payload = json.loads(request.form['data'])
    request_payload = request.get_json()
    updated_id = products_dao.update_product(connection, request_payload)
    response = jsonify({
        'updated_id': updated_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/addExpense', methods=['POST'])
def add_expense():
    request_payload = request.get_json()
    expense_id = expenses_dao.insert_new_expense(connection, request_payload)
    response = jsonify({
        'expense_id': expense_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getExpenses', methods=['GET'])
def get_expenses():
    expenses = expenses_dao.get_all_expenses(connection)
    response = jsonify(expenses)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# @app.route('/getProfitSummary', methods=['GET'])
# def get_profit_summary():
#     summary = profits_dao.calculate_profit(connection)
#     response = jsonify(summary)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response
@app.route('/getProfitSummary', methods=['GET'])
def get_profit_summary():
    filter_option = request.args.get('filter', 'daily')  # default to daily
    summary = profits_dao.calculate_profit(connection, filter_option)
    response = jsonify(summary)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(port=5000)

