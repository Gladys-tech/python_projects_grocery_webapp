from sql_connection import get_sql_connection

def get_all_expenses(connection):
    cursor = connection.cursor()
    query = "SELECT expense_id, category, description, amount, date FROM expenses ORDER BY date DESC"
    cursor.execute(query)
    response = []
    for (expense_id, category, description, amount, date) in cursor:
        response.append({
            'expense_id': expense_id,
            'category': category,
            'description': description,
            'amount': amount,
            'date': date.strftime('%Y-%m-%d %H:%M:%S')  # convert datetime to string
            # 'date': date,
        })
    return response


def insert_new_expense(connection, expense):
    cursor = connection.cursor()
    query = (
        "INSERT INTO expenses "
        "(category, description, amount, date) "
        "VALUES (%s, %s, %s, NOW())"
    )
    data = (
        expense['category'],
        expense['description'],
        float(expense['amount'])  # ensure it's a float
    )

    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid


def delete_expense(connection, expense_id):
    cursor = connection.cursor()
    query = "DELETE FROM expenses WHERE expense_id = %s"
    cursor.execute(query, (expense_id,))
    connection.commit()

    return cursor.rowcount


if __name__ == '__main__':
    connection = get_sql_connection()

    # Insert sample
    print(insert_new_expense(connection, {
        'category': 'Utilities',
        'description': 'Electricity bill for July',
        'amount': 55000
    }))

    # View all
    for expense in get_all_expenses(connection):
        print(expense)

    # Delete example
    # print(delete_expense(connection, 1))
