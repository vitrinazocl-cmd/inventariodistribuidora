from flask import Flask, jsonify, request, send_file
import random
import string
import os

app = Flask(__name__)

# ======================
# LISTAS (En Memoria)
# ======================
productos = []
clientes = []

# ======================
# DATOS BASE Y FUNCIONES (Tu código original)
# ======================
nombres = ["Juan", "Pedro", "Carlos", "Diego", "Luis", "Andrés", "Felipe", "María", "Camila", "Valentina", "Paula", "Daniela"]
apellidos = ["Pérez", "González", "Muñoz", "Rojas", "Díaz", "Soto", "Contreras", "Silva", "Martínez"]
calles = ["Av. Providencia", "Av. Libertador", "Calle Los Olivos", "Pasaje Las Flores", "Av. España", "Calle Prat"]
dominios = ["gmail.com", "hotmail.com", "outlook.com"]
bebidas = ["Coca-Cola", "Pepsi", "Fanta", "Sprite", "Agua Mineral", "Agua con Gas", "Red Bull", "Monster", "Cerveza Cristal", "Cerveza Escudo", "Corona", "Heineken", "Vino Cabernet", "Vino Sauvignon Blanc", "Whisky", "Ron", "Vodka", "Pisco"]
tipos_venta = ["Unidad", "Pack", "Caja", "Jaba"]

def generar_sku(idp): return f"BEB-{idp:05d}"
def generar_pasillo(): return random.choice(string.ascii_uppercase)
def generar_posicion(): return random.randint(1, 100)
def generar_direccion(): return f"{random.choice(calles)} #{random.randint(100,9999)}"
def generar_email(nombre, apellido): return f"{nombre.lower()}.{apellido.lower()}{random.randint(1,999)}@{random.choice(dominios)}"
def generar_telefono(): return f"+569{random.randint(10000000,99999999)}"

def cargar_datos():
    clientes.clear()
    productos.clear()
    # Reducimos a 50 para que la página web no se sature al cargar todo de golpe en la demo
    for i in range(1, 51):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        clientes.append({
            "id": i, "nombre": f"{nombre} {apellido}", "direccion": generar_direccion(),
            "email": generar_email(nombre, apellido), "telefono": generar_telefono()
        })
    for i in range(1, 51):
        tipo = random.choice(tipos_venta)
        if tipo == "Unidad": precio = random.randint(800, 3000)
        elif tipo == "Pack": precio = random.randint(4000, 12000)
        elif tipo == "Caja": precio = random.randint(12000, 40000)
        else: precio = random.randint(20000, 60000)
        productos.append({
            "id": i, "sku": generar_sku(i), "nombre": f"{random.choice(bebidas)} {random.randint(250,1500)}ml",
            "tipo_venta": tipo, "precio": precio, "stock": random.randint(10, 500),
            "pasillo": generar_pasillo(), "posicion": generar_posicion()
        })

# ======================
# RUTAS DE FLASK (API y Web)
# ======================

# 1. Ruta para entregar la página web
@app.route('/')
def home():
    return send_file('index.html')

# 2. Ruta para obtener los productos
@app.route('/api/productos', methods=['GET'])
def get_productos():
    return jsonify(productos)

# 3. Ruta para vender y descontar stock
@app.route('/api/vender', methods=['POST'])
def vender():
    data = request.json
    idp = data.get('id')
    cantidad = data.get('cantidad')
    
    for p in productos:
        if p["id"] == idp:
            if p["stock"] >= cantidad:
                p["stock"] -= cantidad
                return jsonify({"status": "success", "message": "Venta exitosa", "stock_actual": p["stock"]})
            else:
                return jsonify({"status": "error", "message": "Stock insuficiente"}), 400
    
    return jsonify({"status": "error", "message": "Producto no encontrado"}), 404

# ======================
# MAIN
# ======================
if __name__ == '__main__':
    cargar_datos()
    print("Datos cargados. Iniciando servidor en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
