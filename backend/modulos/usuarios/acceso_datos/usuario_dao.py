from modulos.usuarios.acceso_datos.usuario_dto import UsuarioDTO
from modulos.usuarios.acceso_datos.conexion import ConexionDB

# --- SE ELIMINA LA CONEXIÓN GLOBAL ---
# conn = ConexionDB().obtener_conexion()  <-- Esta línea es la causa del problema y se quita.

class UsuarioDAO:
    """
    DAO unificado para la tabla 'usuarios'.
    Gestiona la conexión y las transacciones de forma segura para cada operación,
    evitando errores 500 y de 'transacción abortada'.
    """
    def guardar(self, usuario_dto: UsuarioDTO):
        """
        Guarda un nuevo usuario de forma segura.
        """
        conn = None  # Inicia la conexión como nula
        try:
            # 1. Adquiere una conexión nueva solo para esta operación
            conn = ConexionDB().obtener_conexion()
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO usuarios (nombre, apellido, correo, telefono, direccion, contrasena)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                valores = (
                    usuario_dto.nombre, usuario_dto.apellido, usuario_dto.correo,
                    usuario_dto.telefono, usuario_dto.direccion, usuario_dto.contrasena
                )
                cursor.execute(sql, valores)
            # 2. Confirma la transacción si todo fue exitoso
            conn.commit()
        except Exception as e:
            # 3. Si ocurre cualquier error, deshace la transacción
            if conn:
                conn.rollback()
            print(f"Error al guardar usuario: {e}")
            raise  # Vuelve a lanzar el error para que FastAPI lo capture
        finally:
            # 4. Al final, con o sin error, cierra la conexión
            if conn:
                conn.close()

    def obtener_todos(self):
        """
        Obtiene todos los usuarios de forma segura.
        """
        conn = None
        try:
            conn = ConexionDB().obtener_conexion()
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_usuario, nombre, apellido, correo, telefono, direccion, contrasena, fecha_registro FROM usuarios")
                rows = cursor.fetchall()

            usuarios = [
                UsuarioDTO(id_usuario=row[0], nombre=row[1], apellido=row[2], correo=row[3], telefono=row[4], direccion=row[5], contrasena=row[6], fecha_registro=row[7]) for row in rows
            ]
            return usuarios
        except Exception as e:
            print(f"Error al obtener todos los usuarios: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_usuario: int):
        """
        Obtiene un usuario por ID de forma segura.
        """
        conn = None
        try:
            conn = ConexionDB().obtener_conexion()
            with conn.cursor() as cursor:
                sql = "SELECT id_usuario, nombre, apellido, correo, telefono, direccion, contrasena, fecha_registro FROM usuarios WHERE id_usuario = %s"
                cursor.execute(sql, (id_usuario,))
                row = cursor.fetchone()

            if row:
                return UsuarioDTO(id_usuario=row[0], nombre=row[1], apellido=row[2], correo=row[3], telefono=row[4], direccion=row[5], contrasena=row[6], fecha_registro=row[7])
            return None
        except Exception as e:
            print(f"Error al obtener usuario por ID: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def actualizar(self, usuario_dto: UsuarioDTO):
        """
        Actualiza un usuario de forma segura.
        """
        conn = None
        try:
            conn = ConexionDB().obtener_conexion()
            with conn.cursor() as cursor:
                sql = """
                    UPDATE usuarios SET nombre = %s, apellido = %s, correo = %s, telefono = %s, direccion = %s, contrasena = %s
                    WHERE id_usuario = %s
                """
                valores = (
                    usuario_dto.nombre, usuario_dto.apellido, usuario_dto.correo,
                    usuario_dto.telefono, usuario_dto.direccion, usuario_dto.contrasena,
                    usuario_dto.id_usuario
                )
                cursor.execute(sql, valores)
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al actualizar usuario: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def eliminar(self, id_usuario: int):
        """
        Elimina un usuario de forma segura.
        """
        conn = None
        try:
            conn = ConexionDB().obtener_conexion()
            with conn.cursor() as cursor:
                sql = "DELETE FROM usuarios WHERE id_usuario = %s"
                cursor.execute(sql, (id_usuario,))
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al eliminar usuario: {e}")
            raise
        finally:
            if conn:
                conn.close()