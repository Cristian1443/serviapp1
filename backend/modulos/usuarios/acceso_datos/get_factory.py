from modulos.usuarios.configuracion.config import cargar_configuracion
from modulos.usuarios.acceso_datos.mysql_factory import MySQLUsuarioDAOFactory
from modulos.usuarios.acceso_datos.postgres_factory import PostgresUsuarioDAOFactory

def obtener_fabrica():
    config = cargar_configuracion()
    if config["db_engine"] == "postgres":
        return PostgresUsuarioDAOFactory()
    return MySQLUsuarioDAOFactory()
