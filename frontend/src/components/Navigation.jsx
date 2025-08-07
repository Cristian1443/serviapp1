import { useState } from 'react';
import './Navigation.css';

// Importar todos los componentes
import EvidenciaForm from './evidencias/EvidenciaForm';
import EvidenciaList from './evidencias/EvidenciaList';
import SolicitudForm from './servicios/SolicitudForm';
import SolicitudList from './servicios/SolicitudList';
import PQRForm from './pqr/PQRForm';
import PQRList from './pqr/PQRList';
import Login from './auth/Login';
import RoleSelection from './auth/RoleSelection';
import Register from './auth/Register';

const Navigation = () => {
  const [currentView, setCurrentView] = useState('login');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userType, setUserType] = useState(null);
  const [selectedRole, setSelectedRole] = useState(null);

  const handleLogin = () => {
    setIsAuthenticated(true);
    setCurrentView('solicitudes');
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUserType(null);
    setSelectedRole(null);
    setCurrentView('login');
  };

  const handleShowRegister = () => {
    setCurrentView('role-selection');
  };

  const handleRoleSelect = (role) => {
    setSelectedRole(role);
    setCurrentView('register');
  };

  const handleRegister = (userData) => {
    setUserType(selectedRole);
    setIsAuthenticated(true);
    setCurrentView('solicitudes');
  };

  const handleBackToLogin = () => {
    setCurrentView('login');
    setSelectedRole(null);
  };

  const handleBackToRoleSelection = () => {
    setCurrentView('role-selection');
    setSelectedRole(null);
  };

  // Pantallas de autenticación
  if (!isAuthenticated) {
    switch (currentView) {
      case 'role-selection':
        return <RoleSelection onRoleSelect={handleRoleSelect} />;
      case 'register':
        return (
          <Register 
            userType={selectedRole}
            onRegister={handleRegister}
            onBack={handleBackToRoleSelection}
          />
        );
      default:
        return <Login onLogin={handleLogin} onShowRegister={handleShowRegister} />;
    }
  }

  const renderCurrentView = () => {
    switch (currentView) {
      case 'evidencias':
        return <EvidenciaForm />;
      case 'evidencias-list':
        return <EvidenciaList />;
      case 'solicitudes':
        return <SolicitudForm />;
      case 'solicitudes-list':
        return <SolicitudList />;
      case 'pqr':
        return <PQRForm />;
      case 'pqr-list':
        return <PQRList />;
      default:
        return <SolicitudForm />;
    }
  };

  return (
    <div className="app-container">
      <nav className="main-nav">
        <div className="nav-header">
          <div className="logo">
            <span className="logo-icon">🏠</span>
            <span className="logo-text">ServiApp</span>
          </div>
          <button onClick={handleLogout} className="logout-btn">
            Cerrar Sesión
          </button>
        </div>
        
        <div className="nav-menu">
          <div className="nav-section">
            <h3>📋 Solicitudes</h3>
            <button 
              className={currentView === 'solicitudes' ? 'nav-item active' : 'nav-item'}
              onClick={() => setCurrentView('solicitudes')}
            >
              Nueva Solicitud
            </button>
            <button 
              className={currentView === 'solicitudes-list' ? 'nav-item active' : 'nav-item'}
              onClick={() => setCurrentView('solicitudes-list')}
            >
              Mis Solicitudes
            </button>
          </div>

          <div className="nav-section">
            <h3>📷 Evidencias</h3>
            <button 
              className={currentView === 'evidencias' ? 'nav-item active' : 'nav-item'}
              onClick={() => setCurrentView('evidencias')}
            >
              Cargar Evidencias
            </button>
            <button 
              className={currentView === 'evidencias-list' ? 'nav-item active' : 'nav-item'}
              onClick={() => setCurrentView('evidencias-list')}
            >
              Ver Evidencias
            </button>
          </div>

          <div className="nav-section">
            <h3>📝 PQR</h3>
            <button 
              className={currentView === 'pqr' ? 'nav-item active' : 'nav-item'}
              onClick={() => setCurrentView('pqr')}
            >
              Nueva PQR
            </button>
            <button 
              className={currentView === 'pqr-list' ? 'nav-item active' : 'nav-item'}
              onClick={() => setCurrentView('pqr-list')}
            >
              Mis PQR
            </button>
          </div>
        </div>
      </nav>

      <main className="main-content">
        {renderCurrentView()}
      </main>
    </div>
  );
};

export default Navigation;
