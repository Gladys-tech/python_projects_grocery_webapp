from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from sql_connection import get_sql_connection
from flask_cors import CORS
import mysql.connector
import json


import products_dao
import orders_dao
import uom_dao
import expenses_dao
import profits_dao
import reports_dao

app = Flask(__name__)
bcrypt = Bcrypt(app)
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
    try:
        request_payload = json.loads(request.form.get('data', '{}'))
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid payload'}), 400

    try:
        order_id = orders_dao.insert_order(connection, request_payload)
        return jsonify({'success': True, 'order_id': order_id})
    except ValueError as ve:
        # Known error from stock check (friendly message)
        return jsonify({'success': False, 'error': str(ve)}), 400
    except Exception as e:
        # Log full exception server-side for debugging
        print("Unexpected error inserting order:", e)
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


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
    try:
        request_payload = request.get_json()
        print("Received payload:", request_payload)
        # then parse it
        if 'data' in request_payload:
            request_payload = json.loads(request_payload['data'])
        print("Parsed payload:", request_payload)
        updated_id = products_dao.update_product(connection, request_payload)
        response = jsonify({"status": "success", "updated_id": updated_id})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500


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

@app.route('/getProfitSummary', methods=['GET'])
def get_profit_summary():
    filter_option = request.args.get('filter', 'daily')  # default to daily
    summary = profits_dao.calculate_profit(connection, filter_option)
    response = jsonify(summary)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getSalesReport', methods=['GET'])
def get_sales_report_route():
    filter_option = request.args.get('filter', 'daily')
    data = reports_dao.get_sales_report(connection, filter_option)
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# @app.route('/getInventoryReport', methods=['GET'])
# def inventory_report():
#     data = reports_dao.get_inventory_report(connection)
#     response = jsonify(data)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# @app.route('/getCreditReport', methods=['GET'])
# def credit_report():
#     data = reports_dao.get_credit_report(connection)
#     response = jsonify(data)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# @app.route('/getStaffReport', methods=['GET'])
# def staff_report():
#     data = reports_dao.get_staff_activity_report(connection)
#     response = jsonify(data)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role']  # 'admin' or 'cashier'

    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (username, hashed, role))
        connection.commit()
        return jsonify({'success': True})
    # except:
    #     return jsonify({'success': False, 'error': 'Username already exists'})
    except mysql.connector.IntegrityError:
        return jsonify({'success': False, 'error': 'Username already exists'})



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        return jsonify({'success': True, 'username': user['username'], 'role': user['role']})
    else:
        return jsonify({'success': False, 'error': 'Invalid credentials'})


if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(port=5000)

