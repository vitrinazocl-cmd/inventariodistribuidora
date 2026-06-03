from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    nombre = Column(String, index=True)
    tipo_venta = Column(String)
    precio = Column(Integer)
    stock = Column(Integer)
    pasillo = Column(String)
    posicion = Column(Integer)

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    direccion = Column(String)
    email = Column(String, unique=True, index=True)
    telefono = Column(String)

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    cantidad = Column(Integer)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
    
    producto = relationship("Producto")
    cliente = relationship("Cliente")
