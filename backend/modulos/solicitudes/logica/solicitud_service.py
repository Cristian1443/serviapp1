from fastapi import APIRouter, Request, HTTPException
from modulos.solicitudes.acceso_datos.get_factory import obtener_fabrica_solicitud
from modulos.solicitudes.acceso_datos.solicitud_dto import SolicitudDTO

router = APIRouter()
dao = obtener_fabrica_solicitud().crear_dao()


@router.post("/")
async def crear_solicitud(req: Request):
    data = await req.json()

    try:
        solicitud = SolicitudDTO(
            id_usuario=int(data["id_usuario"]),
            id_profesional=int(data["id_profesional"]),
            id_servicio=int(data["id_servicio"]),
            descripcion=data["descripcion"],
            direccion_servicio=data["direccion_servicio"],
            telefono_contacto=data["telefono_contacto"],
            fecha_servicio=data["fecha_servicio"],
            hora_servicio=data["hora_servicio"],
            presupuesto=float(data["presupuesto"]),
            estado=data.get("estado", "pendiente")
        )
        dao.guardar(solicitud)
        return {"mensaje": "Solicitud registrada correctamente."}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear solicitud: {str(e)}")


@router.get("/")
def obtener_solicitudes():
    solicitudes = dao.obtener_todos()
    return [s.__dict__ for s in solicitudes]


@router.get("/{id}")
def obtener_solicitud(id: int):
    solicitud = dao.obtener_por_id(id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud.__dict__


@router.put("/{id}")
async def actualizar_solicitud(id: int, req: Request):
    data = await req.json()

    solicitud = dao.obtener_por_id(id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    try:
        solicitud_actualizada = SolicitudDTO(
            id_solicitud=id,
            id_usuario=int(data["id_usuario"]),
            id_profesional=int(data["id_profesional"]),
            id_servicio=int(data["id_servicio"]),
            descripcion=data["descripcion"],
            direccion_servicio=data["direccion_servicio"],
            telefono_contacto=data["telefono_contacto"],
            fecha_servicio=data["fecha_servicio"],
            hora_servicio=data["hora_servicio"],
            presupuesto=float(data["presupuesto"]),
            estado=data.get("estado", "pendiente")
        )
        dao.actualizar(solicitud_actualizada)
        return {"mensaje": "Solicitud actualizada correctamente"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar solicitud: {str(e)}")


@router.delete("/{id}")
def eliminar_solicitud(id: int):
    solicitud = dao.obtener_por_id(id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    dao.eliminar(id)
    return {"mensaje": "Solicitud eliminada correctamente"}
