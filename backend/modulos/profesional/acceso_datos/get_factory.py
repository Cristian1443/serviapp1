from modulos.profesional.configuracion.config import cargar_configuracion
from modulos.profesional.acceso_datos.mysql_factory import MySQLProfesionalDAOFactory
from modulos.profesional.acceso_datos.postgres_factory import PostgresProfesionalDAOFactory

def obtener_fabrica():
    config = cargar_configuracion()
    if config["db_engine"] == "postgres":
        return PostgresProfesionalDAOFactory()
    return MySQLProfesionalDAOFactory()
