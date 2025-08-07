import json
import base64 # Necesario para decodificar el archivo
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response
from modulos.evidencias.acceso_datos.get_factory import obtener_fabrica
from modulos.evidencias.acceso_datos.evidencia_dto import EvidenciaDTO

dao = obtener_fabrica().crear_dao()
router = APIRouter()

@router.post("/")
async def crear_evidencia(req: Request):
    """
    Crea un nuevo registro de evidencia.
    Espera un JSON con los datos de la evidencia y el contenido del archivo en base64.
    """
    data = await req.json()

    try:
        archivo_bytes = base64.b64decode(data["archivo_base64"])
    except (KeyError, TypeError):
        raise HTTPException(status_code=400, detail="El campo 'archivo_base64' es requerido y debe ser un string base64 válido.")
    
    evidencia = EvidenciaDTO(
        id_solicitud=int(data["id_solicitud"]),
        id_usuario=int(data["id_usuario"]) if data.get("id_usuario") else None,
        id_profesional=int(data["id_profesional"]) if data.get("id_profesional") else None,
        tipo_actor=data["tipo_actor"],
        archivo_contenido=archivo_bytes,
        descripcion=data["descripcion"],
        estado=data["estado"]
    )
    dao.guardar(evidencia)
    return {"mensaje": "Evidencia almacenada correctamente."}

@router.get("/")
def obtener_evidencias():
    """
    Obtiene una lista de todas las evidencias sin el contenido del archivo.
    """
    todas_las_evidencias = dao.obtener_todos()
    resultados = []
    for evidencia in todas_las_evidencias:
        datos = evidencia.__dict__
        del datos['archivo_contenido']
        resultados.append(datos)
    return resultados

@router.get("/{id}")
def obtener_evidencia(id: int):
    """
    Obtiene una evidencia específica por su ID, sin el contenido del archivo.
    """
    evidencia = dao.obtener_por_id(id)
    if not evidencia:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")
    
    datos = evidencia.__dict__
    del datos['archivo_contenido']
    return datos

@router.put("/{id}")
async def actualizar_evidencia(id: int, req: Request):
    """
    Actualiza una evidencia existente.
    """
    data = await req.json()

    archivo_bytes = None
    if "archivo_base64" in data and data["archivo_base64"]:
        try:
            archivo_bytes = base64.b64decode(data["archivo_base64"])
        except (KeyError, TypeError):
            raise HTTPException(status_code=400, detail="El campo 'archivo_base64' debe ser un string base64 válido.")

    actualizado = EvidenciaDTO(
        id_evidencia=id,
        id_solicitud=int(data["id_solicitud"]),
        id_usuario=int(data["id_usuario"]) if data.get("id_usuario") else None,
        id_profesional=int(data["id_profesional"]) if data.get("id_profesional") else None,
        tipo_actor=data["tipo_actor"],
        archivo_contenido=archivo_bytes,
        descripcion=data["descripcion"],
        estado=data["estado"]
    )
    dao.actualizar(actualizado)
    return {"mensaje": "Evidencia actualizada"}

@router.delete("/{id}")
def eliminar_evidencia(id: int):
    """
    Elimina una evidencia por su ID.
    """
    evidencia = dao.obtener_por_id(id)
    if not evidencia:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")

    dao.eliminar(id)
    return {"mensaje": "Evidencia eliminada"}

@router.get("/{id}/archivo")
def obtener_archivo_evidencia(id: int):
    """
    Obtiene el archivo/imagen de una evidencia como respuesta binaria.
    """
    evidencia = dao.obtener_por_id(id)
    if not evidencia:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")
    
    if not evidencia.archivo_contenido:
        raise HTTPException(status_code=404, detail="La evidencia no tiene archivo adjunto")
    
    # Determinar el tipo de contenido basado en los primeros bytes
    content_type = "application/octet-stream"  # Por defecto
    if evidencia.archivo_contenido.startswith(b'\x89PNG'):
        content_type = "image/png"
    elif evidencia.archivo_contenido.startswith(b'\xff\xd8\xff'):
        content_type = "image/jpeg"
    elif evidencia.archivo_contenido.startswith(b'GIF8'):
        content_type = "image/gif"
    elif evidencia.archivo_contenido.startswith(b'%PDF'):
        content_type = "application/pdf"
    
    return Response(
        content=evidencia.archivo_contenido,
        media_type=content_type,
        headers={
            "Content-Disposition": f"inline; filename=evidencia_{id}.{content_type.split('/')[-1]}"
        }
    )