from modulos.profesional.acceso_datos.profesional_dao import ProfesionalDAOPostgres
from modulos.profesional.acceso_datos.dao_factory import ProfesionalDAOFactory

class PostgresProfesionalDAOFactory(ProfesionalDAOFactory):
    def crear_dao(self):
        return ProfesionalDAOPostgres()
