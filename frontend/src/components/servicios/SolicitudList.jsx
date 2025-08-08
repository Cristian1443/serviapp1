import { useState, useEffect } from 'react';
import './SolicitudList.css';

const SolicitudList = () => {
  const [solicitudes, setSolicitudes] = useState([]);
  const [filtro, setFiltro] = useState('todas');

  // Estados para manejar la solicitud seleccionada y el estado de edición y los campos de edición
  const [solicitudSeleccionada, setSolicitudSeleccionada] = useState(null);
  const [editandoSolicitud, setEditandoSolicitud] = useState(null);
  const [nuevaDescripcion, setNuevaDescripcion] = useState('');
  const [nuevoPresupuesto, setNuevoPresupuesto] = useState('');


  // Simulación de datos - en la aplicación real vendrían del backend
  useEffect(() => {
    const fetchSolicitudes = async () => {
      try {
        const usuario_id = localStorage.getItem('usuario_id'); // <-- obtener el id desde localStorage
        const response = await fetch(`http://localhost:8000/solicitudes?usuario_id=${usuario_id}`);
        if (!response.ok) throw new Error('Error al obtener solicitudes');
        const data = await response.json();
        setSolicitudes(data);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchSolicitudes();
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
                  <button
                    className="action-btn view-btn"
                    onClick={() => setSolicitudSeleccionada(solicitud)}
                  >
                    Ver Detalles
                  </button>
                  <button
                    className="action-btn edit-btn"
                    onClick={() => {
                      setEditandoSolicitud(solicitud);
                      setNuevaDescripcion(solicitud.descripcion);
                      setNuevoPresupuesto(solicitud.presupuesto);
                    }}
                  >
                    Editar
                  </button>
                  {solicitud.estado === 'pendiente' && (
                    <button
                      className="action-btn cancel-btn"
                      onClick={async () => {
                        const confirm = window.confirm('¿Estás seguro de cancelar esta solicitud?');
                        if (!confirm) return;

                        try {
                          const response = await fetch(`http://localhost:8000/solicitudes/${solicitud.id}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ ...solicitud, estado: 'cancelado' }),
                          });
                          if (!response.ok) throw new Error('Error al cancelar');
                          const updated = await response.json();
                          setSolicitudes((prev) =>
                            prev.map((s) => (s.id === updated.id ? updated : s))
                          );
                        } catch (error) {
                          console.error('Error:', error);
                        }
                      }}
                    >
                      Cancelar
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      {solicitudSeleccionada && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Detalle de Solicitud #{solicitudSeleccionada.id}</h3>
            <p><strong>Descripción:</strong> {solicitudSeleccionada.descripcion}</p>
            <p><strong>Dirección:</strong> {solicitudSeleccionada.direccion}</p>
            <p><strong>Teléfono:</strong> {solicitudSeleccionada.telefono}</p>
            <p><strong>Fecha:</strong> {formatDate(solicitudSeleccionada.fecha)}</p>
            <p><strong>Hora:</strong> {solicitudSeleccionada.horarioAtencion}</p>
            <p><strong>Presupuesto:</strong> {formatCurrency(solicitudSeleccionada.presupuesto)}</p>
            <p><strong>Estado:</strong> {getEstadoTexto(solicitudSeleccionada.estado)}</p>
            <button onClick={() => setSolicitudSeleccionada(null)}>Cerrar</button>
          </div>
        </div>
      )}
      {editandoSolicitud && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Editar Solicitud #{editandoSolicitud.id}</h3>
            <label>
              Descripción:
              <input
                type="text"
                value={nuevaDescripcion}
                onChange={(e) => setNuevaDescripcion(e.target.value)}
              />
            </label>
            <label>
              Presupuesto:
              <input
                type="number"
                value={nuevoPresupuesto}
                onChange={(e) => setNuevoPresupuesto(e.target.value)}
              />
            </label>
            <button
              onClick={async () => {
                try {
                  const response = await fetch(`http://localhost:8000/solicitudes/${editandoSolicitud.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                      ...editandoSolicitud,
                      descripcion: nuevaDescripcion,
                      presupuesto: parseInt(nuevoPresupuesto),
                    }),
                  });
                  if (!response.ok) throw new Error('Error al editar solicitud');
                  const updated = await response.json();
                  setSolicitudes((prev) =>
                    prev.map((s) => (s.id === updated.id ? updated : s))
                  );
                  setEditandoSolicitud(null);
                } catch (error) {
                  console.error('Error:', error);
                }
              }}
            >
              Guardar Cambios
            </button>
            <button onClick={() => setEditandoSolicitud(null)}>Cancelar</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default SolicitudList;
