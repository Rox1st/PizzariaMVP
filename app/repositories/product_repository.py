from app.repositories.database import get_connection


class ProductRepository:
    def __init__(self, database='pizzaria.db'):
        self.database = database

    def list_available(self):
        conn = get_connection(self.database)
        rows = conn.execute('SELECT * FROM products WHERE available = 1 ORDER BY category, name').fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def find(self, product_id):
        conn = get_connection(self.database)
        row = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        conn.close()
        return dict(row) if row else None
