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
            posicion INTEGER,
            en_promocion INTEGER DEFAULT 0
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
    licores = ["Pisco Alto del Carmen", "Pisco Mistral", "Pisco Capel", "Whisky Johnnie Walker Red", "Whisky Johnnie Walker Black", "Whisky Chivas Regal", "Ron Bacardi Añejo", "Ron Havana Club", "Ron Flor de Caña", "Vodka Absolut", "Vodka Smirnoff", "Tequila Jose Cuervo", "Gin Tanqueray", "Gin Beefeater", "Baileys", "Jägermeister", "Fernet Branca"]
    vinos = ["Vino Casillero del Diablo Cabernet", "Vino Gato Negro Merlot", "Vino Concha y Toro Sauvignon Blanc", "Vino Santa Helena Cármenère", "Vino Misiones de Rengo", "Vino Tarapacá Gran Reserva", "Vino 120 Santa Rita"]
    cervezas = ["Cerveza Cristal", "Cerveza Escudo", "Cerveza Royal Guard", "Cerveza Corona", "Cerveza Heineken", "Cerveza Stella Artois", "Cerveza Becker", "Cerveza Kunstmann Torobayo", "Cerveza Austral Calafate"]
    bebidas = ["Coca-Cola", "Coca-Cola Zero", "Pepsi", "Fanta", "Sprite", "Kem Piña", "Bilz", "Pap", "Crush", "Canada Dry Ginger Ale", "Agua Mineral Cachantun", "Agua Benedictino", "Red Bull", "Monster Energy", "Jugo Watts Durazno", "Jugo Andina Naranja", "Gatorade Blue"]

    todas_las_bebidas = licores + vinos + cervezas + bebidas
    tipos_venta = ["Unidad", "Pack", "Caja", "Jaba"]

    def generar_sku(idp): return f"BEB-{idp:05d}"
    
    for i in range(1, 1001): 
        nombre_base = random.choice(todas_las_bebidas)
        tipo = random.choice(tipos_venta)
        
        if nombre_base in licores: precio_base = random.randint(6000, 25000)
        elif nombre_base in vinos: precio_base = random.randint(3000, 15000)
        elif nombre_base in cervezas: precio_base = random.randint(1000, 2500)
        else: precio_base = random.randint(800, 2500)

        if tipo == "Unidad": precio = precio_base
        elif tipo == "Pack": precio = precio_base * random.randint(4, 6)
        elif tipo == "Caja": precio = precio_base * random.randint(12, 24)
        else: precio = precio_base * random.randint(6, 12)

        tamano = random.choice(["350cc", "500cc", "1L", "1.5L", "2L", "3L", "750ml"])
        nombre_final = f"{nombre_base} {tamano}"
        
        # Dejaremos exactamente 20 productos con promoción de ejemplo
        en_promocion = 1 if i <= 20 else 0
        
        conn.execute('''
            INSERT INTO productos (sku, nombre, tipo_venta, precio, stock, pasillo, posicion, en_promocion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (generar_sku(i), nombre_final, tipo, precio, random.randint(0, 1000), random.choice(string.ascii_uppercase), random.randint(1, 100), en_promocion))
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
        total = producto['precio'] * cantidad
        descuento = 0
        
        # Calcular descuento del 3% si tiene promo y son más de 10 unidades
        if producto['en_promocion'] == 1 and cantidad > 10:
            descuento = int(total * 0.03)
            total -= descuento
            
        nuevo_stock = producto['stock'] - cantidad
        conn.execute('UPDATE productos SET stock = ? WHERE id = ?', (nuevo_stock, idp))
        conn.commit()
        conn.close()
        
        mensaje = f"Venta exitosa. Total a cobrar: ${total}"
        if descuento > 0:
            mensaje += f" (Incluye un descuento del 3%: ahorró ${descuento})"
            
        return jsonify({"status": "success", "message": mensaje, "stock_actual": nuevo_stock})
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
        INSERT INTO productos (sku, nombre, tipo_venta, precio, stock, pasillo, posicion, en_promocion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        sku, 
        data.get('nombre'), 
        data.get('tipo_venta', 'Unidad'), 
        int(data.get('precio', 0)), 
        int(data.get('stock', 0)), 
        data.get('pasillo', 'A'), 
        int(data.get('posicion', 1)),
        int(data.get('en_promocion', 0))
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Producto agregado exitosamente"}), 201

# 5. Eliminar un Producto
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    
    if producto is None:
        conn.close()
        return jsonify({"status": "error", "message": "Producto no encontrado"}), 404
        
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Producto eliminado exitosamente"})

# ======================
# MAIN
# ======================
# Iniciar DB antes de arrancar el servidor (importante para servidores como Render/Gunicorn)
init_db()

if __name__ == '__main__':
    print("Base de datos SQLite conectada. Iniciando servidor en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
