import datetime

class SolicitudDTO:
    def __init__(self,
                 id_solicitud: int = None,
                 id_usuario: int = None,
                 id_profesional: int = None,
                 id_servicio: int = None,
                 descripcion: str = "",
                 direccion_servicio: str = "",
                 telefono_contacto: str = "",
                 fecha_servicio: datetime.date = None,
                 hora_servicio: datetime.time = None,
                 presupuesto: float = 0.0,
                 estado: str = "pendiente",
                 fecha_creacion: datetime.datetime = None):
        
        self.id_solicitud = id_solicitud
        self.id_usuario = id_usuario
        self.id_profesional = id_profesional
        self.id_servicio = id_servicio
        self.descripcion = descripcion
        self.direccion_servicio = direccion_servicio
        self.telefono_contacto = telefono_contacto
        self.fecha_servicio = fecha_servicio
        self.hora_servicio = hora_servicio
        self.presupuesto = presupuesto
        self.estado = estado
        self.fecha_creacion = fecha_creacion

    def __str__(self) -> str:
        return (f"SolicitudDTO(id_solicitud={self.id_solicitud}, id_usuario={self.id_usuario}, "
                f"id_profesional={self.id_profesional}, id_servicio={self.id_servicio}, "
                f"descripcion='{self.descripcion}', direccion_servicio='{self.direccion_servicio}', "
                f"telefono_contacto='{self.telefono_contacto}', fecha_servicio='{self.fecha_servicio}', "
                f"hora_servicio='{self.hora_servicio}', presupuesto={self.presupuesto}, "
                f"estado='{self.estado}', fecha_creacion='{self.fecha_creacion}')")
