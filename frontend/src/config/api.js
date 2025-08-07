// Configuración de la API
const API_CONFIG = {
  baseURL: 'http://localhost:8000',
  timeout: 30000, // 30 segundos
  headers: {
    'Content-Type': 'application/json'
  }
};

// Función para hacer requests a la API
export const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_CONFIG.baseURL}${endpoint}`;
  
  const config = {
    timeout: API_CONFIG.timeout,
    headers: {
      ...API_CONFIG.headers,
      ...options.headers
    },
    ...options
  };

  // Agregar user-id por defecto (en una app real vendría del contexto de autenticación)
  if (!config.headers['user-id']) {
    config.headers['user-id'] = '1';
  }

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('API Request Error:', error);
    throw error;
  }
};

// Funciones específicas para PQR
export const pqrAPI = {
  // Crear nueva PQR
  crear: async (pqrData) => {
    return await apiRequest('/pqr/', {
      method: 'POST',
      body: JSON.stringify(pqrData)
    });
  },

  // Listar PQRs con filtros opcionales
  listar: async (filtros = {}) => {
    const params = new URLSearchParams();
    
    if (filtros.estado) params.append('estado', filtros.estado);
    if (filtros.tipo) params.append('tipo', filtros.tipo);
    if (filtros.fecha_desde) params.append('fecha_desde', filtros.fecha_desde);
    if (filtros.fecha_hasta) params.append('fecha_hasta', filtros.fecha_hasta);
    if (filtros.limite) params.append('limite', filtros.limite);
    if (filtros.offset) params.append('offset', filtros.offset);

    const queryString = params.toString();
    const endpoint = queryString ? `/pqr/?${queryString}` : '/pqr/';
    
    return await apiRequest(endpoint);
  },

  // Obtener PQR específica
  obtener: async (pqrId) => {
    return await apiRequest(`/pqr/${pqrId}`);
  },

  // Actualizar PQR existente
  actualizar: async (pqrId, pqrData) => {
    return await apiRequest(`/pqr/${pqrId}`, {
      method: 'PUT',
      body: JSON.stringify(pqrData)
    });
  },

  // Eliminar PQR
  eliminar: async (pqrId) => {
    return await apiRequest(`/pqr/${pqrId}`, {
      method: 'DELETE'
    });
  },

  // Responder a una PQR (solo administradores)
  responder: async (pqrId, respuesta) => {
    return await apiRequest(`/pqr/${pqrId}/responder`, {
      method: 'POST',
      body: JSON.stringify({ respuesta })
    });
  },

  // Cerrar PQR (marcar como resuelto)
  cerrar: async (pqrId) => {
    return await apiRequest(`/pqr/${pqrId}/cerrar`, {
      method: 'POST'
    });
  },

  // Obtener estadísticas del dashboard
  dashboard: async () => {
    return await apiRequest('/pqr/dashboard/stats');
  },

  // Obtener configuración del módulo PQR
  configuracion: async () => {
    return await apiRequest('/pqr/config');
  }
};

// Funciones específicas para Evidencias
export const evidenciasAPI = {
  // Crear nueva evidencia
  crear: async (evidenciaData) => {
    return await apiRequest('/evidencias/', {
      method: 'POST',
      body: JSON.stringify(evidenciaData)
    });
  },

  // Listar evidencias
  listar: async () => {
    return await apiRequest('/evidencias/');
  },

  // Obtener evidencia específica
  obtener: async (evidenciaId) => {
    return await apiRequest(`/evidencias/${evidenciaId}`);
  },

  // Actualizar evidencia
  actualizar: async (evidenciaId, evidenciaData) => {
    return await apiRequest(`/evidencias/${evidenciaId}`, {
      method: 'PUT',
      body: JSON.stringify(evidenciaData)
    });
  },

  // Eliminar evidencia
  eliminar: async (evidenciaId) => {
    return await apiRequest(`/evidencias/${evidenciaId}`, {
      method: 'DELETE'
    });
  },

  // Descargar archivo de evidencia
  descargar: async (evidenciaId) => {
    const url = `${API_CONFIG.baseURL}/evidencias/${evidenciaId}/archivo`;
    window.open(url, '_blank');
  }
};

// Funciones para autenticación
export const authAPI = {
  // Login
  login: async (email, password) => {
    return await apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
  },

  // Registro
  register: async (userData) => {
    return await apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
  },

  // Logout
  logout: async () => {
    return await apiRequest('/auth/logout', {
      method: 'POST'
    });
  },

  // Obtener información del usuario actual
  me: async () => {
    return await apiRequest('/auth/me');
  }
};

// Funciones para health check
export const healthAPI = {
  // Health check básico
  ping: async () => {
    return await apiRequest('/health/ping');
  },

  // Health check detallado
  detailed: async () => {
    return await apiRequest('/health/detailed');
  },

  // Estado de las bases de datos
  database: async () => {
    return await apiRequest('/health/database');
  }
};

export default {
  pqr: pqrAPI,
  evidencias: evidenciasAPI,
  auth: authAPI,
  health: healthAPI
};
