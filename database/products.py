import sqlite3

DB_NAME = "shop.db"

def add_product(name, price):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)", (name, price)
    )
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM products")
    products = cur.fetchall()
    conn.close()
    return products
