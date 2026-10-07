import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), "lunch.db")


def add_order(name, food_item, quantity, price):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    total = quantity * price

    cursor.execute("""
        INSERT INTO orders (name, food_item, quantity, price, total)
        VALUES (?, ?, ?, ?, ?)
    """, (name, food_item, quantity, price, total))

    connection.commit()
    connection.close()


def get_orders():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    connection.close()

    return orders


def delete_order(order_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM orders WHERE id = ?",
        (order_id,)
    )

    connection.commit()
    connection.close()


def get_total():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT SUM(total) FROM orders")
    result = cursor.fetchone()

    connection.close()

    return result[0] if result[0] is not None else 0