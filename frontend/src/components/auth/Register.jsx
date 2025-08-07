import { useState } from 'react';
import './Register.css';
// -> CAMBIO: Importamos las funciones para llamar a la API
import { registerUser, registerProfessional } from '../../services/authService';

const Register = ({ userType, onRegister, onBack }) => {
  // -> CAMBIO: Separamos nombre y apellido en el estado inicial
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    correo: '',
    direccion: '',
    telefono: '',
    profesion: '',
    habilidades: '', // Nuevo campo para profesionales
    zona_trabajo: '', // Nuevo campo para profesionales
    contrasena: ''
  });

  // -> CAMBIO: Nuevos estados para manejar mensajes de éxito y error
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // -> CAMBIO: La función handleSubmit ahora es asíncrona y llama a la API
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Limpiamos errores anteriores
    setSuccess(null);

    try {
      let response;
      // Usamos el prop 'userType' para decidir a qué endpoint llamar
      if (userType === 'cliente') {
        response = await registerUser({
          nombre: formData.nombre,
          apellido: formData.apellido,
          correo: formData.correo,
          direccion: formData.direccion,
          telefono: formData.telefono,
          contrasena: formData.contrasena,
        });
      } else if (userType === 'profesional') {
        response = await registerProfessional({
          nombre: formData.nombre,
          apellido: formData.apellido,
          correo: formData.correo,
          telefono: formData.telefono,
          profesion: formData.profesion,
          habilidades: formData.habilidades,
          zona_trabajo: formData.zona_trabajo,
          contrasena: formData.contrasena,
        });
      } else {
        throw new Error("Tipo de usuario no válido.");
      }

      setSuccess(response.mensaje || '¡Cuenta creada exitosamente!');
      // Opcional: puedes llamar a onRegister si necesitas hacer algo en el componente padre
      // onRegister(formData);

    } catch (err) {
      // Capturamos y mostramos el error que viene del backend
      setError(err.message);
    }
  };

  const isClient = userType === 'cliente';

  return (
    <div className="register-container">
      <div className="register-card">
        <div className="register-header">
          <button onClick={onBack} className="back-btn">
            ← Volver
          </button>
          <h1 className="register-title">Regístrate</h1>
          <div className="user-type-indicator">
            {isClient ? '👤 Cliente' : '🔧 Profesional'}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="register-form">
          <div className="form-section">
            {/* -> CAMBIO: Dos campos separados para nombre y apellido */}
            <div className="form-group">
              <input type="text" name="nombre" value={formData.nombre} onChange={handleChange} className="form-input" placeholder="Nombre" required />
            </div>
            <div className="form-group">
              <input type="text" name="apellido" value={formData.apellido} onChange={handleChange} className="form-input" placeholder="Apellidos" required />
            </div>

            <div className="form-group">
              <input type="email" name="correo" value={formData.correo} onChange={handleChange} className="form-input" placeholder="Correo" required />
            </div>
            
            {/* -> CAMBIO: El campo de dirección ahora solo es para clientes */}
            {isClient && (
                <div className="form-group">
                    <input type="text" name="direccion" value={formData.direccion} onChange={handleChange} className="form-input" placeholder="Dirección" required />
                </div>
            )}
            
            <div className="form-group">
              <input type="tel" name="telefono" value={formData.telefono} onChange={handleChange} className="form-input" placeholder="Teléfono" required />
            </div>

            {!isClient && (
              <>
                <div className="form-group">
                  <input type="text" name="profesion" value={formData.profesion} onChange={handleChange} className="form-input" placeholder="Profesión" required />
                </div>
                {/* -> CAMBIO: Nuevos campos para profesionales */}
                <div className="form-group">
                  <input type="text" name="habilidades" value={formData.habilidades} onChange={handleChange} className="form-input" placeholder="Habilidades (ej: plomería, diseño)" />
                </div>
                <div className="form-group">
                  <input type="text" name="zona_trabajo" value={formData.zona_trabajo} onChange={handleChange} className="form-input" placeholder="Zona de Trabajo" />
                </div>
              </>
            )}

            <div className="form-group">
              <input type="password" name="contrasena" value={formData.contrasena} onChange={handleChange} className="form-input" placeholder="Contraseña" required />
            </div>
          </div>

          <button type="submit" className="create-account-btn">
            Crear cuenta
          </button>

          {/* -> CAMBIO: Mostramos mensajes de éxito o error */}
          {error && <p className="error-message">{error}</p>}
          {success && <p className="success-message">{success}</p>}
        </form>

        {/* La sección de beneficios se mantiene igual */}
        <div className="register-info">
          {/* ... tu código de beneficios ... */}
        </div>
      </div>
    </div>
  );
};

export default Register;