from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modulos.evidencias.logica.evidencia_service import router as evidencias_router
from modulos.solicitudes.logica.solicitud_service import router as solicitud_router
from modulos.pqr.logica.pqr_service import router as pqr_router
from modulos.usuarios.logica.usuario_service import router as usuarios_router
from modulos.profesional.logica.profesional_service import router as profesional_router
app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(evidencias_router, prefix="/evidencias")
app.include_router(pqr_router, prefix="/pqr")
app.include_router(usuarios_router, prefix="/usuarios")
app.include_router(profesional_router, prefix="/profesional")
app.include_router(solicitud_router, prefix="/solicitudes", tags=["Solicitudes"])