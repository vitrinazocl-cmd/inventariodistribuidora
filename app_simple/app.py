from flask import Flask, jsonify, request, send_file
import sqlite3
import random
import string
import os

app = Flask(__name__)
DB_FILE = 'inventario.db'

# ======================
# CONFIGURACION DB Y DATOS INICIALES
# ======================
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT,
            nombre TEXT,
            tipo_venta TEXT,
            precio INTEGER,
            stock INTEGER,
            pasillo TEXT,
            posicion INTEGER
        )
    ''')
    conn.commit()
    
    # Revisamos si la base de datos está vacía para meter datos de prueba iniciales
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        cargar_datos_mock(conn)
    
    conn.close()

def cargar_datos_mock(conn):
    bebidas = ["Coca-Cola", "Pepsi", "Fanta", "Sprite", "Agua Mineral", "Agua con Gas", "Red Bull", "Monster", "Cerveza Cristal", "Corona", "Heineken", "Vino Cabernet", "Whisky", "Ron", "Vodka", "Pisco"]
    tipos_venta = ["Unidad", "Pack", "Caja", "Jaba"]

    def generar_sku(idp): return f"BEB-{idp:05d}"
    
    for i in range(1, 21): 
        tipo = random.choice(tipos_venta)
        if tipo == "Unidad": precio = random.randint(800, 3000)
        elif tipo == "Pack": precio = random.randint(4000, 12000)
        elif tipo == "Caja": precio = random.randint(12000, 40000)
        else: precio = random.randint(20000, 60000)
        
        conn.execute('''
            INSERT INTO productos (sku, nombre, tipo_venta, precio, stock, pasillo, posicion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (generar_sku(i), f"{random.choice(bebidas)} {random.randint(250,1500)}ml", tipo, precio, random.randint(10, 500), random.choice(string.ascii_uppercase), random.randint(1, 100)))
    conn.commit()

# ======================
# RUTAS DE FLASK (API y Web)
# ======================

# 1. Mostrar la página web
@app.route('/')
def home():
    return send_file('index.html')

# 1.5. Mostrar el logo
@app.route('/imagen1.jpeg')
def logo():
    return send_file('imagen1.jpeg')

# 2. Obtener productos de la Base de Datos
@app.route('/api/productos', methods=['GET'])
def get_productos():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in productos])

# 3. Registrar venta y bajar stock
@app.route('/api/vender', methods=['POST'])
def vender():
    data = request.json
    idp = data.get('id')
    cantidad = data.get('cantidad')
    
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (idp,)).fetchone()
    
    if producto is None:
        conn.close()
        return jsonify({"status": "error", "message": "Producto no encontrado"}), 404
        
    if producto['stock'] >= cantidad:
        nuevo_stock = producto['stock'] - cantidad
        conn.execute('UPDATE productos SET stock = ? WHERE id = ?', (nuevo_stock, idp))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Venta exitosa", "stock_actual": nuevo_stock})
    else:
        conn.close()
        return jsonify({"status": "error", "message": "Stock insuficiente"}), 400

# 4. Agregar un Producto Nuevo
@app.route('/api/productos', methods=['POST'])
def agregar_producto():
    data = request.json
    sku = f"BEB-{random.randint(10000, 99999)}"
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO productos (sku, nombre, tipo_venta, precio, stock, pasillo, posicion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        sku, 
        data.get('nombre'), 
        data.get('tipo_venta', 'Unidad'), 
        int(data.get('precio', 0)), 
        int(data.get('stock', 0)), 
        data.get('pasillo', 'A'), 
        int(data.get('posicion', 1))
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Producto agregado exitosamente"}), 201

# ======================
# MAIN
# ======================
# Iniciar DB antes de arrancar el servidor (importante para servidores como Render/Gunicorn)
init_db()

if __name__ == '__main__':
    print("Base de datos SQLite conectada. Iniciando servidor en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
