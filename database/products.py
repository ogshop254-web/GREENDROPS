"""
Product-related database functions.
"""

from database.db import get_connection


def add_product(name: str, price: float, stock: int = 0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
        (name, price, stock),
    )
    conn.commit()
    conn.close()


def get_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_product(product_id: int, name=None, price=None, stock=None):
    conn = get_connection()
    cur = conn.cursor()

    if name is not None:
        cur.execute("UPDATE products SET name=? WHERE id=?", (name, product_id))
    if price is not None:
        cur.execute("UPDATE products SET price=? WHERE id=?", (price, product_id))
    if stock is not None:
        cur.execute("UPDATE products SET stock=? WHERE id=?", (stock, product_id))

    conn.commit()
    conn.close()


def delete_product(product_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
