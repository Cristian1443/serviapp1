from modulos.pqr.configuracion.config import cargar_configuracion
from modulos.pqr.acceso_datos.mysql_factory import MySQLPQRDAOFactory
from modulos.pqr.acceso_datos.postgres_factory import PostgresPQRDAOFactory

def obtener_fabrica():
    config = cargar_configuracion()
    if config["db_engine"] == "postgres":
        return PostgresPQRDAOFactory()
    return MySQLPQRDAOFactory()