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

  const handleSubmit = async (e) => {
    e.preventDefault();

    const requestData = {
      id_usuario: 2, // ⚠️ Poner dinámico si tienes login
      id_profesional: 2, // ⚠️ Selección futura
      id_servicio: 2, // ⚠️ Puedes conectarlo a un dropdown más adelante
      descripcion: formData.descripcion,
      direccion_servicio: formData.direccion,
      telefono_contacto: formData.telefono,
      fecha_servicio: formData.fecha,
      hora_servicio: extraerHoraDesdeHorario(formData.horarioAtencion),
      presupuesto: parseInt(formData.presupuesto),
      estado: 'pendiente'
    };

    try {
      const response = await fetch('http://localhost:8000/solicitudes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      });

      if (response.ok) {
        alert('Solicitud enviada exitosamente');
        // Limpiar el formulario
        setFormData({
          descripcion: '',
          direccion: '',
          telefono: '',
          horarioAtencion: '',
          fecha: '',
          presupuesto: ''
        });
      } else {
        const error = await response.json();
        console.error('Error al enviar solicitud:', error);
        alert('Error al enviar solicitud: ' + error.detail);
      }
    } catch (error) {
      console.error('Error al conectar con el servidor:', error);
      alert('No se pudo enviar la solicitud. Intenta más tarde.');
    }
  };

  // Función para extraer una hora genérica desde horarioAtencion (puedes mejorarla después)
  const extraerHoraDesdeHorario = (horario) => {
    // Por ahora simplemente devuelvo 08:00:00 por defecto
    return '08:00:00';
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
