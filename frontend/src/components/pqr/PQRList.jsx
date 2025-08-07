import { useState, useEffect } from 'react';
import './PQRList.css';
import { pqrAPI } from '../../config/api';

const PQRList = () => {
  const [pqrs, setPqrs] = useState([]);
  const [filtro, setFiltro] = useState('todas');
  const [editandoPqr, setEditandoPqr] = useState(null);
  const [formData, setFormData] = useState({});

  // Cargar PQRs desde la API
  useEffect(() => {
    const cargarPQRs = async () => {
      try {
        const result = await pqrAPI.listar();

        if (Array.isArray(result)) {
          setPqrs(result);
        } else if (result.success) {
          setPqrs(result.pqrs || []);
        } else {
          console.error('Error cargando PQRs:', result.error);
          setPqrs([]);
        }
      } catch (error) {
        console.error('Error de conexión:', error);
        setPqrs([]);
      }
    };

    cargarPQRs();
  }, []);

  // Función para eliminar PQR
  const eliminarPQR = async (pqrId) => {
    if (!window.confirm('¿Estás seguro de que deseas eliminar este PQR?')) {
      return;
    }

    try {
      const result = await pqrAPI.eliminar(pqrId);
      
      if (result.mensaje) {
        // Actualizar la lista eliminando el PQR
        setPqrs(pqrs.filter(pqr => pqr.id_pqrs !== pqrId));
        alert('PQR eliminado exitosamente');
      } else {
        alert('Error al eliminar PQR: ' + (result.detail || 'Error desconocido'));
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error de conexión al eliminar PQR');
    }
  };

  // Función para iniciar edición
  const iniciarEdicion = (pqr) => {
    setEditandoPqr(pqr.id_pqrs);
    setFormData({
      id_solicitud: pqr.id_solicitud,
      id_usuario: pqr.id_usuario,
      id_profesional: pqr.id_profesional,
      tipo: pqr.tipo,
      descripcion: pqr.descripcion,
      estado: pqr.estado
    });
  };

  // Función para cancelar edición
  const cancelarEdicion = () => {
    setEditandoPqr(null);
    setFormData({});
  };

  // Función para guardar cambios
  const guardarCambios = async (pqrId) => {
    try {
      const result = await pqrAPI.actualizar(pqrId, formData);
      
      if (result.mensaje) {
        // Actualizar la lista con los nuevos datos
        setPqrs(pqrs.map(pqr => 
          pqr.id_pqrs === pqrId 
            ? { ...pqr, ...formData }
            : pqr
        ));
        setEditandoPqr(null);
        setFormData({});
        alert('PQR actualizado exitosamente');
      } else {
        alert('Error al actualizar PQR: ' + (result.detail || 'Error desconocido'));
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error de conexión al actualizar PQR');
    }
  };

  // Función para manejar cambios en el formulario de edición
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getTipoColor = (tipo) => {
    switch (tipo) {
      case 'peticion': return '#17a2b8';
      case 'queja': return '#ffc107';
      case 'sugerencia': return '#28a745';
      default: return '#6c757d';
    }
  };

  const getTipoTexto = (tipo) => {
    switch (tipo) {
      case 'peticion': return 'Petición';
      case 'queja': return 'Queja';
      case 'sugerencia': return 'Sugerencia';
      default: return 'Desconocido';
    }
  };

  const getEstadoColor = (estado) => {
    switch (estado) {
      case 'pendiente': return '#ffc107';
      case 'en_proceso': return '#17a2b8';
      case 'resuelto': return '#28a745';
      case 'cerrado': return '#6c757d';
      default: return '#6c757d';
    }
  };

  const getEstadoTexto = (estado) => {
    switch (estado) {
      case 'pendiente': return 'Pendiente';
      case 'en_proceso': return 'En Proceso';
      case 'resuelto': return 'Resuelto';
      case 'cerrado': return 'Cerrado';
      default: return 'Desconocido';
    }
  };

  const pqrsFiltradas = pqrs.filter(pqr => {
    if (filtro === 'todas') return true;
    return pqr.estado === filtro;
  });

  return (
    <div className="pqr-list-container">
      <div className="header">
        <div className="menu-icon">
          <div className="menu-lines"></div>
          <div className="menu-lines"></div>
          <div className="menu-lines"></div>
        </div>
        <span className="header-title">Mis PQR</span>
      </div>

      <div className="pqr-list-content">
        <h2 className="page-title">Mis Peticiones, Quejas y Reclamos</h2>
        
        <div className="filtros-container">
          <div className="filtros">
            <button 
              className={filtro === 'todas' ? 'filtro-btn active' : 'filtro-btn'}
              onClick={() => setFiltro('todas')}
            >
              Todas ({pqrs.length})
            </button>
            <button 
              className={filtro === 'pendiente' ? 'filtro-btn active' : 'filtro-btn'}
              onClick={() => setFiltro('pendiente')}
            >
              Pendientes ({pqrs.filter(p => p.estado === 'pendiente').length})
            </button>
            <button 
              className={filtro === 'en_proceso' ? 'filtro-btn active' : 'filtro-btn'}
              onClick={() => setFiltro('en_proceso')}
            >
              En Proceso ({pqrs.filter(p => p.estado === 'en_proceso').length})
            </button>
            <button 
              className={filtro === 'resuelto' ? 'filtro-btn active' : 'filtro-btn'}
              onClick={() => setFiltro('resuelto')}
            >
              Resueltas ({pqrs.filter(p => p.estado === 'resuelto').length})
            </button>
          </div>
        </div>
        
        {pqrsFiltradas.length === 0 ? (
          <div className="no-pqrs">
            <p>No hay PQR {filtro !== 'todas' ? `con estado "${getEstadoTexto(filtro)}"` : ''}</p>
          </div>
        ) : (
          <div className="pqrs-grid">
            {pqrsFiltradas.map((pqr) => (
              <div key={pqr.id_pqrs} className="pqr-card">
                <div className="pqr-header">
                  <div className="pqr-info">
                    <h3 className="pqr-id">PQR #{pqr.id_pqrs}</h3>
                    <span className="fecha-creacion">
                      Creado: {formatDate(pqr.fecha_creacion)}
                    </span>
                  </div>
                  <div className="badges">
                    <div 
                      className="tipo-badge"
                      style={{ backgroundColor: getTipoColor(pqr.tipo) }}
                    >
                      {getTipoTexto(pqr.tipo)}
                    </div>
                    <div 
                      className="estado-badge"
                      style={{ backgroundColor: getEstadoColor(pqr.estado) }}
                    >
                      {getEstadoTexto(pqr.estado)}
                    </div>
                  </div>
                </div>
                
                <div className="pqr-body">
                  {editandoPqr === pqr.id_pqrs ? (
                    // Formulario de edición
                    <div className="edit-form">
                      <div className="form-group">
                        <label>ID Solicitud:</label>
                        <input
                          type="number"
                          name="id_solicitud"
                          value={formData.id_solicitud || ''}
                          onChange={handleChange}
                          className="form-input"
                        />
                      </div>
                      <div className="form-group">
                        <label>ID Profesional:</label>
                        <input
                          type="number"
                          name="id_profesional"
                          value={formData.id_profesional || ''}
                          onChange={handleChange}
                          className="form-input"
                        />
                      </div>
                      <div className="form-group">
                        <label>Tipo:</label>
                        <select
                          name="tipo"
                          value={formData.tipo || ''}
                          onChange={handleChange}
                          className="form-input"
                        >
                          <option value="peticion">📝 Petición</option>
                          <option value="queja">😞 Queja</option>
                          <option value="sugerencia">💡 Sugerencia</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Estado:</label>
                        <select
                          name="estado"
                          value={formData.estado || ''}
                          onChange={handleChange}
                          className="form-input"
                        >
                          <option value="pendiente">⏳ Pendiente</option>
                          <option value="en_proceso">🔄 En Proceso</option>
                          <option value="resuelto">✅ Resuelto</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Descripción:</label>
                        <textarea
                          name="descripcion"
                          value={formData.descripcion || ''}
                          onChange={handleChange}
                          className="form-textarea"
                          rows="4"
                        />
                      </div>
                    </div>
                  ) : (
                    // Vista normal
                    <>
                      <div className="descripcion-section">
                        <h4>📝 Descripción</h4>
                        <p>{pqr.descripcion}</p>
                      </div>

                      <div className="detalles-grid">
                        <div className="detalle-item">
                          <strong>📋 ID Solicitud:</strong>
                          <span>{pqr.id_solicitud}</span>
                        </div>
                        <div className="detalle-item">
                          <strong>👨‍💼 ID Profesional:</strong>
                          <span>{pqr.id_profesional}</span>
                        </div>
                        <div className="detalle-item">
                          <strong>👤 ID Usuario:</strong>
                          <span>{pqr.id_usuario}</span>
                        </div>
                      </div>
                    </>
                  )}

                  {pqr.respuesta && (
                    <div className="respuesta-section">
                      <h4>💬 Respuesta</h4>
                      <div className="respuesta-content">
                        <p>{pqr.respuesta}</p>
                        <span className="fecha-respuesta">
                          Respondido el: {formatDate(pqr.fecha_respuesta)}
                        </span>
                      </div>
                    </div>
                  )}

                  {pqr.estado === 'pendiente' && (
                    <div className="pendiente-section">
                      <p>⏳ Tu PQR está pendiente de revisión. Te notificaremos cuando tengamos una respuesta.</p>
                    </div>
                  )}

                  {pqr.estado === 'en_proceso' && (
                    <div className="proceso-section">
                      <p>🔄 Tu PQR está siendo procesada por nuestro equipo.</p>
                    </div>
                  )}
                </div>

                <div className="pqr-actions">
                  {editandoPqr === pqr.id_pqrs ? (
                    // Botones de edición
                    <>
                      <button 
                        className="action-btn confirm-btn"
                        onClick={() => guardarCambios(pqr.id_pqrs)}
                      >
                        💾 Guardar
                      </button>
                      <button 
                        className="action-btn cancel-btn"
                        onClick={cancelarEdicion}
                      >
                        ❌ Cancelar
                      </button>
                    </>
                  ) : (
                    // Botones normales
                    <>
                      <button 
                        className="action-btn view-btn"
                        onClick={() => iniciarEdicion(pqr)}
                      >
                        ✏️ Editar
                      </button>
                      <button 
                        className="action-btn delete-btn"
                        onClick={() => eliminarPQR(pqr.id_pqrs)}
                        style={{ backgroundColor: '#dc3545' }}
                      >
                        🗑️ Eliminar
                      </button>
                      {pqr.estado === 'en_proceso' && (
                        <button className="action-btn confirm-btn">Marcar como Resuelto</button>
                      )}
                    </>
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

export default PQRList;
