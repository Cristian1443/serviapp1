# 🚀 Conexión Frontend - Backend ServiApp PQR

## 📋 Resumen
Este documento explica cómo conectar el frontend de React con el backend de Python para el módulo PQR de ServiApp.

## 🏗️ Arquitectura
```
Frontend (React) ↔ API (FastAPI) ↔ Backend PQR ↔ PostgreSQL + MySQL
```

### **Frontend (React + Vite)**
- Puerto: `http://localhost:5173`
- Formulario PQR conectado a la API
- Lista de PQRs con datos en tiempo real

### **Backend (FastAPI)**
- Puerto: `http://localhost:8000`
- API REST con endpoints para PQR
- Autenticación simulada
- Documentación automática en `/docs`

### **Módulo PQR**
- PostgreSQL: Datos principales
- MySQL: Auditoría y analytics
- DTOs, DAOs y Services organizados

## 🚀 Cómo Ejecutar

### 1. **Configurar Bases de Datos**

#### PostgreSQL
```sql
-- Crear base de datos
CREATE DATABASE serviapp_pqr;

-- Ejecutar script
\i backend/configuracion/ScriptPostgresProductos.sql
```

#### MySQL
```sql
-- Crear base de datos
CREATE DATABASE serviapp_pqr_audit;

-- Ejecutar script
SOURCE backend/configuracion/ScriptMySQLAudit.sql;
```

### 2. **Configurar Backend**

```bash
# Navegar al backend
cd backend

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (opcional)
export PQR_POSTGRES_HOST=localhost
export PQR_POSTGRES_DB=serviapp_pqr
export PQR_MYSQL_HOST=localhost
export PQR_MYSQL_DB=serviapp_pqr_audit

# Ejecutar servidor
python main.py
```

El servidor estará disponible en:
- API: `http://localhost:8000`
- Documentación: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

### 3. **Configurar Frontend**

```bash
# Navegar al frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

La aplicación estará disponible en:
- Frontend: `http://localhost:5173`

## 📡 Endpoints de la API

### **PQR**
- `POST /api/pqr/` - Crear nueva PQR
- `GET /api/pqr/` - Listar PQRs del usuario
- `GET /api/pqr/{id}` - Obtener PQR específica
- `PUT /api/pqr/{id}` - Actualizar PQR
- `POST /api/pqr/{id}/responder` - Responder PQR
- `POST /api/pqr/{id}/cerrar` - Cerrar PQR
- `GET /api/pqr/dashboard/stats` - Estadísticas
- `GET /api/pqr/config` - Configuración

### **Autenticación**
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/logout` - Cerrar sesión
- `GET /api/auth/me` - Info del usuario

### **Health Check**
- `GET /api/health/` - Estado básico
- `GET /api/health/detailed` - Estado detallado
- `GET /api/health/database` - Estado de bases de datos

## 🔧 Configuración

### **Backend**
El archivo `backend/modulos/pqr/configuracion/config.json` contiene:
```json
{
  "database": {
    "postgresql": {
      "host": "localhost",
      "port": 5432,
      "database": "serviapp_pqr"
    },
    "mysql": {
      "host": "localhost", 
      "port": 3306,
      "database": "serviapp_pqr_audit"
    }
  },
  "pqr": {
    "valid_types": ["peticion", "queja", "reclamo"],
    "valid_states": ["en_revision", "respondido", "resuelto", "cerrado"]
  }
}
```

### **Frontend**
El archivo `frontend/src/config/api.js` contiene:
```javascript
const API_CONFIG = {
  baseURL: 'http://localhost:8000/api',
  timeout: 30000
};
```

## 🧪 Probar la Conexión

### 1. **Verificar Backend**
```bash
curl http://localhost:8000/api/health/
```

### 2. **Crear PQR desde Frontend**
1. Ir a `http://localhost:5173`
2. Navegar a la sección PQR
3. Llenar el formulario
4. Enviar

### 3. **Ver PQRs**
1. Ir a la lista de PQRs
2. Verificar que aparezcan los datos

## 🔍 Debugging

### **Errores Comunes**

#### Backend no responde
```bash
# Verificar que el servidor esté ejecutándose
curl http://localhost:8000/

# Verificar logs en la consola del backend
```

#### Error de CORS
- El backend ya tiene configurado CORS para `localhost:5173`
- Si usas otro puerto, agrégalo en `backend/main.py`

#### Error de Base de Datos
```bash
# Verificar estado de las bases de datos
curl http://localhost:8000/api/health/database
```

#### Frontend no conecta
- Verificar que la URL en `frontend/src/config/api.js` sea correcta
- Verificar que el backend esté ejecutándose

## 📊 Monitoreo

### **Logs del Backend**
- Los requests se muestran en la consola
- Formato: `METHOD /path - STATUS_CODE - TIME`

### **Estado de Salud**
```bash
# Estado general
curl http://localhost:8000/api/health/detailed

# Estado de bases de datos
curl http://localhost:8000/api/health/database

# Métricas del sistema
curl http://localhost:8000/api/health/metrics
```

## 🔐 Autenticación

### **Usuarios de Prueba**
```javascript
// Administrador
{
  "email": "admin@serviapp.com",
  "password": "admin123"
}

// Cliente
{
  "email": "cliente@test.com", 
  "password": "cliente123"
}

// Profesional
{
  "email": "profesional@test.com",
  "password": "profesional123"
}
```

### **Headers Requeridos**
Todas las requests a la API PQR requieren:
```
Content-Type: application/json
user-id: [ID_DEL_USUARIO]
```

## 🎯 Próximos Pasos

1. **Implementar autenticación JWT real**
2. **Agregar validación de permisos**
3. **Implementar subida de archivos**
4. **Agregar notificaciones en tiempo real**
5. **Implementar cache Redis**
6. **Agregar tests automatizados**

## 📞 Soporte

Si tienes problemas:
1. Verificar que ambos servidores estén ejecutándose
2. Revisar los logs en las consolas
3. Verificar la conectividad de las bases de datos
4. Probar los endpoints individualmente con curl o Postman

¡Tu aplicación ServiApp PQR está lista para usar! 🎉
