from .profesional_dao import ProfesionalDAO # <- Importar la clase unificada

class MySQLProfesionalDAOFactory:
    def crear_dao(self):
        return ProfesionalDAO() # <- Devolver la clase unificada