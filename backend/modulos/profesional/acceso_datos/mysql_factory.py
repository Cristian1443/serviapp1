from modulos.profesional.acceso_datos.profesional_dao import ProfesionalDAOMySQL
from modulos.profesional.acceso_datos.dao_factory import ProfesionalDAOFactory

class MySQLProfesionalDAOFactory(ProfesionalDAOFactory):
    def crear_dao(self):
        return ProfesionalDAOMySQL()