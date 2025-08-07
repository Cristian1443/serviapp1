import { useState } from 'react';
import './SolicitudForm.css';

const SolicitudForm = () => {
  const [formData, setFormData] = useState({
    descripcion: '',
    direccion: '',
    telefono: '',
    horarioAtencion: '',
    fecha: '',
    presupuesto: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Solicitud de servicio:', formData);
    // Aquí enviarías los datos al backend
    
    // Reset form
    setFormData({
      descripcion: '',
      direccion: '',
      telefono: '',
      horarioAtencion: '',
      fecha: '',
      presupuesto: ''
    });
    
    alert('Solicitud enviada exitosamente');
  };

  return (
    <div className="solicitud-container">
      <div className="header-nav">
        <div className="nav-circle"></div>
        <div className="nav-buttons">
          <button className="nav-btn active">Solicitudes</button>
          <button className="nav-btn">Evidencias</button>
          <button className="nav-btn">PQR</button>
        </div>
        <div className="user-icon">👤</div>
      </div>

      <div className="solicitud-content">
        <h2 className="form-title">Detalle de la solicitud</h2>
        
        <form onSubmit={handleSubmit} className="solicitud-form">
          <div className="form-group">
            <label className="form-label">*Descripción</label>
            <textarea
              name="descripcion"
              value={formData.descripcion}
              onChange={handleChange}
              className="form-textarea"
              placeholder="Describe el servicio que necesitas..."
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">*Dirección</label>
            <input
              type="text"
              name="direccion"
              value={formData.direccion}
              onChange={handleChange}
              className="form-input"
              placeholder="Ingresa la dirección completa"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">*Teléfono</label>
            <input
              type="tel"
              name="telefono"
              value={formData.telefono}
              onChange={handleChange}
              className="form-input"
              placeholder="Número de contacto"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">*Horario de atención</label>
            <textarea
              name="horarioAtencion"
              value={formData.horarioAtencion}
              onChange={handleChange}
              className="form-textarea"
              placeholder="Especifica tu disponibilidad horaria"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">*Fecha</label>
            <div className="date-input-container">
              <input
                type="date"
                name="fecha"
                value={formData.fecha}
                onChange={handleChange}
                className="form-input date-input"
                required
              />
              <span className="calendar-icon">📅</span>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">*Presupuesto</label>
            <input
              type="number"
              name="presupuesto"
              value={formData.presupuesto}
              onChange={handleChange}
              className="form-input"
              placeholder="Presupuesto estimado"
              min="0"
              step="0.01"
              required
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="submit-btn">
              Enviar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SolicitudForm;
