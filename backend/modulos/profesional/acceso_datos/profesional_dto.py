

class ProfesionalDTO:
    def __init__(self,
                 id_profesional: int = None,
                 nombre: str = None,
                 apellido: str = None,
                 correo: str = None,
                 telefono: str = None,
                 contrasena: str = None, 
                 profesion: str = None,
                 habilidades: str = None,
                 zona_trabajo: str = None):

        self.id_profesional = id_profesional
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono
        self.contrasena = contrasena
        self.profesion = profesion
        self.habilidades = habilidades
        self.zona_trabajo = zona_trabajo

    def __str__(self) -> str:
        return (f"ProfesionalDTO(id_profesional={self.id_profesional}, "
                f"nombre='{self.nombre}', "
                f"apellido='{self.apellido}', "
                f"correo='{self.correo}', "
                f"telefono='{self.telefono}', "
                f"contrasena='******', "
                f"profesion='{self.profesion}', "
                f"habilidades='{self.habilidades}', "
                f"zona_trabajo='{self.zona_trabajo}')")