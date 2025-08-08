# .../acceso_datos/conexion.py

import json
import pymysql
import psycopg2

class ConexionDB:
    def __init__(self):
        """
        El constructor ahora solo carga la configuración desde el archivo JSON.
        No crea ninguna conexión aquí.
        """
        # -> CAMBIO: La ruta al config.json ahora es relativa a la raíz del proyecto.
        #    Ajusta esta ruta si es necesario. Puede ser mejor usar una ruta absoluta o variables de entorno.
        try:
            with open("config.json") as f:
                self._config = json.load(f)
        except FileNotFoundError:
            # Fallback por si el archivo está en la ubicación original
            with open("modulos/usuarios/configuracion/config.json") as f:
                self._config = json.load(f)

        self._motor = self._config.get("db_engine")

    def obtener_conexion(self):
        """
        Este método ahora es el corazón de la clase.
        Crea y devuelve una conexión NUEVA y funcional en cada llamada.
        """
        try:
            if self._motor == "mysql":
                # -> CAMBIO: Crea una nueva conexión en cada llamada
                return pymysql.connect(
                    host=self._config["host"],
                    port=self._config["port"],
                    user=self._config["user"],
                    password=self._config["password"],
                    database=self._config["database"]
                )
            elif self._motor == "postgres":
                # -> CAMBIO: Crea una nueva conexión en cada llamada
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