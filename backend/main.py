from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import models, database

# Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API Distribuidora Bebidas")

# Configuración CORS para permitir peticiones desde React (Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Esquemas Pydantic para Validar Datos ---
class ProductoBase(BaseModel):
    sku: str
    nombre: str
    tipo_venta: str
    precio: int
    stock: int
    pasillo: str
    posicion: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    class Config:
        orm_mode = True

class VentaCreate(BaseModel):
    producto_id: int
    cantidad: int
    cliente_id: int = None

# --- Rutas (Endpoints) ---

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de la Distribuidora"}

# Productos
@app.get("/productos", response_model=List[Producto])
def get_productos(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    productos = db.query(models.Producto).offset(skip).limit(limit).all()
    return productos

@app.post("/productos", response_model=Producto)
def create_producto(producto: ProductoCreate, db: Session = Depends(database.get_db)):
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

# Ventas (Descuenta Stock)
@app.post("/vender")
def realizar_venta(venta: VentaCreate, db: Session = Depends(database.get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == venta.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if producto.stock < venta.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")
    
    # Descontar stock
    producto.stock -= venta.cantidad
    
    # Registrar venta
    db_venta = models.Venta(**venta.dict())
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)
    
    return {"message": "Venta realizada con éxito", "producto": producto.nombre, "stock_restante": producto.stock}
