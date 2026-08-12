import sqlite3
from pathlib import Path

SCHEMA = '''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    available INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT,
    order_type TEXT NOT NULL,
    status TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    paid INTEGER NOT NULL DEFAULT 0,
    delivery_fee REAL NOT NULL DEFAULT 0,
    total REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);
CREATE TABLE IF NOT EXISTS order_status_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    old_status TEXT,
    new_status TEXT NOT NULL,
    changed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(order_id) REFERENCES orders(id)
);
'''


def get_connection(database='pizzaria.db'):
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db(database='pizzaria.db'):
    Path(database).parent.mkdir(parents=True, exist_ok=True) if Path(database).parent != Path('.') else None
    conn = get_connection(database)
    conn.executescript(SCHEMA)
    count = conn.execute('SELECT COUNT(*) AS n FROM products').fetchone()['n']
    if count == 0:
        conn.executemany(
            'INSERT INTO products(name, category, price) VALUES (?, ?, ?)',
            [
                ('Calabresa Grande', 'Pizza', 45.90),
                ('Quatro Queijos Grande', 'Pizza', 49.90),
                ('Frango com Catupiry Grande', 'Pizza', 47.90),
                ('Coca-Cola 2L', 'Bebida', 9.00),
                ('Guaraná 1L', 'Bebida', 7.00),
            ],
        )
    conn.commit()
    conn.close()
