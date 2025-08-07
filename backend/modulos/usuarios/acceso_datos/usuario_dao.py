from modulos.usuarios.acceso_datos.usuario_dto import UsuarioDTO
from modulos.usuarios.acceso_datos.conexion import ConexionDB

conn = ConexionDB().obtener_conexion()

class UsuarioDAOMySQL:
    """
    Data Access Object para la tabla 'usuarios' en MySQL.
    """
    def guardar(self, usuario_dto: UsuarioDTO):
        """
        Guarda un nuevo usuario en la base de datos.
        """
        with conn.cursor() as cursor:
            sql = "INSERT INTO usuarios (nombre, apellido, correo, telefono, direccion, contraseña) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (usuario_dto.nombre, usuario_dto.apellido, usuario_dto.correo, usuario_dto.telefono, usuario_dto.direccion, usuario_dto.contrasena))
        conn.commit()

    def obtener_todos(self):
        """
        Obtiene todos los usuarios de la base de datos.
        """
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_usuario, nombre, apellido, correo, telefono, direccion, contraseña, fecha_registro FROM usuarios")
            rows = cursor.fetchall()
        return [UsuarioDTO(id_usuario=row[0], nombre=row[1], apellido=row[2], correo=row[3], telefono=row[4], direccion=row[5], contrasena=row[6], fecha_registro=row[7]) for row in rows]

    def obtener_por_id(self, id: int):
        """
        Obtiene un usuario por su ID.
        """
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_usuario, nombre, apellido, correo, telefono, direccion, contraseña, fecha_registro FROM usuarios WHERE id_usuario = %s", (id,))
            row = cursor.fetchone()
        if row:
            return UsuarioDTO(id_usuario=row[0], nombre=row[1], apellido=row[2], correo=row[3], telefono=row[4], direccion=row[5], contrasena=row[6], fecha_registro=row[7])
        return None

    def actualizar(self, usuario_dto: UsuarioDTO):
        """
        Actualiza los datos de un usuario existente.
        """
        with conn.cursor() as cursor:
            sql = "UPDATE usuarios SET nombre = %s, apellido = %s, correo = %s, telefono = %s, direccion = %s, contraseña = %s WHERE id_usuario = %s"
            cursor.execute(sql, (usuario_dto.nombre, usuario_dto.apellido, usuario_dto.correo, usuario_dto.telefono, usuario_dto.direccion, usuario_dto.contrasena, usuario_dto.id_usuario))
        conn.commit()

    def eliminar(self, id: int):
        """
        Elimina un usuario de la base de datos por su ID.
        """
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
        conn.commit()


class UsuarioDAOPostgres:
    """
    Data Access Object para la tabla 'usuarios' en PostgreSQL.
    """
    def guardar(self, usuario_dto: UsuarioDTO):
        """
        Guarda un nuevo usuario en la base de datos.
        """
        with conn.cursor() as cursor:
            sql = "INSERT INTO usuarios (nombre, apellido, correo, telefono, direccion, contraseña) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (usuario_dto.nombre, usuario_dto.apellido, usuario_dto.correo, usuario_dto.telefono, usuario_dto.direccion, usuario_dto.contrasena))
        conn.commit()

    def obtener_todos(self):
        """
        Obtiene todos los usuarios de la base de datos.
        """
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_usuario, nombre, apellido, correo, telefono, direccion, contraseña, fecha_registro FROM usuarios")
            rows = cursor.fetchall()
        return [UsuarioDTO(id_usuario=row[0], nombre=row[1], apellido=row[2], correo=row[3], telefono=row[4], direccion=row[5], contrasena=row[6], fecha_registro=row[7]) for row in rows]

    def obtener_por_id(self, id: int):
        """
        Obtiene un usuario por su ID.
        """
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_usuario, nombre, apellido, correo, telefono, direccion, contraseña, fecha_registro FROM usuarios WHERE id_usuario = %s", (id,))
            row = cursor.fetchone()
        if row:
            return UsuarioDTO(id_usuario=row[0], nombre=row[1], apellido=row[2], correo=row[3], telefono=row[4], direccion=row[5], contrasena=row[6], fecha_registro=row[7])
        return None

    def actualizar(self, usuario_dto: UsuarioDTO):
        """
        Actualiza los datos de un usuario existente.
        """
        with conn.cursor() as cursor:
            sql = "UPDATE usuarios SET nombre = %s, apellido = %s, correo = %s, telefono = %s, direccion = %s, contraseña = %s WHERE id_usuario = %s"
            cursor.execute(sql, (usuario_dto.nombre, usuario_dto.apellido, usuario_dto.correo, usuario_dto.telefono, usuario_dto.direccion, usuario_dto.contrasena, usuario_dto.id_usuario))
        conn.commit()

    def eliminar(self, id: int):
        """
        Elimina un usuario de la base de datos por su ID.
        """
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
        conn.commit()