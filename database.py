# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('data/inventario.db')
    cursor = conn.cursor()
    
    # Tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    # Tabla de ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad INTEGER NOT NULL,
            fecha TEXT DEFAULT (datetime('now'))
        )
    ''')

    # Productos de ejemplo
    cursor.execute('''
        INSERT OR IGNORE INTO productos (nombre, precio, stock) VALUES
        ('Laptop', 1500.0, 10),
        ('Ratón', 25.0, 50),
        ('Teclado', 70.0, 30)
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
