"""
Database initialization and connection.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("shop.db")


def get_connection():
    """Return a new database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # dict-like access to rows
    return conn


def init_db():
    """Initialize database tables if they don't exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Products table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0
        )
    """)

    # Carts table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            qty INTEGER NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    # Orders table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total REAL NOT NULL,
            address TEXT,
            payment_method TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)

    # Admins table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            user_id INTEGER PRIMARY KEY,
            role TEXT DEFAULT 'admin'
        )
    """)

    conn.commit()
    conn.close()
