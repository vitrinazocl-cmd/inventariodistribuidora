import React from 'react';
import { MapPin, ShoppingCart, Truck, ShieldCheck } from 'lucide-react';

const LandingPage = () => {
  return (
    <div style={{ paddingBottom: '100px' }}>
      {/* Hero Section */}
      <section style={{
        minHeight: '80vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(rgba(26, 26, 46, 0.8), rgba(26, 26, 46, 0.9)), url("https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80") center/cover',
        textAlign: 'center',
        padding: '0 20px'
      }}>
        <div style={{ maxWidth: '800px' }}>
          <h1 style={{ fontSize: '4rem', marginBottom: '20px', color: '#fff' }}>Refresca tu negocio, <span style={{ color: 'var(--highlight)' }}>al mejor precio</span></h1>
          <p style={{ fontSize: '1.2rem', marginBottom: '40px', color: 'var(--text-muted)' }}>
            Distribuidora mayorista y minorista con el catálogo más amplio de bebidas, cervezas y licores. 
            Abastecemos a cientos de comercios en la Región Metropolitana.
          </p>
          <div style={{ display: 'flex', gap: '20px', justifyContent: 'center' }}>
            <button className="btn btn-primary">Catálogo Mayorista</button>
            <button className="btn btn-outline">Comprar al Detalle</button>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="container" style={{ marginTop: '-50px', position: 'relative', zIndex: 10 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '30px' }}>
          {[
            { icon: <Truck size={40} color="var(--highlight)" />, title: "Despacho Rápido", desc: "Entregas en menos de 24 hrs" },
            { icon: <ShoppingCart size={40} color="var(--highlight)" />, title: "Precios por Volumen", desc: "Mientras más llevas, menos pagas" },
            { icon: <ShieldCheck size={40} color="var(--highlight)" />, title: "Stock Garantizado", desc: "Miles de productos disponibles" }
          ].map((feature, idx) => (
            <div key={idx} className="glass-panel" style={{ padding: '30px', textAlign: 'center' }}>
              <div style={{ marginBottom: '20px' }}>{feature.icon}</div>
              <h3 style={{ marginBottom: '10px' }}>{feature.title}</h3>
              <p style={{ color: 'var(--text-muted)' }}>{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Sucursales */}
      <section className="container" style={{ marginTop: '100px' }}>
        <h2 style={{ textAlign: 'center', fontSize: '2.5rem', marginBottom: '50px' }}>Nuestras Sucursales</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '40px' }}>
          <div className="glass-panel" style={{ padding: '40px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '20px' }}>
              <MapPin size={32} color="var(--highlight)" />
              <h3>Sucursal Cerro Navia</h3>
            </div>
            <p style={{ color: 'var(--text-muted)', marginBottom: '20px' }}>Centro de distribución principal para pedidos mayoristas de gran envergadura.</p>
            <button className="btn btn-outline" style={{ width: '100%' }}>Contactar Sucursal</button>
          </div>
          
          <div className="glass-panel" style={{ padding: '40px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '20px' }}>
              <MapPin size={32} color="var(--highlight)" />
              <h3>Sucursal Pudahuel Sur</h3>
            </div>
            <p style={{ color: 'var(--text-muted)', marginBottom: '20px' }}>Punto de venta directo a público e insumos para comerciantes del sector.</p>
            <button className="btn btn-outline" style={{ width: '100%' }}>Contactar Sucursal</button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
