import { useState } from 'react';
import './PQRForm.css';
import { pqrAPI } from '../../config/api';

const PQRForm = () => {
  const [formData, setFormData] = useState({
    id_solicitud: '',
    id_usuario: '1', // Usuario por defecto, en producción vendría del contexto de autenticación
    id_profesional: '',
    tipo: 'peticion',
    descripcion: '',
    estado: 'pendiente'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.descripcion.trim() || !formData.id_solicitud.trim() || !formData.id_profesional.trim()) {
      alert('Por favor completa todos los campos obligatorios');
      return;
    }

    try {
      const pqrData = {
        id_solicitud: parseInt(formData.id_solicitud),
        id_usuario: parseInt(formData.id_usuario),
        id_profesional: parseInt(formData.id_profesional),
        tipo: formData.tipo,
        descripcion: formData.descripcion.trim(),
        estado: formData.estado
      };

      const result = await pqrAPI.crear(pqrData);

      if (result.mensaje) {
        // Reset form
        setFormData({
          id_solicitud: '',
          id_usuario: '1',
          id_profesional: '',
          tipo: 'peticion',
          descripcion: '',
          estado: 'pendiente'
        });
        
        alert('PQR enviado exitosamente: ' + result.mensaje);
      } else {
        alert('Error enviando PQR: ' + (result.detail || 'Error desconocido'));
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error de conexión. Asegúrate de que el servidor esté ejecutándose en http://localhost:8000');
    }
  };

  return (
    <div className="pqr-container">
      <div className="header">
        <div className="menu-icon">
          <div className="menu-lines"></div>
          <div className="menu-lines"></div>
          <div className="menu-lines"></div>
        </div>
        <span className="header-title">Cuenta</span>
      </div>

      <div className="pqr-content">
        <h2 className="pqr-title">PQR'S</h2>
        <p className="pqr-subtitle">Peticiones, Quejas y Reclamos</p>
        
        <form onSubmit={handleSubmit} className="pqr-form">
          <div className="form-section">
            <div className="form-group">
              <label className="form-label">ID Solicitud</label>
              <input
                type="number"
                name="id_solicitud"
                value={formData.id_solicitud}
                onChange={handleChange}
                className="form-input"
                placeholder="Ingresa el ID de la solicitud relacionada"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">ID Profesional</label>
              <input
                type="number"
                name="id_profesional"
                value={formData.id_profesional}
                onChange={handleChange}
                className="form-input"
                placeholder="Ingresa el ID del profesional"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Tipo de PQR</label>
              <select
                name="tipo"
                value={formData.tipo}
                onChange={handleChange}
                className="form-input"
                required
              >
                <option value="peticion">📝 Petición</option>
                <option value="queja">😞 Queja</option>
                <option value="sugerencia">💡 Sugerencia</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Descripción</label>
              <textarea
                name="descripcion"
                value={formData.descripcion}
                onChange={handleChange}
                className="form-textarea"
                placeholder="Describe detalladamente tu petición, queja o sugerencia..."
                rows="6"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Estado</label>
              <select
                name="estado"
                value={formData.estado}
                onChange={handleChange}
                className="form-input"
                required
              >
                <option value="pendiente">⏳ Pendiente</option>
                <option value="en_proceso">🔄 En Proceso</option>
                <option value="resuelto">✅ Resuelto</option>
              </select>
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" className="submit-btn">
              Enviar PQR
            </button>
          </div>
        </form>

        <div className="pqr-info">
          <h3>Información sobre PQR</h3>
          <div className="info-grid">
            <div className="info-item">
              <h4>📝 Peticiones</h4>
              <p>Solicita información, servicios o gestiones específicas</p>
            </div>
            <div className="info-item">
              <h4>😞 Quejas</h4>
              <p>Expresa tu insatisfacción por el servicio recibido</p>
            </div>
            <div className="info-item">
              <h4>💡 Sugerencias</h4>
              <p>Comparte ideas para mejorar nuestros servicios</p>
            </div>
          </div>
          
          <div className="response-time">
            <p><strong>⏰ Tiempo de respuesta:</strong> Máximo 15 días hábiles</p>
            <p><strong>📧 Notificación:</strong> Recibirás respuesta por correo electrónico</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PQRForm;
