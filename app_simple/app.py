from flask import Flask, jsonify, request, send_file, Response
import random
import string
import os
import csv
import io

app = Flask(__name__)

# ======================
# CONFIGURACION DB Y ENRUTADOR
# ======================
DATABASE_URL = os.environ.get('DATABASE_URL')
USE_POSTGRES = DATABASE_URL is not None

if USE_POSTGRES:
    import psycopg2
    import psycopg2.extras
else:
    import sqlite3

def get_db_connection():
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        conn = sqlite3.connect('inventario.db')
        conn.row_factory = sqlite3.Row
        return conn

def run_query(conn, query, params=()):
    """
    Enrutador inteligente que traduce las consultas de SQLite a PostgreSQL al vuelo.
    """
    if USE_POSTGRES:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # Traducciones de SQLite a PostgreSQL
        q = query.replace('?', '%s')
        q = q.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
        q = q.replace("DATETIME DEFAULT (datetime('now', 'localtime'))", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        q = q.replace('IFNULL', 'COALESCE')
        q = q.replace("date('now', 'localtime')", "CURRENT_DATE")
        q = q.replace("strftime('%W', fecha) = strftime('%W', 'now', 'localtime')", "EXTRACT(WEEK FROM fecha) = EXTRACT(WEEK FROM CURRENT_DATE)")
        q = q.replace("strftime('%m', fecha) = strftime('%m', 'now', 'localtime')", "EXTRACT(MONTH FROM fecha) = EXTRACT(MONTH FROM CURRENT_DATE)")
        q = q.replace("strftime('%Y', fecha) = strftime('%Y', 'now', 'localtime')", "EXTRACT(YEAR FROM fecha) = EXTRACT(YEAR FROM CURRENT_DATE)")
        
        cur.execute(q, params)
        return cur
    else:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur

def init_db():
    conn = get_db_connection()
    run_query(conn, '''
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
    
    run_query(conn, '''
        CREATE TABLE IF NOT EXISTS historial_ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATETIME DEFAULT (datetime('now', 'localtime')),
            producto_id INTEGER,
            nombre_producto TEXT,
            cantidad INTEGER,
            subtotal INTEGER,
            descuento INTEGER,
            iva INTEGER,
            total_final INTEGER
        )
    ''')
    conn.commit()
    
    # Revisamos si la base de datos está vacía
    cursor = run_query(conn, 'SELECT COUNT(*) as count FROM productos')
    if cursor.fetchone()['count'] == 0:
        cargar_datos_mock(conn)
    
    conn.close()

def cargar_datos_mock(conn):
    licores = ["Pisco Alto del Carmen", "Pisco Mistral", "Pisco Capel", "Whisky Johnnie Walker", "Vodka Absolut", "Ron Bacardi"]
    vinos = ["Vino Casillero del Diablo", "Vino Gato Negro", "Vino Misiones de Rengo"]
    cervezas = ["Cerveza Cristal", "Cerveza Escudo", "Cerveza Corona", "Cerveza Heineken"]
    bebidas = ["Coca-Cola", "Pepsi", "Fanta", "Sprite", "Kem Piña", "Bilz", "Pap", "Red Bull"]

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
        en_promocion = 1 if i <= 20 else 0
        
        run_query(conn, '''
            INSERT INTO productos (sku, nombre, tipo_venta, precio, stock, pasillo, posicion, en_promocion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (generar_sku(i), nombre_final, tipo, precio, random.randint(0, 1000), random.choice(string.ascii_uppercase), random.randint(1, 100), en_promocion))
    conn.commit()

# ======================
# RUTAS DE FLASK (API y Web)
# ======================

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/imagen1.jpeg')
def logo():
    return send_file('imagen1.jpeg')

@app.route('/api/productos', methods=['GET'])
def get_productos():
    conn = get_db_connection()
    
    necesarios = ["Coca-Cola 1.25L", "Fanta 1.25L", "Sprite 1.25L"]
    for nombre in necesarios:
        existe = run_query(conn, 'SELECT 1 FROM productos WHERE nombre = ?', (nombre,)).fetchone()
        if not existe:
            run_query(conn, '''
                INSERT INTO productos (sku, nombre, tipo_venta, precio, stock, pasillo, posicion, en_promocion)
                VALUES (?, ?, 'Unidad', 1200, 500, 'A', 1, 0)
            ''', (f"BEB-125-{random.randint(10,99)}", nombre))
            conn.commit()
            
    productos = run_query(conn, 'SELECT * FROM productos').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in productos])

