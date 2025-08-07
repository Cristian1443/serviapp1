from modulos.profesional.acceso_datos.profesional_dto import ProfesionalDTO
from modulos.profesional.acceso_datos.conexion import ConexionDB

conn = ConexionDB().obtener_conexion()

class ProfesionalDAOMySQL:
    """
    Data Access Object para la tabla 'profesionales' en MySQL.
    """
    def guardar(self, profesional_dto: ProfesionalDTO):
        """
        Guarda un nuevo profesional en la base de datos.
        """
        with conn.cursor() as cursor:
            sql = "INSERT INTO profesionales (nombre, apellido, correo, telefono, contraseña, profesion, habilidades, zona_trabajo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            valores = (
                profesional_dto.nombre,
                profesional_dto.apellido,
                profesional_dto.correo,
                profesional_dto.telefono,
                profesional_dto.contrasena,
                profesional_dto.profesion,
                profesional_dto.habilidades,
                profesional_dto.zona_trabajo
            )
            cursor.execute(sql, valores)
        conn.commit()

    def obtener_todos(self):
        """
        Obtiene todos los profesionales de la base de datos.
        """
        with conn.cursor() as cursor:
            sql = "SELECT id_profesional, nombre, apellido, correo, telefono, contraseña, profesion, habilidades, zona_trabajo FROM profesionales"
            cursor.execute(sql)
            rows = cursor.fetchall()
        
        return [ProfesionalDTO(
                id_profesional=row[0],
                nombre=row[1],
                apellido=row[2],
                correo=row[3],
                telefono=row[4],
                contrasena=row[5],
                profesion=row[6],
                habilidades=row[7],
                zona_trabajo=row[8]
            ) for row in rows
        ]

    def obtener_por_id(self, id: int):
        """
        Obtiene un profesional por su ID.
        """
        with conn.cursor() as cursor:
            sql = "SELECT id_profesional, nombre, apellido, correo, telefono, contraseña, profesion, habilidades, zona_trabajo FROM profesionales WHERE id_profesional = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
        
        if row:
            return ProfesionalDTO(
                id_profesional=row[0],
                nombre=row[1],
                apellido=row[2],
                correo=row[3],
                telefono=row[4],
                contrasena=row[5],
                profesion=row[6],
                habilidades=row[7],
                zona_trabajo=row[8]
            )
        return None

    def actualizar(self, profesional_dto: ProfesionalDTO):
        """
        Actualiza los datos de un profesional existente.
        """
        with conn.cursor() as cursor:
            sql = """
                UPDATE profesionales SET
                    nombre = %s,
                    apellido = %s,
                    correo = %s,
                    telefono = %s,
                    contraseña = %s,
                    profesion = %s,
                    habilidades = %s,
                    zona_trabajo = %s
                WHERE id_profesional = %s
            """
            valores = (
                profesional_dto.nombre,
                profesional_dto.apellido,
                profesional_dto.correo,
                profesional_dto.telefono,
                profesional_dto.contrasena,
                profesional_dto.profesion,
                profesional_dto.habilidades,
                profesional_dto.zona_trabajo,
                profesional_dto.id_profesional
            )
            cursor.execute(sql, valores)
        conn.commit()

    def eliminar(self, id: int):
        """
        Elimina un profesional de la base de datos por su ID.
        """
        with conn.cursor() as cursor:
            sql = "DELETE FROM profesionales WHERE id_profesional = %s"
            cursor.execute(sql, (id,))
        conn.commit()


class ProfesionalDAOPostgres:
    """
    Data Access Object para la tabla 'profesionales' en PostgreSQL.
    """
    def guardar(self, profesional_dto: ProfesionalDTO):
        """
        Guarda un nuevo profesional en la base de datos.
        """
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO profesionales (nombre, apellido, correo, telefono, contraseña, profesion, habilidades, zona_trabajo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                profesional_dto.nombre,
                profesional_dto.apellido,
                profesional_dto.correo,
                profesional_dto.telefono,
                profesional_dto.contrasena,
                profesional_dto.profesion,
                profesional_dto.habilidades,
                profesional_dto.zona_trabajo
            )
            cursor.execute(sql, valores)
        conn.commit()

    def obtener_todos(self):
        """
        Obtiene todos los profesionales de la base de datos.
        """
        with conn.cursor() as cursor:
            sql = "SELECT id_profesional, nombre, apellido, correo, telefono, contraseña, profesion, habilidades, zona_trabajo FROM profesionales"
            cursor.execute(sql)
            rows = cursor.fetchall()
        
        return [
            ProfesionalDTO(
                id_profesional=row[0],
                nombre=row[1],
                apellido=row[2],
                correo=row[3],
                telefono=row[4],
                contrasena=row[5],
                profesion=row[6],
                habilidades=row[7],
                zona_trabajo=row[8]
            ) for row in rows
        ]

    def obtener_por_id(self, id: int):
        """
        Obtiene un profesional por su ID.
        """
        with conn.cursor() as cursor:
            sql = "SELECT id_profesional, nombre, apellido, correo, telefono, contraseña, profesion, habilidades, zona_trabajo FROM profesionales WHERE id_profesional = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
        
        if row:
            return ProfesionalDTO(
                id_profesional=row[0],
                nombre=row[1],
                apellido=row[2],
                correo=row[3],
                telefono=row[4],
                contrasena=row[5],
                profesion=row[6],
                habilidades=row[7],
                zona_trabajo=row[8]
            )
        return None

    def actualizar(self, profesional_dto: ProfesionalDTO):
        """
        Actualiza los datos de un profesional existente.
        """
        with conn.cursor() as cursor:
            sql = """
                UPDATE profesionales SET
                    nombre = %s,
                    apellido = %s,
                    correo = %s,
                    telefono = %s,
                    contraseña = %s,
                    profesion = %s,
                    habilidades = %s,
                    zona_trabajo = %s
                WHERE id_profesional = %s
            """
            valores = (
                profesional_dto.nombre,
                profesional_dto.apellido,
                profesional_dto.correo,
                profesional_dto.telefono,
                profesional_dto.contrasena,
                profesional_dto.profesion,
                profesional_dto.habilidades,
                profesional_dto.zona_trabajo,
                profesional_dto.id_profesional
            )
            cursor.execute(sql, valores)
        conn.commit()

    def eliminar(self, id: int):
        """
        Elimina un profesional de la base de datos por su ID.
        """
        with conn.cursor() as cursor:
            sql = "DELETE FROM profesionales WHERE id_profesional = %s"
            cursor.execute(sql, (id,))
        conn.commit()