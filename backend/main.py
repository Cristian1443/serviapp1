from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from datetime import datetime
from config.db_test import test_db_connection


# Importar módulo PQR (sistema nuevo que funciona)
try:
    from modulos.pqr.logica.pqr_service import router as pqr_router
    PQR_AVAILABLE = True
    print("✅ Módulo PQR cargado correctamente")
except ImportError as e:
    print(f"❌ Error importando módulo PQR: {e}")
    PQR_AVAILABLE = False

# Importar módulo Evidencias
try:
    from modulos.evidencias.logica.evidencia_service import router as evidencias_router
    EVIDENCIAS_AVAILABLE = True
    print("✅ Módulo Evidencias cargado correctamente")
except ImportError as e:
    print(f"❌ Error importando módulo Evidencias: {e}")
    EVIDENCIAS_AVAILABLE = False

# Importar módulo Profesionales
try:
    # Se asume que la ruta es 'modulos.profesionales.logica.profesional_service'
    from modulos.profesional.logica.profesional_service import router as profesionales_router
    PROFESIONAL_AVAILABLE = True
    print("✅ Módulo Profesionales cargado correctamente")
except ImportError as e:
    print(f"❌ Error importando módulo Profesionales: {e}")
    PROFESIONAL_AVAILABLE = False   

# Importar módulo Usuarios
try:
    from modulos.usuarios.logica.usuario_service import router as usuario_router
    USUARIOS_AVAILABLE = True
    print("✅ Módulo Usuarios cargado correctamente")
except ImportError as e:
    print(f"❌ Error importando módulo Usuarios: {e}")
    USUARIOS_AVAILABLE = False


# Crear aplicación FastAPI
app = FastAPI(
    title="ServiApp API",
    description="API para la aplicación ServiApp - Gestión de servicios y PQR",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    
    # Procesar request
    response = await call_next(request)
    
    # Calcular tiempo de procesamiento
    process_time = datetime.now() - start_time
    
    # Log básico (en producción usar un logger apropiado)
    print(f"{request.method} {request.url.path} - {response.status_code} - {process_time}")
    
    return response

# Incluir rutas PQR
if PQR_AVAILABLE:
    app.include_router(pqr_router, prefix="/pqr", tags=["PQR"])

# Incluir rutas Evidencias
if EVIDENCIAS_AVAILABLE:
    app.include_router(evidencias_router, prefix="/evidencias", tags=["Evidencias"])

# Incluir rutas Profesionales
if PROFESIONAL_AVAILABLE:
    app.include_router(profesionales_router, prefix="/profesional", tags=["Profesional"])

# Incluir rutas Usuarios
if USUARIOS_AVAILABLE:
    app.include_router(usuario_router, prefix="/usuarios", tags=["Usuarios"])

# Endpoints raíz
@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "¡Bienvenido a ServiApp API!",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/api/health",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api")
async def api_info():
    """Información general de la API"""
    return {
        "api": "ServiApp",
        "version": "1.0.0",
        "modulos": {
            "pqr": "Peticiones, Quejas y Reclamos",
            "evidencias": "Gestión de Evidencias",
            "profesional": "Gestión de Profesionales",
            "usuarios": "Gestión de Usuarios",
            "auth": "Autenticación y autorización",
            "health": "Monitoreo de salud del sistema"
        },
        "endpoints": {
            "pqr": "/pqr",
            "evidencias": "/evidencias",
            "profesional": "/profesional",
            "usuarios": "/usuarios"
        }
    }

# Manejador de errores global
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Error interno del servidor",
            "detail": str(exc) if os.getenv("DEBUG", "false").lower() == "true" else None,
            "status_code": 500,
            "timestamp": datetime.now().isoformat()
        }
    )

# Evento de inicio
@app.on_event("startup")
async def startup_event():
    print("🚀 Iniciando ServiApp API...")
    
    # Confirmar estado de módulos
    if PQR_AVAILABLE:
        print("✅ ServiApp PQR listo para usar")
    else:
        print("⚠️ Módulo PQR no disponible")
    
    if EVIDENCIAS_AVAILABLE:
        print("✅ ServiApp Evidencias listo para usar")
    else:
        print("⚠️ Módulo Evidencias no disponible")
    
    if PROFESIONAL_AVAILABLE:
        print("✅ ServiApp Profesionales listo para usar")
    else:
        print("⚠️ Módulo Profesionales no disponible")

    if USUARIOS_AVAILABLE:
        print("✅ ServiApp Usuarios listo para usar")
    else:
        print("⚠️ Módulo Usuarios no disponible")

    # ⬇️ Agrega esta línea para probar la base de datos
    test_db_connection()

    print("✅ ServiApp API lista en http://localhost:8000")
    print("📚 Documentación disponible en http://localhost:8000/docs")
    
# Evento de apagado
@app.on_event("shutdown")
async def shutdown_event():
    """Limpiar recursos al apagar"""
    print("🔄 Cerrando ServiApp API...")
    print("✅ API cerrada correctamente")

# Función para ejecutar el servidor
def start_server():
    """Iniciar servidor de desarrollo"""
    # Configuración del servidor
    config = {
        'host': '0.0.0.0',
        'port': 8000,
        'debug': True
    }
    
    uvicorn.run(
        "main:app",
        host=config.get('host', '0.0.0.0'),
        port=config.get('port', 8000),
        reload=config.get('debug', True),
        log_level="info"
    )

if __name__ == "__main__":
    start_server()
