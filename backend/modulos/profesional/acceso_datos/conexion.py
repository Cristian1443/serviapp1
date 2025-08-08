import json
import pymysql
import psycopg2

class ConexionDB:
    def __init__(self):
        """
        El constructor ahora solo carga la configuración desde el archivo JSON.
        No crea ninguna conexión aquí.
        """
        # Se intenta leer el config.json desde la raíz del proyecto,
        # y si no se encuentra, se busca en la ruta específica del módulo.
        try:
            with open("config.json") as f:
                self._config = json.load(f)
        except FileNotFoundError:
            # Fallback a la ruta original si no se encuentra en la raíz
            with open("modulos/profesional/configuracion/config.json") as f:
                self._config = json.load(f)

        self._motor = self._config.get("db_engine")

    def obtener_conexion(self):
        """
        Este método ahora es el corazón de la clase.
        Crea y devuelve una conexión NUEVA y funcional en cada llamada.
        """
        try:
            if self._motor == "mysql":
                # Crea una nueva conexión MySQL en cada llamada
                return pymysql.connect(
                    host=self._config["host"],
                    port=self._config["port"],
                    user=self._config["user"],
                    password=self._config["password"],
                    database=self._config["database"]
                )
            elif self._motor == "postgres":
                # Crea una nueva conexión PostgreSQL en cada llamada
                return psycopg2.connect(
                    host=self._config["host"],
                    port=self._config["port"],
                    user=self._config["user"],
                    password=self._config["password"],
                    dbname=self._config["database"]  # Ojo: psycopg2 usa 'dbname'
                )
            else:
                raise ValueError(f"Motor de base de datos no soportado: {self._motor}")
        except Exception as e:
            print(f"Error al crear la conexión a la base de datos: {e}")
            raise