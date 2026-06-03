import random
import os
import string

# ======================
# LISTAS
# ======================
productos = []
clientes = []

# ======================
# DATOS BASE
# ======================
nombres = [
    "Juan", "Pedro", "Carlos", "Diego", "Luis", "Andrés", "Felipe",
    "María", "Camila", "Valentina", "Paula", "Daniela"
]

apellidos = [
    "Pérez", "González", "Muñoz", "Rojas", "Díaz",
    "Soto", "Contreras", "Silva", "Martínez"
]

calles = [
    "Av. Providencia", "Av. Libertador", "Calle Los Olivos",
    "Pasaje Las Flores", "Av. España", "Calle Prat"
]

dominios = ["gmail.com", "hotmail.com", "outlook.com"]

# PRODUCTOS BEBIDAS
bebidas = [
    "Coca-Cola", "Pepsi", "Fanta", "Sprite",
    "Agua Mineral", "Agua con Gas",
    "Red Bull", "Monster",
    "Cerveza Cristal", "Cerveza Escudo", "Corona", "Heineken",
    "Vino Cabernet", "Vino Sauvignon Blanc",
    "Whisky", "Ron", "Vodka", "Pisco"
]

tipos_venta = ["Unidad", "Pack", "Caja", "Jaba"]

# ======================
# FUNCIONES GENERALES
# ======================
def limpiar():
    os.system("cls")

def generar_sku(idp):
    return f"BEB-{idp:05d}"

def generar_pasillo():
    return random.choice(string.ascii_uppercase)

def generar_posicion():
    return random.randint(1, 100)

def generar_direccion():
    return f"{random.choice(calles)} #{random.randint(100,9999)}"

def generar_email(nombre, apellido):
    return f"{nombre.lower()}.{apellido.lower()}{random.randint(1,999)}@{random.choice(dominios)}"

def generar_telefono():
    return f"+569{random.randint(10000000,99999999)}"

# ======================
# CARGA DE DATOS
# ======================
def cargar_datos():
    clientes.clear()
    productos.clear()

    # 1000 CLIENTES
    for i in range(1, 1001):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)

        clientes.append({
            "id": i,
            "nombre": f"{nombre} {apellido}",
            "direccion": generar_direccion(),
            "email": generar_email(nombre, apellido),
            "telefono": generar_telefono()
        })

    # 1000 PRODUCTOS BEBIDAS
    for i in range(1, 1001):
        tipo = random.choice(tipos_venta)

        # Ajuste de precios según tipo de venta
        if tipo == "Unidad":
            precio = random.randint(800, 3000)
        elif tipo == "Pack":
            precio = random.randint(4000, 12000)
        elif tipo == "Caja":
            precio = random.randint(12000, 40000)
        else:  # Jaba
            precio = random.randint(20000, 60000)

        productos.append({
            "id": i,
            "sku": generar_sku(i),
            "nombre": f"{random.choice(bebidas)} {random.randint(250,1500)}ml",
            "tipo_venta": tipo,
            "precio": precio,
            "stock": random.randint(10, 500),
            "pasillo": generar_pasillo(),
            "posicion": generar_posicion()
        })

# ======================
# PRODUCTOS
# ======================
def ver_productos():
    limpiar()
    print("=== INVENTARIO DISTRIBUIDORA ===\n")

    for p in productos:
        print(f"ID: {p['id']} | {p['sku']}")
        print(f"{p['nombre']} ({p['tipo_venta']})")
        print(f"Precio: ${p['precio']} | Stock: {p['stock']}")
        print(f"Ubicación: Pasillo {p['pasillo']} - Posición {p['posicion']}")
        print("-" * 50)

    input("\nEnter para continuar...")

def agregar_producto():
    limpiar()
    print("=== AGREGAR PRODUCTO ===\n")

    nombre = input("Nombre bebida: ")
    tipo = input("Tipo (Unidad/Pack/Caja/Jaba): ")
    precio = int(input("Precio: "))
    stock = int(input("Stock: "))

    nuevo_id = len(productos) + 1

    productos.append({
        "id": nuevo_id,
        "sku": generar_sku(nuevo_id),
        "nombre": nombre,
        "tipo_venta": tipo,
        "precio": precio,
        "stock": stock,
        "pasillo": generar_pasillo(),
        "posicion": generar_posicion()
    })

    print("\n✅ Producto agregado")
    input("Enter para continuar...")

def eliminar_producto():
    limpiar()
    print("=== ELIMINAR PRODUCTO ===\n")

    idp = int(input("Ingrese ID del producto: "))

    for p in productos:
        if p["id"] == idp:
            productos.remove(p)
            print("\n✅ Producto eliminado")
            break
    else:
        print("\n❌ Producto no encontrado")

    input("Enter para continuar...")

def consultar_stock():
    limpiar()
    print("=== CONSULTAR STOCK ===\n")

    idp = int(input("Ingrese ID del producto: "))

    for p in productos:
        if p["id"] == idp:
            print(f"\nNombre: {p['nombre']}")
            print(f"Tipo: {p['tipo_venta']}")
            print(f"SKU: {p['sku']}")
            print(f"Stock: {p['stock']}")
            print(f"Precio: ${p['precio']}")
            print(f"Ubicación: Pasillo {p['pasillo']} - Posición {p['posicion']}")
            break
    else:
        print("❌ Producto no encontrado")

    input("\nEnter para continuar...")

# ======================
# CLIENTES (sin cambios)
# ======================
def ver_clientes():
    limpiar()
    print("=== LISTADO DE CLIENTES ===\n")

    for c in clientes:
        print(f"ID: {c['id']} | {c['nombre']}")
        print(f"Dirección: {c['direccion']}")
        print(f"Email: {c['email']}")
        print(f"Teléfono: {c['telefono']}")
        print("-" * 40)

    input("\nEnter para continuar...")

def agregar_cliente():
    limpiar()
    print("=== AGREGAR CLIENTE ===\n")

    nombre = input("Nombre: ")
    direccion = input("Dirección: ")
    email = input("Email: ")
    telefono = input("Teléfono: ")

    nuevo_id = len(clientes) + 1

    clientes.append({
        "id": nuevo_id,
        "nombre": nombre,
        "direccion": direccion,
        "email": email,
        "telefono": telefono
    })

    print("\n✅ Cliente agregado")
    input("Enter para continuar...")

def eliminar_cliente():
    limpiar()
    print("=== ELIMINAR CLIENTE ===\n")

    idc = int(input("Ingrese ID del cliente: "))

    for c in clientes:
        if c["id"] == idc:
            clientes.remove(c)
            print("\n✅ Cliente eliminado")
            break
    else:
        print("\n❌ Cliente no encontrado")

    input("Enter para continuar...")

# ======================
# MENÚ
# ======================
def menu():
    while True:
        limpiar()
        print("=== SISTEMA DISTRIBUIDORA BEBIDAS ===")
        print("1. Ver productos")
        print("2. Agregar producto")
        print("3. Eliminar producto")
        print("4. Consultar stock")
        print("5. Ver clientes")
        print("6. Agregar cliente")
        print("7. Eliminar cliente")
        print("0. Salir")

        op = input("Opción: ")

        if op == "1":
            ver_productos()
        elif op == "2":
            agregar_producto()
        elif op == "3":
            eliminar_producto()
        elif op == "4":
            consultar_stock()
        elif op == "5":
            ver_clientes()
        elif op == "6":
            agregar_cliente()
        elif op == "7":
            eliminar_cliente()
        elif op == "0":
            break
        else:
            input("Opción inválida...")

# ======================
# MAIN
# ======================
cargar_datos()
menu()