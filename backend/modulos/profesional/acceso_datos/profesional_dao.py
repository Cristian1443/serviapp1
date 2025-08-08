# Se asume que la ruta al DTO y a la conexión es similar
from modulos.profesional.acceso_datos.profesional_dto import ProfesionalDTO
from modulos.profesional.acceso_datos.conexion import ConexionDB

# --- SE ELIMINA LA CONEXIÓN GLOBAL ---

class ProfesionalDAO:
    """
    DAO unificado y seguro para la tabla 'profesionales'.
    Gestiona la conexión y las transacciones de forma segura para cada operación.
    """
    def guardar(self, profesional_dto: ProfesionalDTO):
        """
        Guarda un nuevo profesional de forma segura.
        """
        conn = None
        try:
            conn = ConexionDB().obtener_conexion()
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO profesionales (nombre, apellido, correo, telefono, contrasena, profesion, habilidades, zona_trabajo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    profesional_dto.nombre, profesional_dto.apellido, profesional_dto.correo,
                    profesional_dto.telefono, profesional_dto.contrasena, profesional_dto.profesion,
                    profesional_dto.habilidades, profesional_dto.zona_trabajo
                )
                cursor.execute(sql, valores)
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al guardar profesional: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def obtener_todos(self):
        """
        Obtiene todos los profesionales de forma segura.
        """
        conn = None
        try:
            conn = ConexionDB().obtener_conexion()
            with conn.cursor() as cursor:
                sql = "SELECT id_profesional, nombre, apellido, correo, telefono, contrasena, profesion, habilidades, zona_trabajo FROM profesionales"
                cursor.execute(sql)
                rows = cursor.fetchall()
            
            profesionales = [
                ProfesionalDTO(
                    id_profesional=row[0], nombre=row[1], apellido=row[2], correo=row[3], telefono=row[4],
                    contrasena=row[5], profesion=row[6], habilidades=row[7], zona_trabajo=row[8]
                ) for row in rows
            ]
            return profesionales
        except Exception as e:
            print(f"Error al obtener todos los profesionales: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_profesional: int):
        """
        Obtiene un profesional por ID de forma segura.
        """
        conn = None
        try:
            conn = ConexionDB().obtener_conexion()
            with conn.cursor() as cursor:
                sql = "SELECT id_profesional, nombre, apellido, correo, telefono, contrasena, profesion, habilidades, zona_trabajo FROM profesionales WHERE id_profesional = %s"
                cursor.execute(sql, (id_profesional,))
                row = cursor.fetchone()

            if row:
                return ProfesionalDTO(
                    id_profesional=row[0], nombre=row[1], apellido=row[2], correo=row[3], telefono=row[4],
                    contrasena=row[5], profesion=row[6], habilidades=row[7], zona_trabajo=row[8]
                )
            return None
        except Exception as e:
            print(f"Error al obtener profesional por ID: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def actualizar(self, profesional_dto: ProfesionalDTO):
        """
        Actualiza un profesional de forma segura.
        """
        conn = None
        try:
            conn = ConexionDB().obtener_conexion()
            with conn.cursor() as cursor:
                sql = """
                    UPDATE profesionales SET
                        nombre = %s, apellido = %s, correo = %s, telefono = %s, contrasena = %s,
                        profesion = %s, habilidades = %s, zona_trabajo = %s
                    WHERE id_profesional = %s
                """
                valores = (
                    profesional_dto.nombre, profesional_dto.apellido, profesional_dto.correo,
                    profesional_dto.telefono, profesional_dto.contrasena, profesional_dto.profesion,
                    profesional_dto.habilidades, profesional_dto.zona_trabajo,
                    profesional_dto.id_profesional
                )
                cursor.execute(sql, valores)
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al actualizar profesional: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def eliminar(self, id_profesional: int):
        """
        Elimina un profesional de forma segura.
        """
        conn = None
        try:
            conn = ConexionDB().obtener_conexion()
            with conn.cursor() as cursor:
                sql = "DELETE FROM profesionales WHERE id_profesional = %s"
                cursor.execute(sql, (id_profesional,))
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al eliminar profesional: {e}")
            raise
        finally:
            if conn:
                conn.close()