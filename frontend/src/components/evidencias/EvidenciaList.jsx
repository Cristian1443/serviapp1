import { useState, useEffect } from 'react';
import { evidenciasAPI } from '../../config/api'; // Asegúrate que la ruta sea correcta
import './EvidenciaList.css'; // Usaremos el CSS actualizado

// --- Componente para el Modal de Edición ---
const EditEvidenciaModal = ({ evidencia, onClose, onUpdateSuccess }) => {
  const [formData, setFormData] = useState({
    descripcion: evidencia.descripcion || '',
    estado: evidencia.estado || 'satisfactorio'
  });
  const [isSaving, setIsSaving] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      const dataToUpdate = { ...evidencia, ...formData };
      await evidenciasAPI.actualizar(evidencia.id_evidencia, dataToUpdate);
      alert('Evidencia actualizada correctamente');
      onUpdateSuccess();
    } catch (error) {
      console.error("Error actualizando la evidencia:", error);
      alert("No se pudo actualizar la evidencia.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Editar Evidencia #{evidencia.id_evidencia}</h2>
          <button onClick={onClose} className="close-modal-btn">&times;</button>
        </div>
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label htmlFor="descripcion">Descripción</label>
            <textarea id="descripcion" name="descripcion" value={formData.descripcion} onChange={handleChange} rows="5" />
          </div>
          <div className="form-group">
            <label htmlFor="estado">Estado</label>
            <select id="estado" name="estado" value={formData.estado} onChange={handleChange}>
              <option value="satisfactorio">Satisfactorio</option>
              <option value="no_satisfactorio">No Satisfactorio</option>
            </select>
          </div>
          <div className="modal-footer">
            <button type="button" onClick={onClose} className="cancel-btn">Cancelar</button>
            <button type="submit" className="confirm-btn" disabled={isSaving}>
              {isSaving ? 'Guardando...' : 'Guardar Cambios'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// --- Componente Principal de la Lista de Evidencias ---
const EvidenciaList = () => {
  const [evidencias, setEvidencias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingEvidencia, setEditingEvidencia] = useState(null);
  const [deletingEvidenciaId, setDeletingEvidenciaId] = useState(null);

  const cargarEvidencias = async () => {
    try {
      setLoading(true);
      const data = await evidenciasAPI.listar();
      setEvidencias(Array.isArray(data) ? data : []);
      setError(null);
    } catch (err) {
      console.error('Error cargando evidencias:', err);
      setError('No se pudieron cargar las evidencias. Intenta recargar la página.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarEvidencias();
  }, []);

  const handleConfirmDelete = async () => {
    if (!deletingEvidenciaId) return;
    try {
      await evidenciasAPI.eliminar(deletingEvidenciaId);
      setDeletingEvidenciaId(null);
      await cargarEvidencias();
      alert('Evidencia eliminada correctamente.');
    } catch (err) {
      console.error('Error eliminando evidencia:', err);
      alert('Error al eliminar la evidencia.');
      setDeletingEvidenciaId(null);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Fecha no disponible';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' });
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
        
        {loading && <div className="loading"><p>Cargando evidencias...</p></div>}
        {error && <div className="error"><p>{error}</p><button onClick={cargarEvidencias}>Reintentar</button></div>}
        {!loading && !error && evidencias.length === 0 && <div className="no-evidencias"><p>No hay evidencias guardadas</p></div>}

        {!loading && !error && (
          <div className="evidencias-grid">
            {evidencias.map((evidencia) => (
              <div key={evidencia.id_evidencia} className="evidencia-card">
                <div className="evidencia-header">
                  <h3>Evidencia #{evidencia.id_evidencia}</h3>
                  <span className="fecha-creacion">{formatDate(evidencia.fecha_subida)}</span>
                </div>
                
                {/* --- SECCIÓN CORREGIDA --- */}
                <div className="evidencia-info">
                  <div className="info-item">
                    <span className="info-label">Solicitud:</span>
                    <span className="info-value">#{evidencia.id_solicitud || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Subido por:</span>
                    <span className="info-value">{evidencia.tipo_actor || 'N/A'} #{evidencia.tipo_actor === 'usuario' ? evidencia.id_usuario : evidencia.id_profesional}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Estado:</span>
                    <span className="info-value">
                      <span className={`estado-badge estado-${evidencia.estado}`}>{evidencia.estado || 'N/A'}</span>
                    </span>
                  </div>
                </div>

                <div className="evidencia-descripcion">
                  <strong>Descripción:</strong>
                  <p>{evidencia.descripcion || 'Sin descripción'}</p>
                </div>

                <div className="evidencia-archivo">
                  <img 
                    src={`${evidenciasAPI.baseURL}/evidencias/${evidencia.id_evidencia}/archivo`}
                    alt={`Evidencia ${evidencia.id_evidencia}`}
                    className="evidencia-imagen"
                    onError={(e) => { e.target.style.display = 'none'; }}
                  />
                </div>

                <div className="evidencia-actions">
                  <button className="action-btn edit-btn" onClick={() => setEditingEvidencia(evidencia)}>Editar</button>
                  <button className="action-btn delete-btn" onClick={() => setDeletingEvidenciaId(evidencia.id_evidencia)}>Eliminar</button>
                  <button className="action-btn download-btn" onClick={() => evidenciasAPI.descargar(evidencia.id_evidencia)}>Descargar</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {editingEvidencia && (
        <EditEvidenciaModal
          evidencia={editingEvidencia}
          onClose={() => setEditingEvidencia(null)}
          onUpdateSuccess={() => {
            setEditingEvidencia(null);
            cargarEvidencias();
          }}
        />
      )}

      {deletingEvidenciaId && (
        <div className="modal-overlay">
          <div className="modal-content confirmation-dialog">
            <h3>Confirmar Eliminación</h3>
            <p>¿Estás seguro de que quieres eliminar la evidencia #{deletingEvidenciaId}? Esta acción no se puede deshacer.</p>
            <div className="modal-footer">
              <button onClick={() => setDeletingEvidenciaId(null)} className="cancel-btn">Cancelar</button>
              <button onClick={handleConfirmDelete} className="confirm-btn delete-confirmation-btn">Sí, Eliminar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EvidenciaList;
