def get_sales_report(connection, filter_option='daily'):
    cursor = connection.cursor(dictionary=True)

    # Conditions based on filter option
    if filter_option == 'daily':
        condition = "DATE(o.datetime) = CURDATE()"
        expense_condition = "DATE(date) = CURDATE()"
    elif filter_option == 'weekly':
        condition = "YEARWEEK(o.datetime, 1) = YEARWEEK(CURDATE(), 1)"
        expense_condition = "YEARWEEK(date, 1) = YEARWEEK(CURDATE(), 1)"
    elif filter_option == 'monthly':
        condition = "MONTH(o.datetime) = MONTH(CURDATE()) AND YEAR(o.datetime) = YEAR(CURDATE())"
        expense_condition = "MONTH(date) = MONTH(CURDATE()) AND YEAR(date) = YEAR(CURDATE())"
    elif filter_option == 'yearly':
        condition = "YEAR(o.datetime) = YEAR(CURDATE())"
        expense_condition = "YEAR(date) = YEAR(CURDATE())"
    else:
        condition = "1"
        expense_condition = "1"

    # Total Sales
    cursor.execute(f"""
        SELECT SUM(total) AS total_sales
        FROM orders o
        WHERE {condition}
    """)
    total_sales = cursor.fetchone()['total_sales'] or 0

    # Total Cost (based on buying price)
    cursor.execute(f"""
        SELECT SUM(p.buying_price * od.quantity) AS total_cost
        FROM order_details od
        JOIN products p ON od.product_id = p.product_id
        JOIN orders o ON od.order_id = o.order_id
        WHERE {condition}
    """)
    total_cost = cursor.fetchone()['total_cost'] or 0

     #Get expenses
    cursor.execute(f"SELECT SUM(amount) AS total_expenses FROM expenses WHERE {expense_condition}")
    expenses_result = cursor.fetchone()
    total_expenses = expenses_result['total_expenses'] or 0

    # Profit = Revenue - (Cost + Expenses)
    profit = total_sales - (total_cost + total_expenses)

    cursor.close()
    return {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'total_cost': total_cost,
        'total_profit': profit
    }

# def get_inventory_report(connection):
#     cursor = connection.cursor(dictionary=True)

#     # Fast Moving: sold frequently (e.g., > 10 times)
#     cursor.execute("""
#         SELECT p.name, SUM(od.quantity) AS total_sold
#         FROM order_details od
#         JOIN products p ON od.product_id = p.product_id
#         GROUP BY od.product_id
#         ORDER BY total_sold DESC
#     """)
#     products = cursor.fetchall()

#     fast_movers = [p['name'] for p in products if p['total_sold'] >= 10]
#     slow_movers = [p['name'] for p in products if p['total_sold'] < 10]

#     # Out of Stock
#     cursor.execute("SELECT name FROM products WHERE quantity_in_stock = 0")
#     out_of_stock = [row['name'] for row in cursor.fetchall()]

#     cursor.close()
#     return {
#         'fast_moving': fast_movers,
#         'slow_moving': slow_movers,
#         'out_of_stock': out_of_stock
#     }

# def get_credit_report(connection):
#     cursor = connection.cursor(dictionary=True)

#     cursor.execute("""
#         SELECT customer_name, amount_owed, follow_up_date
#         FROM credits
#     """)
#     data = cursor.fetchall()

#     total_owed = sum(d['amount_owed'] for d in data)

#     cursor.close()
#     return {
#         'credits': data,
#         'total_owed': total_owed
#     }


# def get_staff_activity_report(connection):
#     cursor = connection.cursor(dictionary=True)

#     cursor.execute("""
#         SELECT cashier_name, COUNT(*) AS sales_count, SUM(total) AS total_sales
#         FROM orders
#         GROUP BY cashier_name
#     """)
#     data = cursor.fetchall()

#     # Optional: detect sales below zero (errors)
#     cursor.execute("SELECT COUNT(*) AS error_count FROM orders WHERE total < 0")
#     error_count = cursor.fetchone()['error_count']

#     cursor.close()
#     return {
#         'staff': data,
#         'errors': error_count
#     }
