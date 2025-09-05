"""
Order-related database functions.
"""

from database.db import get_connection


def create_order(user_id: int, items: list, total: float, address: str, payment_method: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO orders (user_id, total, address, payment_method, status) VALUES (?, ?, ?, ?, ?)",
        (user_id, total, address, payment_method, "pending"),
    )
    conn.commit()
    order_id = cur.lastrowid
    conn.close()
    return order_id


def get_orders(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_order_status(order_id: int, status: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    conn.commit()
    conn.close()
