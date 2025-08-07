import { useState } from 'react';
import './RoleSelection.css';

const RoleSelection = ({ onRoleSelect }) => {
  return (
    <div className="role-selection-container">
      <div className="role-selection-card">
        <h2 className="role-title">¿Cuál será tu rol?</h2>
        
        <div className="role-buttons">
          <button 
            className="role-btn client-btn"
            onClick={() => onRoleSelect('cliente')}
          >
            Cliente
          </button>
          
          <button 
            className="role-btn professional-btn"
            onClick={() => onRoleSelect('profesional')}
          >
            Profesional
          </button>
        </div>
        
        <div className="role-info">
          <div className="info-section">
            <h3>👤 Cliente</h3>
            <p>Solicita servicios profesionales, gestiona evidencias y envía PQR</p>
          </div>
          
          <div className="info-section">
            <h3>🔧 Profesional</h3>
            <p>Ofrece servicios, gestiona solicitudes y atiende clientes</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RoleSelection;
