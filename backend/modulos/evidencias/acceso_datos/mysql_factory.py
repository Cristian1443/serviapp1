from modulos.evidencias.acceso_datos.evidencia_dao import EvidenciaDAOMySQL
from modulos.evidencias.acceso_datos.dao_factory import EvidenciaDAOFactory

class MySQLEvidenciaDAOFactory(EvidenciaDAOFactory):
    def crear_dao(self):
        return EvidenciaDAOMySQL()