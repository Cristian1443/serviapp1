import json
from fastapi import APIRouter, Request, HTTPException
from modulos.pqr.acceso_datos.get_factory import obtener_fabrica
from modulos.pqr.acceso_datos.evidencia_dto import PQRDTO

dao = obtener_fabrica().crear_dao()
router = APIRouter()

@router.post("/")
async def crear_pqr(req: Request):
    """
    Crea un nuevo registro de PQR.
    Espera un JSON con los datos del PQR.
    """
    data = await req.json()
    
    pqr = PQRDTO(
        id_solicitud=int(data["id_solicitud"]),
        id_usuario=int(data["id_usuario"]),
        id_profesional=int(data["id_profesional"]) if data.get("id_profesional") else None,
        tipo=data["tipo"],
        descripcion=data["descripcion"],
        estado=data.get("estado", "pendiente")
    )
    dao.guardar(pqr)
    return {"mensaje": "PQR almacenado correctamente."}

@router.get("/")
def obtener_pqrs():
    """
    Obtiene una lista de todos los PQRs.
    """
    todos_los_pqrs = dao.obtener_todos()
    resultados = []
    for pqr in todos_los_pqrs:
        datos = pqr.__dict__
        resultados.append(datos)
    return resultados

@router.get("/{id}")
def obtener_pqr(id: int):
    """
    Obtiene un PQR específico por su ID.
    """
    pqr = dao.obtener_por_id(id)
    if not pqr:
        raise HTTPException(status_code=404, detail="PQR no encontrado")
    
    datos = pqr.__dict__
    return datos

@router.put("/{id}")
async def actualizar_pqr(id: int, req: Request):
    """
    Actualiza un PQR existente.
    """
    data = await req.json()

    actualizado = PQRDTO(
        id_pqrs=id,
        id_solicitud=int(data["id_solicitud"]),
        id_usuario=int(data["id_usuario"]),
        id_profesional=int(data["id_profesional"]) if data.get("id_profesional") else None,
        tipo=data["tipo"],
        descripcion=data["descripcion"],
        estado=data["estado"]
    )
    dao.actualizar(actualizado)
    return {"mensaje": "PQR actualizado"}

@router.delete("/{id}")
def eliminar_pqr(id: int):
    """
    Elimina un PQR por su ID.
    """
    pqr = dao.obtener_por_id(id)
    if not pqr:
        raise HTTPException(status_code=404, detail="PQR no encontrado")

    dao.eliminar(id)
    return {"mensaje": "PQR eliminado"}