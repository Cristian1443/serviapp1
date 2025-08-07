from modulos.pqr.acceso_datos.evidencia_dao import PQRDAOMySQL
from modulos.pqr.acceso_datos.dao_factory import PQRDAOFactory

class MySQLPQRDAOFactory(PQRDAOFactory):
    def crear_dao(self):
        return PQRDAOMySQL()