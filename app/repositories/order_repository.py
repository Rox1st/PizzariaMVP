from app.repositories.database import get_connection


class OrderRepository:
    def __init__(self, database='pizzaria.db'):
        self.database = database

    def create(self, order, items):
        conn = get_connection(self.database)
        cur = conn.execute('''INSERT INTO orders
            (customer_name, phone, address, order_type, status, payment_method, paid, delivery_fee, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (order.customer_name, order.phone, order.address, order.order_type.value,
             order.status.value, order.payment_method, int(order.paid), order.delivery_fee, order.total))
        order_id = cur.lastrowid
        conn.executemany('INSERT INTO order_items(order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
                         [(order_id, i.product_id, i.quantity, i.unit_price) for i in items])
        conn.execute('INSERT INTO order_status_history(order_id, old_status, new_status) VALUES (?, ?, ?)',
                     (order_id, None, order.status.value))
        conn.commit(); conn.close()
        return order_id

    def list_all(self):
        conn = get_connection(self.database)
        rows = conn.execute('SELECT * FROM orders ORDER BY id DESC').fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def find(self, order_id):
        conn = get_connection(self.database)
        row = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def update_status(self, order_id, status):
        conn = get_connection(self.database)
        row = conn.execute('SELECT status FROM orders WHERE id = ?', (order_id,)).fetchone()
        if not row:
            conn.close(); return None
        old = row['status']
        conn.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
        conn.commit(); conn.close()
        return old

    def mark_paid(self, order_id):
        conn = get_connection(self.database)
        cur = conn.execute('UPDATE orders SET paid = 1 WHERE id = ?', (order_id,))
        conn.commit(); conn.close()
        return cur.rowcount > 0

    def add_status_history(self, order_id, old_status, new_status):
        conn = get_connection(self.database)
        conn.execute('INSERT INTO order_status_history(order_id, old_status, new_status) VALUES (?, ?, ?)',
                     (order_id, old_status, new_status))
        conn.commit(); conn.close()
