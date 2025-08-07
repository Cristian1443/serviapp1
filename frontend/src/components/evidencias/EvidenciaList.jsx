import { useState, useEffect } from 'react';
import { evidenciasAPI } from '../../config/api';
import './EvidenciaList.css';

const EvidenciaList = () => {
  const [evidencias, setEvidencias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Cargar evidencias del backend
  useEffect(() => {
    const cargarEvidencias = async () => {
      try {
        setLoading(true);
        const response = await evidenciasAPI.listar();
        
        // La respuesta puede ser directamente un array o estar dentro de un objeto
        const evidenciasData = Array.isArray(response) ? response : response.evidencias || [];
        
        setEvidencias(evidenciasData);
        setError(null);
      } catch (err) {
        console.error('Error cargando evidencias:', err);
        setError('Error al cargar las evidencias');
        
        // Mostrar datos mock si falla la conexión (opcional)
        const evidenciasMock = [
          {
            id_evidencia: 1,
            id_solicitud: 1,
            id_usuario: 1,
            id_profesional: 1,
            tipo_actor: 'usuario',
            descripcion: 'Evidencia de prueba 1',
            estado: 'satisfactorio',
            fecha_subida: '2024-01-21'
          },
          {
            id_evidencia: 2,
            id_solicitud: 2,
            id_usuario: 1,
            id_profesional: 2,
            tipo_actor: 'profesional',
            descripcion: 'Evidencia de prueba 2',
            estado: 'satisfactorio',
            fecha_subida: '2024-01-26'
          }
        ];
        setEvidencias(evidenciasMock);
      } finally {
        setLoading(false);
      }
    };

    cargarEvidencias();
  }, []);

  // Eliminar evidencia
  const eliminarEvidencia = async (id) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta evidencia?')) {
      try {
        await evidenciasAPI.eliminar(id);
        setEvidencias(evidencias.filter(e => e.id_evidencia !== id));
      } catch (err) {
        console.error('Error eliminando evidencia:', err);
        alert('Error al eliminar la evidencia');
      }
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="evidencia-list-container">
      <div className="header">
        <div className="menu-icon">
          <div className="menu-lines"></div>
          <div className="menu-lines"></div>
          <div className="menu-lines"></div>
        </div>
        <span className="header-title">Evidencias Guardadas</span>
      </div>

      <div className="evidencia-list-content">
        <h2 className="page-title">Mis Evidencias</h2>
        
        {loading ? (
          <div className="loading">
            <p>Cargando evidencias...</p>
          </div>
        ) : error && evidencias.length === 0 ? (
          <div className="error">
            <p>{error}</p>
            <button onClick={() => window.location.reload()}>Reintentar</button>
          </div>
        ) : evidencias.length === 0 ? (
          <div className="no-evidencias">
            <p>No hay evidencias guardadas</p>
          </div>
        ) : (
          <div className="evidencias-grid">
            {evidencias.map((evidencia) => (
              <div key={evidencia.id_evidencia || evidencia.id} className="evidencia-card">
                <div className="evidencia-header">
                  <h3 className="evidencia-id">Evidencia #{evidencia.id_evidencia || evidencia.id}</h3>
                  <span className="fecha-creacion">
                    Creado: {formatDate(evidencia.fecha_subida || evidencia.fechaCreacion)}
                  </span>
                </div>
                
                <div className="evidencia-info">
                  <div className="info-row">
                    <strong>Solicitud:</strong>
                    <span>#{evidencia.id_solicitud || 'N/A'}</span>
                  </div>
                  <div className="info-row">
                    <strong>Usuario:</strong>
                    <span>#{evidencia.id_usuario || 'N/A'}</span>
                  </div>
                  {evidencia.id_profesional && (
                    <div className="info-row">
                      <strong>Profesional:</strong>
                      <span>#{evidencia.id_profesional}</span>
                    </div>
                  )}
                  <div className="info-row">
                    <strong>Tipo:</strong>
                    <span className={`tipo-${evidencia.tipo_actor}`}>
                      {evidencia.tipo_actor || 'N/A'}
                    </span>
                  </div>
                  <div className="info-row">
                    <strong>Estado:</strong>
                    <span className={`estado-${evidencia.estado}`}>
                      {evidencia.estado || 'N/A'}
                    </span>
                  </div>
                </div>

                <div className="evidencia-descripcion">
                  <strong>Descripción:</strong>
                  <p>{evidencia.descripcion || 'Sin descripción'}</p>
                </div>

                <div className="evidencia-archivo">
                  <h4>Archivo adjunto</h4>
                  <div className="archivo-preview">
                    <img 
                      src={`http://localhost:8000/evidencias/${evidencia.id_evidencia || evidencia.id}/archivo`}
                      alt={`Evidencia ${evidencia.id_evidencia || evidencia.id}`}
                      className="evidencia-imagen"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'block';
                      }}
                    />
                    <div className="archivo-no-imagen" style={{display: 'none'}}>
                      📎 Archivo disponible (no es imagen)
                    </div>
                  </div>
                </div>

                <div className="evidencia-actions">
                  <button 
                    className="download-btn"
                    onClick={() => evidenciasAPI.descargar(evidencia.id_evidencia || evidencia.id)}
                    disabled={!evidencia.archivo_contenido}
                  >
                    Descargar
                  </button>
                  <button 
                    className="delete-btn"
                    onClick={() => eliminarEvidencia(evidencia.id_evidencia || evidencia.id)}
                  >
                    Eliminar
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default EvidenciaList;
