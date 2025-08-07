from modulos.usuarios.acceso_datos.usuario_dao import UsuarioDAOPostgres
from modulos.usuarios.acceso_datos.dao_factory import UsuarioDAOFactory

class PostgresUsuarioDAOFactory(UsuarioDAOFactory):
    def crear_dao(self):
        return UsuarioDAOPostgres()
