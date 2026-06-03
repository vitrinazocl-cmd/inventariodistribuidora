import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(false);

  // Funciones simuladas si el backend no está corriendo aún
  const loadMockData = () => {
    setProductos([
      { id: 1, sku: 'BEB-00001', nombre: 'Coca-Cola 1.5L', tipo_venta: 'Pack', precio: 10000, stock: 150, pasillo: 'A', posicion: 10 },
      { id: 2, sku: 'BEB-00002', nombre: 'Cerveza Cristal', tipo_venta: 'Caja', precio: 15000, stock: 45, pasillo: 'B', posicion: 5 },
      { id: 3, sku: 'BEB-00003', nombre: 'Agua Mineral con Gas', tipo_venta: 'Unidad', precio: 800, stock: 300, pasillo: 'C', posicion: 1 }
    ]);
  };

  useEffect(() => {
    // Intentar cargar desde la API, si falla cargar mock data
    axios.get('http://127.0.0.1:8000/productos')
      .then(res => setProductos(res.data))
      .catch(err => {
        console.error("Backend no detectado, cargando datos de prueba...");
        loadMockData();
      });
  }, []);

  const handleVender = (id) => {
    const cantidad = prompt("Ingrese cantidad a vender:");
    if (!cantidad) return;
    
    // Simulación de venta para efectos visuales (El backend real descontaría esto en la DB)
    setProductos(prev => prev.map(p => {
      if (p.id === id) {
        return { ...p, stock: p.stock - parseInt(cantidad) };
      }
      return p;
    }));
    alert("Venta registrada. Stock actualizado.");
  };

  return (
    <div className="container" style={{ marginTop: '50px', paddingBottom: '50px' }}>
      <h1 style={{ marginBottom: '30px' }}>Panel de Inventario</h1>
      
      <div className="glass-panel" style={{ padding: '20px', overflowX: 'auto' }}>
        <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
              <th style={{ padding: '15px' }}>SKU</th>
              <th style={{ padding: '15px' }}>Producto</th>
              <th style={{ padding: '15px' }}>Tipo</th>
              <th style={{ padding: '15px' }}>Precio</th>
              <th style={{ padding: '15px' }}>Stock</th>
              <th style={{ padding: '15px' }}>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {productos.map(p => (
              <tr key={p.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                <td style={{ padding: '15px', color: 'var(--text-muted)' }}>{p.sku}</td>
                <td style={{ padding: '15px', fontWeight: '600' }}>{p.nombre}</td>
                <td style={{ padding: '15px' }}>
                  <span style={{ 
                    padding: '4px 8px', 
                    borderRadius: '4px', 
                    backgroundColor: 'rgba(233, 69, 96, 0.2)', 
                    color: 'var(--highlight)',
                    fontSize: '0.85rem'
                  }}>
                    {p.tipo_venta}
                  </span>
                </td>
                <td style={{ padding: '15px' }}>${p.precio}</td>
                <td style={{ padding: '15px' }}>
                  <span style={{ color: p.stock < 50 ? 'var(--danger)' : 'var(--success)', fontWeight: 'bold' }}>
                    {p.stock}
                  </span>
                </td>
                <td style={{ padding: '15px' }}>
                  <button onClick={() => handleVender(p.id)} className="btn btn-primary" style={{ padding: '8px 16px', fontSize: '0.9rem' }}>
                    Registrar Venta
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
