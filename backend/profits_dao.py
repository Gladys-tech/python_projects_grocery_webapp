# # profit_dao.py

# def calculate_profit(connection):
#     cursor = connection.cursor(dictionary=True)

#     # Get total revenue from orders
#     cursor.execute("SELECT SUM(total) AS total_revenue FROM orders")
#     revenue_result = cursor.fetchone()
#     total_revenue = revenue_result['total_revenue'] if revenue_result['total_revenue'] else 0

#     # Get total expenses from expenses table
#     cursor.execute("SELECT SUM(amount) AS total_expenses FROM expenses")
#     expenses_result = cursor.fetchone()
#     total_expenses = expenses_result['total_expenses'] if expenses_result['total_expenses'] else 0

#     # Calculate profit
#     profit = total_revenue - total_expenses

#     cursor.close()

#     return {
#         'total_revenue': total_revenue,
#         'total_expenses': total_expenses,
#         'profit': profit
#     }

from datetime import datetime, timedelta

def calculate_profit(connection, filter_option='daily'):
    cursor = connection.cursor(dictionary=True)

    # Determine date condition
    if filter_option == 'daily':
        condition = "DATE(datetime) = CURDATE()"
        expense_condition = "DATE(date) = CURDATE()"
    elif filter_option == 'weekly':
        condition = "YEARWEEK(datetime, 1) = YEARWEEK(CURDATE(), 1)"
        expense_condition = "YEARWEEK(date, 1) = YEARWEEK(CURDATE(), 1)"
    elif filter_option == 'monthly':
        condition = "MONTH(datetime) = MONTH(CURDATE()) AND YEAR(datetime) = YEAR(CURDATE())"
        expense_condition = "MONTH(date) = MONTH(CURDATE()) AND YEAR(date) = YEAR(CURDATE())"
    elif filter_option == 'yearly':
        condition = "YEAR(datetime) = YEAR(CURDATE())"
        expense_condition = "YEAR(date) = YEAR(CURDATE())"
    else:
        condition = "1"  # no filter
        expense_condition = "1"

    # Get revenue
    cursor.execute(f"SELECT SUM(total) AS total_revenue FROM orders WHERE {condition}")
    revenue_result = cursor.fetchone()
    total_revenue = revenue_result['total_revenue'] or 0

    # Get expenses
    cursor.execute(f"SELECT SUM(amount) AS total_expenses FROM expenses WHERE {expense_condition}")
    expenses_result = cursor.fetchone()
    total_expenses = expenses_result['total_expenses'] or 0

     # Buying Price Total (COGS)
    cursor.execute(f"""
        SELECT SUM(oi.quantity * p.buying_price) AS total_buying_price
        FROM orders o
        JOIN order_details oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE {condition}
    """)
    buying_result = cursor.fetchone()
    total_buying_price = buying_result['total_buying_price'] or 0

    # profit = total_revenue - total_expenses
    # Profit = Revenue - (Expenses + Buying Cost)
    profit = total_revenue - total_expenses - total_buying_price

    cursor.close()

    return {
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'total_buying_price': total_buying_price,
        'profit': profit
    }