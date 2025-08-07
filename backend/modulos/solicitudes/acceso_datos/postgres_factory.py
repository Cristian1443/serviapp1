from modulos.solicitudes.acceso_datos.solicitud_dao import SolicitudDAOPostgres
from modulos.solicitudes.acceso_datos.solicitud_dao_factory import SolicitudDAOFactory

class PostgresSolicitudDAOFactory(SolicitudDAOFactory):
    def crear_dao(self):
        return SolicitudDAOPostgres()
