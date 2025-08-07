from modulos.pqr.acceso_datos.evidencia_dao import PQRDAOPostgres
from modulos.pqr.acceso_datos.dao_factory import PQRDAOFactory

class PostgresPQRDAOFactory(PQRDAOFactory):
    def crear_dao(self):
        return PQRDAOPostgres()