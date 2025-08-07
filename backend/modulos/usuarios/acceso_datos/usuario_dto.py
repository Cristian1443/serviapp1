import datetime

class UsuarioDTO:
    def __init__(self,
                 id_usuario: int = None,
                 nombre: str = None,
                 apellido: str = None,
                 correo: str = None,
                 telefono: str = None,
                 direccion: str = None,
                 contrasena: str = None,  
                 fecha_registro: datetime.datetime | str = None):

        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion
        self.contrasena = contrasena  
        self.fecha_registro = fecha_registro

    def __str__(self) -> str:
        return (f"UsuarioDTO(id_usuario={self.id_usuario}, "
                f"nombre='{self.nombre}', "
                f"apellido='{self.apellido}', "
                f"correo='{self.correo}', "
                f"telefono='{self.telefono}', "
                f"direccion='{self.direccion}', "
                f"contrasena='******', "  
                f"fecha_registro='{self.fecha_registro}')")