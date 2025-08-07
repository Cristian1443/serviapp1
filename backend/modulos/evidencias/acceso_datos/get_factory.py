from modulos.evidencias.configuracion.config import cargar_configuracion
from modulos.evidencias.acceso_datos.mysql_factory import MySQLEvidenciaDAOFactory
from modulos.evidencias.acceso_datos.postgres_factory import PostgresEvidenciaDAOFactory

def obtener_fabrica():
    config = cargar_configuracion()
    if config["db_engine"] == "postgres":
        return PostgresEvidenciaDAOFactory()
    return MySQLEvidenciaDAOFactory()