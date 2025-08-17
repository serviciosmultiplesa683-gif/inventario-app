print("hola el app.py se esta ejecutando")
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('data/inventario.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    conn = get_db_connection()
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        conn.execute('INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)',
                     (nombre, precio, stock))
        conn.commit()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))

@app.route('/ventas', methods=['GET', 'POST'])
def ventas():
    conn = get_db_connection()
    if request.method == 'POST':
        producto_id = int(request.form['producto_id'])
        cantidad = int(request.form['cantidad'])
        producto = conn.execute('SELECT stock FROM productos WHERE id = ?', (producto_id,)).fetchone()
        if producto and producto['stock'] >= cantidad:
            conn.execute('INSERT INTO ventas (producto_id, cantidad) VALUES (?, ?)', (producto_id, cantidad))
            conn.execute('UPDATE productos SET stock = stock - ? WHERE id = ?', (cantidad, producto_id))
            conn.commit()
        else:
            return "Error: Stock insuficiente o producto no existe.", 400
    ventas = conn.execute('''
        SELECT v.id, p.nombre, v.cantidad, p.precio, v.fecha
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        ORDER BY v.fecha DESC
    ''').fetchall()
    productos = conn.execute('SELECT id, nombre FROM productos WHERE stock > 0').fetchall()
    conn.close()
    return render_template('ventas.html', ventas=ventas, productos=productos)

if __name__ == '__main__':
    from database import init_db
    port = int(os.getenv("PORT", 5000))  # ✅ Así sí
    app.run(host='0.0.0.0', port=port)
