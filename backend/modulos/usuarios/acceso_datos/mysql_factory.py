from modulos.usuarios.acceso_datos.usuario_dao import UsuarioDAOMySQL
from modulos.usuarios.acceso_datos.dao_factory import UsuarioDAOFactory

class MySQLUsuarioDAOFactory(UsuarioDAOFactory):
    def crear_dao(self):
        return UsuarioDAOMySQL()