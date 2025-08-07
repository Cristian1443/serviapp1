from modulos.evidencias.acceso_datos.evidencia_dto import EvidenciaDTO
from modulos.evidencias.acceso_datos.conexion import ConexionDB

conn = ConexionDB().obtener_conexion()

class EvidenciaDAOMySQL:
    def guardar(self, producto_dto): 
        with conn.cursor() as cursor:
            sql = "INSERT INTO evidencias (id_solicitud, id_usuario, id_profesional, tipo_actor, archivo_contenido, descripcion, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (producto_dto.id_solicitud, producto_dto.id_usuario, producto_dto.id_profesional, producto_dto.tipo_actor, producto_dto.archivo_contenido, producto_dto.descripcion, producto_dto.estado))
        conn.commit()

    def obtener_todos(self):
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_evidencia, id_solicitud, id_usuario, id_profesional, tipo_actor, archivo_contenido, descripcion, estado, fecha_subida FROM evidencias")
            rows = cursor.fetchall()
        return [EvidenciaDTO(id_evidencia=row[0], id_solicitud=row[1], id_usuario=row[2], id_profesional=row[3], tipo_actor=row[4], archivo_contenido=row[5], descripcion=row[6], estado=row[7], fecha_subida=row[8]) for row in rows]

    def obtener_por_id(self, id):
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_evidencia, id_solicitud, id_usuario, id_profesional, tipo_actor, archivo_contenido, descripcion, estado, fecha_subida FROM evidencias WHERE id_evidencia = %s", (id,))
            row = cursor.fetchone()
        if row:
            return EvidenciaDTO(id_evidencia=row[0], id_solicitud=row[1], id_usuario=row[2], id_profesional=row[3], tipo_actor=row[4], archivo_contenido=row[5], descripcion=row[6], estado=row[7], fecha_subida=row[8])
        return None

    def actualizar(self, producto_dto): 
        with conn.cursor() as cursor:
            sql = "UPDATE evidencias SET id_solicitud = %s, id_usuario = %s, id_profesional = %s, tipo_actor = %s, archivo_contenido = %s, descripcion = %s, estado = %s WHERE id_evidencia = %s"
            cursor.execute(sql, (producto_dto.id_solicitud, producto_dto.id_usuario, producto_dto.id_profesional, producto_dto.tipo_actor, producto_dto.archivo_contenido, producto_dto.descripcion, producto_dto.estado, producto_dto.id_evidencia))
        conn.commit()

    def eliminar(self, id): 
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM evidencias WHERE id_evidencia = %s", (id,))
        conn.commit()


class EvidenciaDAOPostgres:
    def guardar(self, producto_dto):
        with conn.cursor() as cursor:
            sql = "INSERT INTO evidencias (id_solicitud, id_usuario, id_profesional, tipo_actor, archivo_contenido, descripcion, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (producto_dto.id_solicitud, producto_dto.id_usuario, producto_dto.id_profesional, producto_dto.tipo_actor, producto_dto.archivo_contenido, producto_dto.descripcion, producto_dto.estado))
        conn.commit()

    def obtener_todos(self):
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_evidencia, id_solicitud, id_usuario, id_profesional, tipo_actor, archivo_contenido, descripcion, estado, fecha_subida FROM evidencias")
            rows = cursor.fetchall()
        return [EvidenciaDTO(id_evidencia=row[0], id_solicitud=row[1], id_usuario=row[2], id_profesional=row[3], tipo_actor=row[4], archivo_contenido=row[5], descripcion=row[6], estado=row[7], fecha_subida=row[8]) for row in rows]

    def obtener_por_id(self, id):
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_evidencia, id_solicitud, id_usuario, id_profesional, tipo_actor, archivo_contenido, descripcion, estado, fecha_subida FROM evidencias WHERE id_evidencia = %s", (id,))
            row = cursor.fetchone()
        if row:
            return EvidenciaDTO(id_evidencia=row[0], id_solicitud=row[1], id_usuario=row[2], id_profesional=row[3], tipo_actor=row[4], archivo_contenido=row[5], descripcion=row[6], estado=row[7], fecha_subida=row[8])
        return None

    def actualizar(self, producto_dto):
        with conn.cursor() as cursor:
            sql = "UPDATE evidencias SET id_solicitud = %s, id_usuario = %s, id_profesional = %s, tipo_actor = %s, archivo_contenido = %s, descripcion = %s, estado = %s WHERE id_evidencia = %s"
            cursor.execute(sql, (producto_dto.id_solicitud, producto_dto.id_usuario, producto_dto.id_profesional, producto_dto.tipo_actor, producto_dto.archivo_contenido, producto_dto.descripcion, producto_dto.estado, producto_dto.id_evidencia))
        conn.commit()

    def eliminar(self, id):
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM evidencias WHERE id_evidencia = %s", (id,))
        conn.commit()