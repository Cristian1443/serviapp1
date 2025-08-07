from modulos.pqr.acceso_datos.evidencia_dto import PQRDTO
from modulos.pqr.acceso_datos.conexion import ConexionDB

conn = ConexionDB().obtener_conexion()

class PQRDAOMySQL:
    def guardar(self, pqr_dto): 
        with conn.cursor() as cursor:
            sql = "INSERT INTO pqrs (id_solicitud, id_usuario, id_profesional, tipo, descripcion, estado) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (pqr_dto.id_solicitud, pqr_dto.id_usuario, pqr_dto.id_profesional, pqr_dto.tipo, pqr_dto.descripcion, pqr_dto.estado))
        conn.commit()

    def obtener_todos(self):
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_pqrs, id_solicitud, id_usuario, id_profesional, tipo, descripcion, estado, fecha_creacion FROM pqrs")
            rows = cursor.fetchall()
        return [PQRDTO(id_pqrs=row[0], id_solicitud=row[1], id_usuario=row[2], id_profesional=row[3], tipo=row[4], descripcion=row[5], estado=row[6], fecha_creacion=row[7]) for row in rows]

    def obtener_por_id(self, id):
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_pqrs, id_solicitud, id_usuario, id_profesional, tipo, descripcion, estado, fecha_creacion FROM pqrs WHERE id_pqrs = %s", (id,))
            row = cursor.fetchone()
        if row:
            return PQRDTO(id_pqrs=row[0], id_solicitud=row[1], id_usuario=row[2], id_profesional=row[3], tipo=row[4], descripcion=row[5], estado=row[6], fecha_creacion=row[7])
        return None

    def actualizar(self, pqr_dto): 
        with conn.cursor() as cursor:
            sql = "UPDATE pqrs SET id_solicitud = %s, id_usuario = %s, id_profesional = %s, tipo = %s, descripcion = %s, estado = %s WHERE id_pqrs = %s"
            cursor.execute(sql, (pqr_dto.id_solicitud, pqr_dto.id_usuario, pqr_dto.id_profesional, pqr_dto.tipo, pqr_dto.descripcion, pqr_dto.estado, pqr_dto.id_pqrs))
        conn.commit()

    def eliminar(self, id): 
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM pqrs WHERE id_pqrs = %s", (id,))
        conn.commit()


class PQRDAOPostgres:
    def guardar(self, pqr_dto):
        with conn.cursor() as cursor:
            sql = "INSERT INTO pqrs (id_solicitud, id_usuario, id_profesional, tipo, descripcion, estado) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (pqr_dto.id_solicitud, pqr_dto.id_usuario, pqr_dto.id_profesional, pqr_dto.tipo, pqr_dto.descripcion, pqr_dto.estado))
        conn.commit()

    def obtener_todos(self):
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_pqrs, id_solicitud, id_usuario, id_profesional, tipo, descripcion, estado, fecha_creacion FROM pqrs")
            rows = cursor.fetchall()
        return [PQRDTO(id_pqrs=row[0], id_solicitud=row[1], id_usuario=row[2], id_profesional=row[3], tipo=row[4], descripcion=row[5], estado=row[6], fecha_creacion=row[7]) for row in rows]

    def obtener_por_id(self, id):
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_pqrs, id_solicitud, id_usuario, id_profesional, tipo, descripcion, estado, fecha_creacion FROM pqrs WHERE id_pqrs = %s", (id,))
            row = cursor.fetchone()
        if row:
            return PQRDTO(id_pqrs=row[0], id_solicitud=row[1], id_usuario=row[2], id_profesional=row[3], tipo=row[4], descripcion=row[5], estado=row[6], fecha_creacion=row[7])
        return None

    def actualizar(self, pqr_dto):
        with conn.cursor() as cursor:
            sql = "UPDATE pqrs SET id_solicitud = %s, id_usuario = %s, id_profesional = %s, tipo = %s, descripcion = %s, estado = %s WHERE id_pqrs = %s"
            cursor.execute(sql, (pqr_dto.id_solicitud, pqr_dto.id_usuario, pqr_dto.id_profesional, pqr_dto.tipo, pqr_dto.descripcion, pqr_dto.estado, pqr_dto.id_pqrs))
        conn.commit()

    def eliminar(self, id):
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM pqrs WHERE id_pqrs = %s", (id,))
        conn.commit()