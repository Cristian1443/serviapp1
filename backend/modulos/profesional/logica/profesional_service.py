from fastapi import APIRouter, Request, HTTPException, status
from modulos.profesional.acceso_datos.get_factory import obtener_fabrica
from modulos.profesional.acceso_datos.profesional_dto import ProfesionalDTO

# La fábrica debería estar configurada para devolver el ProfesionalDAO
dao = obtener_fabrica().crear_dao()
router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_profesional(req: Request):
    """
    Crea un nuevo profesional en la base de datos.
    """
    data = await req.json()

    try:

        password = data.get("contrasena") or data.get("contraseña")
        if not password:
            # Si no se encuentra con ninguna de las dos claves, se lanza el error.
            raise KeyError("contrasena' o 'contraseña")

        # Instancia del ProfesionalDTO con sus campos correspondientes
        nuevo_profesional = ProfesionalDTO(
            nombre=data["nombre"],
            apellido=data["apellido"],
            correo=data["correo"],
            contrasena=password, # -> CAMBIO: Se usa la contraseña encontrada.
            profesion=data["profesion"],
            habilidades=data.get("habilidades"),
            zona_trabajo=data.get("zona_trabajo"),
            telefono=data.get("telefono")
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El campo requerido '{e.args[0]}' está ausente.")

    dao.guardar(nuevo_profesional)
    return {"mensaje": "Profesional creado exitosamente"}

@router.get("/")
def obtener_profesionales():
    """
    Retorna una lista con todos los profesionales registrados.
    """
    profesionales = dao.obtener_todos()
    return [profesional.__dict__ for profesional in profesionales]

@router.get("/{id}")
def obtener_profesional(id: int):
    """
    Retorna un profesional específico por su ID.
    """
    profesional = dao.obtener_por_id(id)
    if not profesional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesional no encontrado")

    return profesional.__dict__

@router.put("/{id}")
async def actualizar_profesional(id: int, req: Request):
    """
    Actualiza un profesional existente por su ID.
    """
    data = await req.json()

    if not dao.obtener_por_id(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesional no encontrado")

    try:
        # -> CAMBIO: Se busca la contraseña con 'ñ' y sin 'ñ' para ser flexible.
        password = data.get("contrasena") or data.get("contraseña")
        if not password:
            raise KeyError("contrasena' o 'contraseña")

        # Creamos el DTO para la actualización
        profesional_actualizado = ProfesionalDTO(
            id_profesional=id,
            nombre=data["nombre"],
            apellido=data["apellido"],
            correo=data["correo"],
            contrasena=password, # -> CAMBIO: Se usa la contraseña encontrada.
            profesion=data["profesion"],
            habilidades=data.get("habilidades"),
            zona_trabajo=data.get("zona_trabajo"),
            telefono=data.get("telefono")
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El campo requerido '{e.args[0]}' está ausente.")

    dao.actualizar(profesional_actualizado)
    return {"mensaje": "Profesional actualizado correctamente"}

@router.delete("/{id}")
def eliminar_profesional(id: int):
    """
    Elimina permanentemente un profesional de la base de datos por su ID.
    """
    if not dao.obtener_por_id(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesional no encontrado")

    dao.eliminar(id)
    return {"mensaje": "Profesional eliminado permanentemente"}