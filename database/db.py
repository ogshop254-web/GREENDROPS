"""
Database initialization and connection.
"""

import sqlite3
from pathlib import Path

DB_NAME = "shop.db"


def get_connection():
    """Return a new database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # dict-like access to rows
    return conn


def init_db():
    """Initialize database tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

     # Products table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
)
    """)

    # Cart table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            PRIMARY KEY (user_id, product_id)
        )
    """)

    # Orders table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            items TEXT,
            total REAL,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()
# ============================
# Cart Functions
# ============================

def add_to_cart(user_id, product_id, quantity=1):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # If product already exists → increase qty
    cursor.execute(
        "SELECT quantity FROM cart WHERE user_id=? AND product_id=?",
        (user_id, product_id)
    )
    row = cursor.fetchone()

    if row:
        cursor.execute(
            "UPDATE cart SET quantity = quantity + 1 WHERE user_id=? AND product_id=?",
            (user_id, product_id)
        )
    else:
        cursor.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1)",
            (user_id, product_id)
        )

    conn.commit()
    conn.close()

    
def get_cart(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name, p.price, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_cart(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def add_order(user_id, items, total):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (user_id, items, total, status)
        VALUES (?, ?, ?, 'Pending')
    """, (user_id, items, total))
    conn.commit()
    conn.close()


def get_orders(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, items, total, status
        FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def remove_from_cart(user_id, product_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Check current quantity
    cur.execute(
        "SELECT quantity FROM cart WHERE user_id=? AND product_id=?",
        (user_id, product_id)
    )
    row = cur.fetchone()

    if not row:
        conn.close()
        return False  # nothing to remove

    qty = row[0]
    if qty > 1:
        # reduce quantity
        cur.execute(
            "UPDATE cart SET quantity = quantity - 1 WHERE user_id=? AND product_id=?",
            (user_id, product_id)
        )
    else:
        # delete the row completely
        cur.execute(
            "DELETE FROM cart WHERE user_id=? AND product_id=?",
            (user_id, product_id)
        )

    conn.commit()
    conn.close()
    return True

def clear_cart(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()