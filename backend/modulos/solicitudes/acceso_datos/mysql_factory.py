from modulos.solicitudes.acceso_datos.solicitud_dao import SolicitudDAOMySQL
from modulos.solicitudes.acceso_datos.solicitud_dao_factory import SolicitudDAOFactory

class MySQLSolicitudDAOFactory(SolicitudDAOFactory):
    def crear_dao(self):
        return SolicitudDAOMySQL()
