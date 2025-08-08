import { useState, useEffect } from 'react';
// Asegúrate de que la ruta a tu API sea correcta
import { evidenciasAPI, solicitudesAPI, usuariosAPI, profesionalesAPI } from '../../config/api';
import './EvidenciaForm.css';

const EvidenciaForm = () => {
  // --- ESTADOS PARA LOS DATOS DE LOS DROPDOWNS ---
  const [solicitudes, setSolicitudes] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [profesionales, setProfesionales] = useState([]);
  
  // --- ESTADO PARA EL FORMULARIO ---
  // Inicializamos todos los campos que el usuario llenará.
  const [formData, setFormData] = useState({
    id_solicitud: '',
    id_usuario: '',
    id_profesional: '', // Puede ser opcional
    tipo_actor: 'usuario', // Valor por defecto
    descripcion: '',
    estado: 'satisfactorio' // Valor por defecto
  });

  // --- ESTADOS ADICIONALES ---
  const [imagenes, setImagenes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dataLoading, setDataLoading] = useState(true); // Estado para la carga inicial de datos
  const [error, setError] = useState(null);

  // --- USEEFFECT PARA CARGAR DATOS INICIALES (SOLICITUDES, USUARIOS, ETC.) ---
  useEffect(() => {
    const cargarDatosParaFormulario = async () => {
      try {
        // Hacemos las llamadas a la API en paralelo para mayor eficiencia
        const [solicitudesData, usuariosData, profesionalesData] = await Promise.all([
          solicitudesAPI.listar(),
          usuariosAPI.listar(),
          profesionalesAPI.listar()
        ]);
        
        setSolicitudes(solicitudesData);
        setUsuarios(usuariosData);
        setProfesionales(profesionalesData);
        setError(null);
      } catch (err) {
        console.error("Error cargando datos para el formulario:", err);
        setError("No se pudieron cargar los datos necesarios para el formulario. Por favor, recarga la página.");
      } finally {
        setDataLoading(false);
      }
    };

    cargarDatosParaFormulario();
  }, []); // El array vacío asegura que se ejecute solo una vez al montar el componente

  // --- MANEJADORES DE EVENTOS ---

  // Un solo manejador para todos los campos de texto y select
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

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
      reader.onload = () => resolve(reader.result.split(',')[1]);
      reader.onerror = error => reject(error);
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (imagenes.length === 0) {
      alert('Por favor, selecciona al menos una imagen como evidencia.');
      return;
    }
    if (!formData.id_solicitud || !formData.tipo_actor || !formData.estado) {
        alert('Por favor, completa todos los campos requeridos (*).');
        return;
    }
    
    setLoading(true);
    
    try {
      const archivoBase64 = await convertFileToBase64(imagenes[0].file);
      
      const evidenciaData = {
        ...formData,
        archivo_base64: archivoBase64,
        // Aseguramos que los IDs se envíen como números
        id_solicitud: parseInt(formData.id_solicitud),
        id_usuario: formData.id_usuario ? parseInt(formData.id_usuario) : null,
        id_profesional: formData.id_profesional ? parseInt(formData.id_profesional) : null
      };
      
      console.log('Enviando evidencia:', evidenciaData);
      await evidenciasAPI.crear(evidenciaData);
      
      alert('Evidencia guardada exitosamente');
      
      // Limpiar formulario después de enviar
      setImagenes([]);
      setFormData({
        id_solicitud: '',
        id_usuario: '',
        id_profesional: '',
        tipo_actor: 'usuario',
        descripcion: '',
        estado: 'satisfactorio'
      });

    } catch (error) {
      console.error('Error guardando evidencia:', error);
      alert('Error al guardar la evidencia: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // Si los datos iniciales están cargando, muestra un mensaje
  if (dataLoading) {
    return <div className="evidencia-container"><p style={{textAlign: 'center', padding: '20px'}}>Cargando datos del formulario...</p></div>;
  }

  // Si hubo un error al cargar datos, muestra el error
  if (error) {
    return <div className="evidencia-container"><p style={{textAlign: 'center', color: 'red', padding: '20px'}}>{error}</p></div>;
  }

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
        <h2 className="evidencia-title">Registrar Evidencia de Servicio</h2>
        
        <form onSubmit={handleSubmit} className="evidencia-form">
          
          {/* --- SELECT PARA SOLICITUD --- */}
          <div className="form-group">
            <label htmlFor="id_solicitud" className="form-label">* Solicitud Asociada</label>
            <select id="id_solicitud" name="id_solicitud" value={formData.id_solicitud} onChange={handleChange} className="form-select" required>
              <option value="">-- Seleccione una solicitud --</option>
              {solicitudes.map(sol => (
                <option key={sol.id_solicitud} value={sol.id_solicitud}>
                  ID: {sol.id_solicitud} - {sol.descripcion.substring(0, 50)}...
                </option>
              ))}
            </select>
          </div>

          {/* --- SELECT PARA TIPO DE ACTOR --- */}
          <div className="form-group">
            <label htmlFor="tipo_actor" className="form-label">* Evidencia subida por</label>
            <select id="tipo_actor" name="tipo_actor" value={formData.tipo_actor} onChange={handleChange} className="form-select" required>
              <option value="usuario">Usuario</option>
              <option value="profesional">Profesional</option>
            </select>
          </div>

          {/* --- SELECTS CONDICIONALES PARA USUARIO O PROFESIONAL --- */}
          {formData.tipo_actor === 'usuario' && (
            <div className="form-group">
              <label htmlFor="id_usuario" className="form-label">* Usuario que sube la evidencia</label>
              <select id="id_usuario" name="id_usuario" value={formData.id_usuario} onChange={handleChange} className="form-select" required>
                <option value="">-- Seleccione un usuario --</option>
                {usuarios.map(u => (
                  <option key={u.id_usuario} value={u.id_usuario}>{u.nombre} {u.apellido}</option>
                ))}
              </select>
            </div>
          )}

          {formData.tipo_actor === 'profesional' && (
            <div className="form-group">
              <label htmlFor="id_profesional" className="form-label">* Profesional que sube la evidencia</label>
              <select id="id_profesional" name="id_profesional" value={formData.id_profesional} onChange={handleChange} className="form-select" required>
                <option value="">-- Seleccione un profesional --</option>
                {profesionales.map(p => (
                  <option key={p.id_profesional} value={p.id_profesional}>{p.nombre} {p.apellido}</option>
                ))}
              </select>
            </div>
          )}
          
          {/* --- CAMPO DE DESCRIPCIÓN --- */}
          <div className="form-group">
            <label htmlFor="descripcion" className="form-label">Descripción (Opcional)</label>
            <textarea id="descripcion" name="descripcion" value={formData.descripcion} onChange={handleChange} className="form-textarea" rows="4" placeholder="Añada detalles sobre la evidencia..."></textarea>
          </div>

          {/* --- SECCIÓN PARA SUBIR IMÁGENES --- */}
          <div className="form-group">
            <label className="form-label">* Archivo de Evidencia</label>
            <div className="image-upload-section">
              <div className="image-grid">
                {imagenes.map((imagen) => (
                  <div key={imagen.id} className="image-container">
                    <img src={imagen.preview} alt="Evidencia" className="uploaded-image" />
                    <button type="button" onClick={() => removeImage(imagen.id)} className="remove-image-btn">×</button>
                  </div>
                ))}
                {imagenes.length < 1 && ( // Permitimos solo una imagen para simplificar
                  <div className="add-image-container">
                    <input type="file" accept="image/*" onChange={handleImageUpload} className="file-input" id="imageUpload" />
                    <label htmlFor="imageUpload" className="add-image-btn">
                      <span className="camera-icon">📷</span>
                      <span className="plus-icon">+</span>
                    </label>
                  </div>
                )}
              </div>
            </div>
          </div>
          
          {/* --- SELECT PARA ESTADO DE LA EVIDENCIA --- */}
          <div className="form-group">
            <label htmlFor="estado" className="form-label">* Estado del trabajo</label>
            <select id="estado" name="estado" value={formData.estado} onChange={handleChange} className="form-select" required>
              <option value="satisfactorio">Satisfactorio</option>
              <option value="no_satisfactorio">No Satisfactorio</option>
            </select>
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Guardando...' : 'Guardar Evidencia'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default EvidenciaForm;
