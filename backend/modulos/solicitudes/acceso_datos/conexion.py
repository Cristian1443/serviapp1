import json
import pymysql
import psycopg2
from modulos.evidencias.configuracion.config import cargar_configuracion

class ConexionDB:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._crear_conexion()
        return cls._instancia

    def _crear_conexion(self):
        config = cargar_configuracion()
        motor = config["db_engine"]
        self.motor = motor

        if motor == "mysql":
            self.conexion = pymysql.connect(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                database=config["database"]
            )
        elif motor == "postgres":
            self.conexion = psycopg2.connect(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                dbname=config["database"]
            )
        else:
            raise ValueError("Motor de base de datos no soportado")

    def obtener_conexion(self):
        return self.conexion
