from modulos.evidencias.acceso_datos.evidencia_dao import EvidenciaDAOPostgres
from modulos.evidencias.acceso_datos.dao_factory import EvidenciaDAOFactory

class PostgresEvidenciaDAOFactory(EvidenciaDAOFactory):
    def crear_dao(self):
        return EvidenciaDAOPostgres()