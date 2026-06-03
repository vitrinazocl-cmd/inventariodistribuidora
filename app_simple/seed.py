import sqlite3
import random
import string

DB_FILE = 'inventario.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

def inyectar_1000_productos():
    conn = get_db_connection()
    
    # Limpiamos la tabla antigua por si quieres correr el script más de una vez
    conn.execute('DELETE FROM productos')
    
    # Listas enriquecidas
    licores = ["Pisco Alto del Carmen", "Pisco Mistral", "Pisco Capel", "Whisky Johnnie Walker Red", "Whisky Johnnie Walker Black", "Whisky Chivas Regal", "Ron Bacardi Añejo", "Ron Havana Club", "Ron Flor de Caña", "Vodka Absolut", "Vodka Smirnoff", "Tequila Jose Cuervo", "Gin Tanqueray", "Gin Beefeater", "Baileys", "Jägermeister", "Fernet Branca"]
    vinos = ["Vino Casillero del Diablo Cabernet", "Vino Gato Negro Merlot", "Vino Concha y Toro Sauvignon Blanc", "Vino Santa Helena Cármenère", "Vino Misiones de Rengo", "Vino Tarapacá Gran Reserva", "Vino 120 Santa Rita"]
    cervezas = ["Cerveza Cristal", "Cerveza Escudo", "Cerveza Royal Guard", "Cerveza Corona", "Cerveza Heineken", "Cerveza Stella Artois", "Cerveza Becker", "Cerveza Kunstmann Torobayo", "Cerveza Austral Calafate"]
    bebidas = ["Coca-Cola", "Coca-Cola Zero", "Pepsi", "Fanta", "Sprite", "Kem Piña", "Bilz", "Pap", "Crush", "Canada Dry Ginger Ale", "Agua Mineral Cachantun", "Agua Benedictino", "Red Bull", "Monster Energy", "Jugo Watts Durazno", "Jugo Andina Naranja", "Gatorade Blue"]

    todas_las_bebidas = licores + vinos + cervezas + bebidas
    tipos_venta = ["Unidad", "Pack", "Caja", "Jaba"]

    def generar_sku(idp): return f"BEB-{idp:05d}"
    def generar_pasillo(): return random.choice(string.ascii_uppercase)
    def generar_posicion(): return random.randint(1, 100)
    
    print("Iniciando inyección de 1000 productos...")

    for i in range(1, 1001):
        nombre_base = random.choice(todas_las_bebidas)
        tipo = random.choice(tipos_venta)
        
        # Asignar precios lógicos dependiendo de la categoría
        if nombre_base in licores:
            precio_base = random.randint(6000, 25000)
        elif nombre_base in vinos:
            precio_base = random.randint(3000, 15000)
        elif nombre_base in cervezas:
            precio_base = random.randint(1000, 2500)
        else:
            precio_base = random.randint(800, 2500)

        # Ajuste de precio por tipo de empaque
        if tipo == "Unidad": precio = precio_base
        elif tipo == "Pack": precio = precio_base * random.randint(4, 6)
        elif tipo == "Caja": precio = precio_base * random.randint(12, 24)
        else: precio = precio_base * random.randint(6, 12) # Jaba

        tamano = random.choice(["350cc", "500cc", "1L", "1.5L", "2L", "3L", "750ml"])
        nombre_final = f"{nombre_base} {tamano}"
        
        conn.execute('''
            INSERT INTO productos (sku, nombre, tipo_venta, precio, stock, pasillo, posicion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (generar_sku(i), nombre_final, tipo, precio, random.randint(0, 1000), generar_pasillo(), generar_posicion()))
        
        # Pequeño feedback de progreso
        if i % 100 == 0:
            print(f"Cargados {i} productos...")

    conn.commit()
    conn.close()
    print("¡Base de datos inyectada con éxito! Ahora tienes 1000 productos reales.")

if __name__ == '__main__':
    inyectar_1000_productos()
