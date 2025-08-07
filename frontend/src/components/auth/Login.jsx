import { useState } from 'react';
import './Login.css';

const Login = ({ onLogin, onShowRegister }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
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
    // Aquí normalmente validarías las credenciales con el backend
    console.log('Login attempt:', formData);
    
    // Simulación de login exitoso
    if (formData.email && formData.password) {
      onLogin();
    } else {
      alert('Por favor ingresa tu email y contraseña');
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <div className="logo">
            <span className="logo-icon">🏠</span>
            <h1 className="logo-text">ServiApp</h1>
          </div>
          <p className="login-subtitle">Plataforma de Gestión de Servicios</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="form-input"
              placeholder="Ingresa tu email"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Contraseña</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="form-input"
              placeholder="Ingresa tu contraseña"
              required
            />
          </div>

          <button type="submit" className="login-btn">
            Iniciar Sesión
          </button>
        </form>

        <div className="login-info">
          <h3>¿Qué puedes hacer en ServiApp?</h3>
          <div className="features">
            <div className="feature">
              <span className="feature-icon">📋</span>
              <div>
                <strong>Solicitar Servicios</strong>
                <p>Crea solicitudes detalladas de servicios profesionales</p>
              </div>
            </div>
            <div className="feature">
              <span className="feature-icon">📷</span>
              <div>
                <strong>Gestionar Evidencias</strong>
                <p>Sube y organiza evidencias fotográficas de trabajos</p>
              </div>
            </div>
            <div className="feature">
              <span className="feature-icon">📝</span>
              <div>
                <strong>Enviar PQR</strong>
                <p>Presenta peticiones, quejas y reclamos de manera formal</p>
              </div>
            </div>
          </div>
        </div>

        <div className="demo-credentials">
          <p><strong>Para Demo:</strong></p>
          <p>Email: demo@serviapp.com</p>
          <p>Contraseña: demo123</p>
        </div>

        <div className="register-section">
          <p>¿No tienes cuenta?</p>
          <button onClick={onShowRegister} className="register-link-btn">
            Regístrate aquí
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
