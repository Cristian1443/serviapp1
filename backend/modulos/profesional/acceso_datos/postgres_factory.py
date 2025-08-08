
from .profesional_dao import ProfesionalDAO

class PostgresProfesionalDAOFactory:
    def crear_dao(self):
        return ProfesionalDAO()