@app.route('/api/productos', methods=['POST'])
def agregar_producto():
    data = request.json
    sku = f"BEB-{random.randint(10000, 99999)}"
    
    conn = get_db_connection()
    run_query(conn, '''
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

@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    conn = get_db_connection()
    producto = run_query(conn, 'SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    
    if producto is None:
        conn.close()
        return jsonify({"status": "error", "message": "Producto no encontrado"}), 404
        
    run_query(conn, 'DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Producto eliminado exitosamente"})

@app.route('/api/venta_masiva', methods=['POST'])
def venta_masiva():
    data = request.json
    items = data.get('items', [])
    
    if not items:
        return jsonify({"status": "error", "message": "El carrito está vacío"}), 400
        
    conn = get_db_connection()
    
    try:
        for item in items:
            if item.get('is_jaba_mixta'):
                for sub in item['sub_items']:
                    idp = sub['id']
                    sub_qty = sub['qty'] * item['cantidad']
                    
                    if sub_qty > 0:
                        producto = run_query(conn, 'SELECT * FROM productos WHERE id = ?', (idp,)).fetchone()
                        if producto is None:
                            raise Exception("Producto componente de Jaba no encontrado")
                        if producto['stock'] < sub_qty:
                            raise Exception(f"Falta stock de {producto['nombre']} para armar la Jaba Mixta")
                            
                        nuevo_stock = producto['stock'] - sub_qty
                        run_query(conn, 'UPDATE productos SET stock = ? WHERE id = ?', (nuevo_stock, idp))
                
                total_pagar = item['precio'] * item['cantidad']
                neto_item = int(total_pagar / 1.19)
                iva_item = total_pagar - neto_item
                run_query(conn, '''
                    INSERT INTO historial_ventas (fecha, producto_id, nombre_producto, cantidad, subtotal, descuento, iva, total_final)
                    VALUES (datetime('now', 'localtime'), 0, ?, ?, ?, 0, ?, ?)
                ''', (item['nombre'], item['cantidad'], neto_item, iva_item, total_pagar))
                
            else:
                idp = item['id']
                cantidad = item['cantidad']
                
                producto = run_query(conn, 'SELECT * FROM productos WHERE id = ?', (idp,)).fetchone()
                
                if producto is None:
                    raise Exception(f"Producto ID {idp} no encontrado en la base de datos.")
                    
                if producto['stock'] < cantidad:
                    raise Exception(f"Stock insuficiente para {producto['nombre']}.")
                    
                nuevo_stock = producto['stock'] - cantidad
                run_query(conn, 'UPDATE productos SET stock = ? WHERE id = ?', (nuevo_stock, idp))
                
                total_item = producto['precio'] * cantidad
                descto_item = int(total_item * 0.03) if (producto['en_promocion'] == 1 and cantidad > 10) else 0
                total_pagar = total_item - descto_item
                
                neto_item = int(total_pagar / 1.19)
                iva_item = total_pagar - neto_item
                
                run_query(conn, '''
                    INSERT INTO historial_ventas (fecha, producto_id, nombre_producto, cantidad, subtotal, descuento, iva, total_final)
                    VALUES (datetime('now', 'localtime'), ?, ?, ?, ?, ?, ?, ?)
                ''', (idp, producto['nombre'], cantidad, neto_item, descto_item, iva_item, total_pagar))
            
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"status": "error", "message": str(e)}), 400
        
    conn.close()
    return jsonify({"status": "success", "message": "Venta procesada con éxito y stock descontado."})

@app.route('/api/reportes', methods=['GET'])
def obtener_reportes():
    conn = get_db_connection()
    hoy = run_query(conn, "SELECT IFNULL(SUM(total_final), 0) as t FROM historial_ventas WHERE date(fecha) = date('now', 'localtime')").fetchone()['t']
    semana = run_query(conn, "SELECT IFNULL(SUM(total_final), 0) as t FROM historial_ventas WHERE strftime('%W', fecha) = strftime('%W', 'now', 'localtime') AND strftime('%Y', fecha) = strftime('%Y', 'now', 'localtime')").fetchone()['t']
    mes = run_query(conn, "SELECT IFNULL(SUM(total_final), 0) as t FROM historial_ventas WHERE strftime('%m', fecha) = strftime('%m', 'now', 'localtime') AND strftime('%Y', fecha) = strftime('%Y', 'now', 'localtime')").fetchone()['t']
    ano = run_query(conn, "SELECT IFNULL(SUM(total_final), 0) as t FROM historial_ventas WHERE strftime('%Y', fecha) = strftime('%Y', 'now', 'localtime')").fetchone()['t']
    ultimas = run_query(conn, "SELECT * FROM historial_ventas ORDER BY id DESC LIMIT 50").fetchall()
    conn.close()
    
    return jsonify({
        "hoy": hoy,
        "semana": semana,
        "mes": mes,
        "ano": ano,
        "ultimas": [dict(ix) for ix in ultimas]
    })

@app.route('/api/descargar_excel', methods=['GET'])
def descargar_excel():
    conn = get_db_connection()
    ventas = run_query(conn, "SELECT * FROM historial_ventas ORDER BY id DESC").fetchall()
    conn.close()
    
    salida = io.StringIO()
    writer = csv.writer(salida, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['ID Venta', 'Fecha y Hora', 'ID Producto', 'Nombre Producto', 'Unidades Vendidas', 'Subtotal Neto ($)', 'Descuento ($)', 'IVA 19% ($)', 'Total Cobrado ($)'])
    
    for v in ventas:
        writer.writerow([v['id'], v['fecha'], v['producto_id'], v['nombre_producto'], v['cantidad'], v['subtotal'], v['descuento'], v['iva'], v['total_final']])
    
    return Response(
        salida.getvalue().encode('utf-8-sig'), 
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=Reporte_Distribuidora.csv"}
    )

init_db()

if __name__ == '__main__':
    print("Servidor iniciando en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
