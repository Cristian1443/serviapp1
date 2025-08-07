import { useState } from 'react';
import { evidenciasAPI } from '../../config/api';
import './EvidenciaForm.css';

const EvidenciaForm = () => {
  // Estado para el diseño original
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFinalizacion, setFechaFinalizacion] = useState('');
  const [imagenes, setImagenes] = useState([]);
  
  // Estado para conexión backend (oculto del usuario)
  const [formData, setFormData] = useState({
    id_solicitud: '13', // Solicitud que existe en la BD
    id_usuario: '1',
    id_profesional: '',
    tipo_actor: 'usuario',
    descripcion: '',
    estado: 'satisfactorio'
  });
  const [loading, setLoading] = useState(false);

  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files);
    const newImages = files.map(file => ({
      id: Date.now() + Math.random(),
      file,
      preview: URL.createObjectURL(file)
    }));
    setImagenes(prev => [...prev, ...newImages]);
  };

  const removeImage = (id) => {
    setImagenes(prev => prev.filter(img => img.id !== id));
  };

  const convertFileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result.split(',')[1]); // Remover el prefijo data:...;base64,
      reader.onerror = error => reject(error);
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (imagenes.length === 0) {
      alert('Por favor selecciona al menos una imagen');
      return;
    }
    
    setLoading(true);
    
    try {
      // Convertir la primera imagen a base64 (el backend espera una sola imagen)
      const primeraImagen = imagenes[0].file;
      const archivoBase64 = await convertFileToBase64(primeraImagen);
      
      const evidenciaData = {
        ...formData,
        descripcion: `Evidencia del ${fechaInicio} al ${fechaFinalizacion}. Imágenes: ${imagenes.length}`,
        archivo_base64: archivoBase64,
        id_solicitud: parseInt(formData.id_solicitud),
        id_usuario: parseInt(formData.id_usuario),
        id_profesional: formData.id_profesional ? parseInt(formData.id_profesional) : null
      };
      
      console.log('Enviando evidencia:', evidenciaData);
      await evidenciasAPI.crear(evidenciaData);
      
      // Reset form
      setFechaInicio('');
      setFechaFinalizacion('');
      setImagenes([]);
      setFormData({
        id_solicitud: '13',
        id_usuario: '1',
        id_profesional: '',
        tipo_actor: 'usuario',
        descripcion: '',
        estado: 'satisfactorio'
      });
      
      alert('Evidencia guardada exitosamente');
    } catch (error) {
      console.error('Error guardando evidencia:', error);
      alert('Error al guardar la evidencia: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="evidencia-container">
      <div className="header">
        <div className="menu-icon">
          <div className="menu-lines"></div>
          <div className="menu-lines"></div>
          <div className="menu-lines"></div>
        </div>
        <span className="header-title">Cuenta</span>
      </div>

      <div className="evidencia-content">
        <h2 className="evidencia-title">Evidencias</h2>
        
        <form onSubmit={handleSubmit} className="evidencia-form">
          <div className="form-group">
            <label className="form-label">*Fecha de inicio</label>
            <input
              type="date"
              value={fechaInicio}
              onChange={(e) => setFechaInicio(e.target.value)}
              className="date-input"
              required
            />
          </div>

          <div className="image-upload-section">
            <div className="image-grid">
              {imagenes.map((imagen) => (
                <div key={imagen.id} className="image-container">
                  <img src={imagen.preview} alt="Evidencia" className="uploaded-image" />
                  <button
                    type="button"
                    onClick={() => removeImage(imagen.id)}
                    className="remove-image-btn"
                  >
                    ×
                  </button>
                </div>
              ))}
              
              {imagenes.length < 6 && (
                <div className="add-image-container">
                  <input
                    type="file"
                    accept="image/*"
                    multiple
                    onChange={handleImageUpload}
                    className="file-input"
                    id="imageUpload"
                  />
                  <label htmlFor="imageUpload" className="add-image-btn">
                    <span className="camera-icon">📷</span>
                    <span className="plus-icon">+</span>
                  </label>
                </div>
              )}
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">*Fecha de finalización</label>
            <input
              type="date"
              value={fechaFinalizacion}
              onChange={(e) => setFechaFinalizacion(e.target.value)}
              className="date-input"
              required
            />
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Guardando...' : 'Guardar'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default EvidenciaForm;
