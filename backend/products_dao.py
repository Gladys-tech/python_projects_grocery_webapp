from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()
    query = ("select products.product_id, products.name, products.uom_id, products.price_per_unit, products.buying_price, uom.uom_name from products inner join uom on products.uom_id=uom.uom_id")
    cursor.execute(query)
    response = []
    for (product_id, name, uom_id, price_per_unit, buying_price, uom_name) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_id': uom_id,
            'price_per_unit': price_per_unit,
            'buying_price': buying_price,
            'uom_name': uom_name
        })
    return response


def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = (
        "INSERT INTO products "
        "(name, uom_id, price_per_unit, buying_price) "
        "VALUES (%s, %s, %s, %s)"
    )
    data = (
        product['product_name'],
        product['uom_id'],
        product['price_per_unit'],
        product.get('buying_price', 0)
    )

    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid


def update_product(connection, product):
    cursor = connection.cursor()
    query = ("UPDATE products SET name=%s, uom_id=%s, price_per_unit=%s, buying_price=%s WHERE product_id=%s")
    # data = (product['product_name'], product['uom_id'], product['price_per_unit'], product['buying_price'], product['product_id'])
    data = (
            product['product_name'],
            int(product['uom_id']),             # convert to int
            float(product['price_per_unit']),   # convert to float
            float(product['buying_price']),     # convert to float
            int(product['product_id'])          # convert to int
        )
    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM products where product_id=" + str(product_id))
    cursor.execute(query)
    connection.commit()

    return cursor.lastrowid

if __name__ == '__main__':
    connection = get_sql_connection()
    # print(get_all_products(connection))
    print(insert_new_product(connection, {
        'product_name': 'potatoes',
        'uom_id': '1',
        'price_per_unit': 10,
        'buying_price': 6 
    }))