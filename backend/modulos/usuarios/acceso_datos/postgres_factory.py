
from .usuario_dao import UsuarioDAO


class PostgresUsuarioDAOFactory:
    def crear_dao(self):
        return UsuarioDAO()