"""
Cart-related database functions.
"""

from database.db import get_connection


def add_to_cart(user_id: int, product_id: int, qty: int = 1):
    conn = get_connection()
    cur = conn.cursor()

    # If item already in cart, increase qty
    cur.execute(
        "SELECT qty FROM carts WHERE user_id=? AND product_id=?",
        (user_id, product_id),
    )
    row = cur.fetchone()

    if row:
        new_qty = row["qty"] + qty
        cur.execute(
            "UPDATE carts SET qty=? WHERE user_id=? AND product_id=?",
            (new_qty, user_id, product_id),
        )
    else:
        cur.execute(
            "INSERT INTO carts (user_id, product_id, qty) VALUES (?, ?, ?)",
            (user_id, product_id, qty),
        )

    conn.commit()
    conn.close()


def get_cart(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT c.id, p.name, p.price, c.qty, (p.price * c.qty) AS subtotal
        FROM carts c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id=?
        """,
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def clear_cart(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM carts WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
