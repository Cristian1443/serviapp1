import { useState, useEffect } from 'react';
import './SolicitudList.css';

const SolicitudList = () => {
  const [solicitudes, setSolicitudes] = useState([]);
  const [filtro, setFiltro] = useState('todas');

  // Simulación de datos - en la aplicación real vendrían del backend
  useEffect(() => {
    const solicitudesMock = [
      {
        id: 1,
        descripcion: 'Reparación de tubería en la cocina. Hay una fuga considerable que necesita atención urgente.',
        direccion: 'Calle 123 #45-67, Bogotá',
        telefono: '3001234567',
        horarioAtencion: 'Lunes a viernes de 8:00 AM a 5:00 PM',
        fecha: '2024-02-15',
        presupuesto: 150000,
        estado: 'pendiente',
        fechaCreacion: '2024-01-28'
      },
      {
        id: 2,
        descripcion: 'Instalación de sistema eléctrico para nueva oficina. Incluye tomas, interruptores y tablero principal.',
        direccion: 'Carrera 50 #30-20, Medellín',
        telefono: '3009876543',
        horarioAtencion: 'Disponible todo el día, fines de semana incluidos',
        fecha: '2024-02-20',
        presupuesto: 500000,
        estado: 'en_proceso',
        fechaCreacion: '2024-01-25'
      },
      {
        id: 3,
        descripcion: 'Limpieza profunda de apartamento de 3 habitaciones después de remodelación.',
        direccion: 'Avenida 68 #40-55, Bogotá',
        telefono: '3005555555',
        horarioAtencion: 'Sábados y domingos únicamente',
        fecha: '2024-02-10',
        presupuesto: 200000,
        estado: 'completado',
        fechaCreacion: '2024-01-20'
      }
    ];
    setSolicitudes(solicitudesMock);
  }, []);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getEstadoColor = (estado) => {
    switch (estado) {
      case 'pendiente': return '#ffc107';
      case 'en_proceso': return '#17a2b8';
      case 'completado': return '#28a745';
      case 'cancelado': return '#dc3545';
      default: return '#6c757d';
    }
  };

  const getEstadoTexto = (estado) => {
    switch (estado) {
      case 'pendiente': return 'Pendiente';
      case 'en_proceso': return 'En Proceso';
      case 'completado': return 'Completado';
      case 'cancelado': return 'Cancelado';
      default: return 'Desconocido';
    }
  };

  const solicitudesFiltradas = solicitudes.filter(solicitud => {
    if (filtro === 'todas') return true;
    return solicitud.estado === filtro;
  });

  return (
    <div className="solicitud-list-container">
      <div className="header-nav">
        <div className="nav-circle"></div>
        <div className="nav-buttons">
          <button className="nav-btn active">Mis Solicitudes</button>
          <button className="nav-btn">Nueva Solicitud</button>
        </div>
        <div className="user-icon">👤</div>
      </div>

      <div className="solicitud-list-content">
        <h2 className="page-title">Mis Solicitudes de Servicio</h2>
        
        <div className="filtros-container">
          <div className="filtros">
            <button 
              className={filtro === 'todas' ? 'filtro-btn active' : 'filtro-btn'}
              onClick={() => setFiltro('todas')}
            >
              Todas ({solicitudes.length})
            </button>
            <button 
              className={filtro === 'pendiente' ? 'filtro-btn active' : 'filtro-btn'}
              onClick={() => setFiltro('pendiente')}
            >
              Pendientes ({solicitudes.filter(s => s.estado === 'pendiente').length})
            </button>
            <button 
              className={filtro === 'en_proceso' ? 'filtro-btn active' : 'filtro-btn'}
              onClick={() => setFiltro('en_proceso')}
            >
              En Proceso ({solicitudes.filter(s => s.estado === 'en_proceso').length})
            </button>
            <button 
              className={filtro === 'completado' ? 'filtro-btn active' : 'filtro-btn'}
              onClick={() => setFiltro('completado')}
            >
              Completadas ({solicitudes.filter(s => s.estado === 'completado').length})
            </button>
          </div>
        </div>
        
        {solicitudesFiltradas.length === 0 ? (
          <div className="no-solicitudes">
            <p>No hay solicitudes {filtro !== 'todas' ? `con estado "${getEstadoTexto(filtro)}"` : ''}</p>
          </div>
        ) : (
          <div className="solicitudes-grid">
            {solicitudesFiltradas.map((solicitud) => (
              <div key={solicitud.id} className="solicitud-card">
                <div className="solicitud-header">
                  <div className="solicitud-info">
                    <h3 className="solicitud-id">Solicitud #{solicitud.id}</h3>
                    <span className="fecha-creacion">
                      Creado: {formatDate(solicitud.fechaCreacion)}
                    </span>
                  </div>
                  <div 
                    className="estado-badge"
                    style={{ backgroundColor: getEstadoColor(solicitud.estado) }}
                  >
                    {getEstadoTexto(solicitud.estado)}
                  </div>
                </div>
                
                <div className="solicitud-body">
                  <div className="descripcion-section">
                    <h4>Descripción del Servicio</h4>
                    <p>{solicitud.descripcion}</p>
                  </div>

                  <div className="detalles-grid">
                    <div className="detalle-item">
                      <strong>📍 Dirección:</strong>
                      <span>{solicitud.direccion}</span>
                    </div>
                    <div className="detalle-item">
                      <strong>📞 Teléfono:</strong>
                      <span>{solicitud.telefono}</span>
                    </div>
                    <div className="detalle-item">
                      <strong>🗓️ Fecha programada:</strong>
                      <span>{formatDate(solicitud.fecha)}</span>
                    </div>
                    <div className="detalle-item">
                      <strong>💰 Presupuesto:</strong>
                      <span className="presupuesto">{formatCurrency(solicitud.presupuesto)}</span>
                    </div>
                  </div>

                  <div className="horario-section">
                    <h4>🕒 Horario de Atención</h4>
                    <p>{solicitud.horarioAtencion}</p>
                  </div>
                </div>

                <div className="solicitud-actions">
                  <button className="action-btn view-btn">Ver Detalles</button>
                  <button className="action-btn edit-btn">Editar</button>
                  {solicitud.estado === 'pendiente' && (
                    <button className="action-btn cancel-btn">Cancelar</button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SolicitudList;
