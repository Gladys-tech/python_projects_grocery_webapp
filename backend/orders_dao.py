from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()
    try:
        # Insert order header
        order_query = """
            INSERT INTO orders (customer_name, total, datetime)
            VALUES (%s, %s, %s)
        """
        cursor.execute(order_query, (
            order['customer_name'],
            order['grand_total'],
            datetime.now()
        ))
        order_id = cursor.lastrowid

        # Prepare queries
        order_details_query = """
            INSERT INTO order_details (order_id, product_id, quantity, total_price)
            VALUES (%s, %s, %s, %s)
        """
        update_quantity_query = """
            UPDATE products
            SET quantity = quantity - %s
            WHERE product_id = %s AND quantity >= %s
        """

        # Process items
        for detail in order['order_details']:
            product_id = int(detail['product_id'])
            qty = float(detail['quantity'])
            total_price = float(detail['total_price'])

            # Try to update stock first
            cursor.execute(update_quantity_query, (qty, product_id, qty))
            if cursor.rowcount == 0:
                cursor2 = connection.cursor()
                cursor2.execute("SELECT name, quantity FROM products WHERE product_id = %s", (product_id,))
                row = cursor2.fetchone()
                cursor2.close()

                product_name = row[0] if row else f"Product {product_id}"
                available = row[1] if row else 0

                connection.rollback()
                raise ValueError(f"Not enough stock for '{product_name}'. Available: {available}, requested: {qty}")

            # Insert order detail if stock OK
            cursor.execute(order_details_query, (order_id, product_id, qty, total_price))

        # Commit all
        connection.commit()
        return order_id

    except:
        connection.rollback()
        raise

    finally:
        cursor.close()



def get_order_details(connection, order_id):
    cursor = connection.cursor()

    query = "SELECT * from order_details where order_id = %s"

    query = "SELECT order_details.order_id, order_details.quantity, order_details.total_price, "\
            "products.name, products.price_per_unit FROM order_details LEFT JOIN products on " \
            "order_details.product_id = products.product_id where order_details.order_id = %s"

    data = (order_id, )

    cursor.execute(query, data)

    records = []
    for (order_id, quantity, total_price, product_name, price_per_unit) in cursor:
        records.append({
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'product_name': product_name,
            'price_per_unit': price_per_unit
        })

    cursor.close()

    return records

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)
    response = []
    for (order_id, customer_name, total, dt) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            # 'datetime': dt,
            'datetime': dt.isoformat(), 
        })

    cursor.close()

    # append order details in each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
    # print(get_order_details(connection,4))
    # print(insert_order(connection, {
    #     'customer_name': 'dhaval',
    #     'total': '500',
    #     'datetime': datetime.now(),
    #     'order_details': [
    #         {
    #             'product_id': 1,
    #             'quantity': 2,
    #             'total_price': 50
    #         },
    #         {
    #             'product_id': 3,
    #             'quantity': 1,
    #             'total_price': 30
    #         }
    #     ]
    # }))