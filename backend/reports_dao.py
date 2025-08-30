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
