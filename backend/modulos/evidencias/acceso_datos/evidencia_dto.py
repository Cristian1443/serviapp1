import datetime

class EvidenciaDTO:
    def __init__(self, 
                 id_evidencia: int = None, 
                 id_solicitud: int = None, 
                 id_usuario: int = None, 
                 id_profesional: int = None,
                 tipo_actor: str = None,     
                 archivo_contenido: bytes = None, 
                 descripcion: str = "",
                 estado: str = None,          
                 fecha_subida: datetime.datetime | str = None): 

        self.id_evidencia = id_evidencia
        self.id_solicitud = id_solicitud
        self.id_usuario = id_usuario
        self.id_profesional = id_profesional
        self.tipo_actor = tipo_actor
        self.archivo_contenido = archivo_contenido
        self.descripcion = descripcion
        self.estado = estado
        self.fecha_subida = fecha_subida

    def __str__(self) -> str:
        archivo_info = f"<{len(self.archivo_contenido)} bytes>" if self.archivo_contenido else "None"
        
        return (f"EvidenciaDTO(id_evidencia={self.id_evidencia}, "
                f"id_solicitud={self.id_solicitud}, "
                f"id_usuario={self.id_usuario}, "
                f"id_profesional={self.id_profesional}, "
                f"tipo_actor='{self.tipo_actor}', "
                f"archivo_contenido={archivo_info}, "
                f"descripcion='{self.descripcion}', "
                f"estado='{self.estado}', "
                f"fecha_subida='{self.fecha_subida}')")