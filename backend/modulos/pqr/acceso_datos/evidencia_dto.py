import datetime

class PQRDTO:
    def __init__(self, 
                 id_pqrs: int = None, 
                 id_solicitud: int = None, 
                 id_usuario: int = None, 
                 id_profesional: int = None,
                 tipo: str = None,  # peticion, queja, sugerencia, etc.
                 descripcion: str = "",
                 estado: str = None,  # pendiente, en_proceso, resuelto, cerrado
                 fecha_creacion: datetime.datetime | str = None): 

        self.id_pqrs = id_pqrs
        self.id_solicitud = id_solicitud
        self.id_usuario = id_usuario
        self.id_profesional = id_profesional
        self.tipo = tipo
        self.descripcion = descripcion
        self.estado = estado
        self.fecha_creacion = fecha_creacion

    def __str__(self) -> str:
        return (f"PQRDTO(id_pqrs={self.id_pqrs}, "
                f"id_solicitud={self.id_solicitud}, "
                f"id_usuario={self.id_usuario}, "
                f"id_profesional={self.id_profesional}, "
                f"tipo='{self.tipo}', "
                f"descripcion='{self.descripcion}', "
                f"estado='{self.estado}', "
                f"fecha_creacion='{self.fecha_creacion}')")