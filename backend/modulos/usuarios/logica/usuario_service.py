from fastapi import APIRouter, Request, HTTPException, status
from modulos.usuarios.acceso_datos.get_factory import obtener_fabrica
from modulos.usuarios.acceso_datos.usuario_dto import UsuarioDTO

dao = obtener_fabrica().crear_dao()
router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(req: Request):
    """
    Crea un nuevo usuario en la base de datos.
    
    Espera un JSON con los siguientes campos:
    - nombre (str): Requerido
    - apellido (str): Requerido
    - correo (str): Requerido
    - contrasena (str): Requerido
    - direccion (str): Opcional
    - telefono (str): Opcional
    """
    data = await req.json()

    try:
        # Instancia del DTO con los campos corregidos
        nuevo_usuario = UsuarioDTO(
            nombre=data["nombre"],
            apellido=data["apellido"],
            correo=data["correo"],
            contrasena=data["contrasena"],
            direccion=data.get("direccion"), # Campo opcional
            telefono=data.get("telefono")    # Campo opcional
        )
    except KeyError as e:
        # Error si falta un campo requerido
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El campo requerido '{e.args[0]}' está ausente.")
    
    dao.guardar(nuevo_usuario)
    return {"mensaje": "Usuario creado exitosamente"}

@router.get("/")
def obtener_usuarios():
    """
    Retorna una lista con todos los usuarios registrados.
    """
    usuarios = dao.obtener_todos()
    # La respuesta se adapta automáticamente a los campos del DTO
    return [usuario.__dict__ for usuario in usuarios]

@router.get("/{id}")
def obtener_usuario(id: int):
    """
    Retorna un usuario específico por su ID.
    """
    usuario = dao.obtener_por_id(id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    # La respuesta se adapta automáticamente a los campos del DTO
    return usuario.__dict__

@router.put("/{id}")
async def actualizar_usuario(id: int, req: Request):
    """
    Actualiza un usuario existente por su ID.
    
    Espera un JSON con los campos a actualizar.
    """
    data = await req.json()

    # Primero, verificamos que el usuario exista
    if not dao.obtener_por_id(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    try:
        # Creamos el DTO para la actualización con los campos corregidos
        usuario_actualizado = UsuarioDTO(
            id_usuario=id,
            nombre=data["nombre"],
            apellido=data["apellido"],
            correo=data["correo"],
            contrasena=data["contrasena"],
            direccion=data.get("direccion"),
            telefono=data.get("telefono")
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El campo requerido '{e.args[0]}' está ausente.")
    
    dao.actualizar(usuario_actualizado)
    return {"mensaje": "Usuario actualizado correctamente"}

@router.delete("/{id}")
def eliminar_usuario(id: int):
    """
    Elimina permanentemente un usuario de la base de datos por su ID.
    """
    # Verificamos que el usuario exista antes de intentar eliminarlo
    if not dao.obtener_por_id(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    dao.eliminar(id)
    return {"mensaje": "Usuario eliminado permanentemente"}