
from .usuario_dao import UsuarioDAO

class MySQLUsuarioDAOFactory:
    def crear_dao(self):
        # Devuelve una instancia de la nueva clase DAO
        return UsuarioDAO()