// src/services/authService.js

const API_URL = 'http://localhost:8000'; // La URL de tu backend FastAPI

/**
 * Registra un nuevo usuario estándar.
 * @param {object} userData - Datos del usuario (nombre, apellido, correo, etc.).
 * @returns {Promise<object>} - La respuesta del servidor.
 */
export const registerUser = async (userData) => {
    const response = await fetch(`${API_URL}/usuarios`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    if (!response.ok) {
        // Si la respuesta no es exitosa, lanza un error con el mensaje del backend
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al registrar el usuario.');
    }

    return response.json();
};

/**
 * Registra un nuevo profesional.
 * @param {object} professionalData - Datos del profesional (nombre, profesion, etc.).
 * @returns {Promise<object>} - La respuesta del servidor.
 */
export const registerProfessional = async (professionalData) => {
    const response = await fetch(`${API_URL}/profesionales`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(professionalData),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al registrar el profesional.');
    }

    return response.json();
};