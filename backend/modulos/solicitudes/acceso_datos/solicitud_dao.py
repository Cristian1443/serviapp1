from modulos.evidencias.acceso_datos.conexion import ConexionDB
from modulos.solicitudes.acceso_datos.solicitud_dto import SolicitudDTO

conn = ConexionDB().obtener_conexion()

class SolicitudDAOMySQL:
    def guardar(self, dto: SolicitudDTO):
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO solicitudes (
                    id_usuario, id_profesional, id_servicio, descripcion,
                    direccion_servicio, telefono_contacto, fecha_servicio,
                    hora_servicio, presupuesto, estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                dto.id_usuario, dto.id_profesional, dto.id_servicio,
                dto.descripcion, dto.direccion_servicio, dto.telefono_contacto,
                dto.fecha_servicio, dto.hora_servicio, dto.presupuesto, dto.estado
            ))
        conn.commit()

    def obtener_todos(self):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM solicitudes")
            rows = cursor.fetchall()
        return [SolicitudDTO(*row) for row in rows]

    def obtener_por_id(self, id_solicitud):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM solicitudes WHERE id_solicitud = %s", (id_solicitud,))
            row = cursor.fetchone()
        return SolicitudDTO(*row) if row else None

    def actualizar(self, dto: SolicitudDTO):
        with conn.cursor() as cursor:
            sql = """
                UPDATE solicitudes SET
                    id_usuario = %s,
                    id_profesional = %s,
                    id_servicio = %s,
                    descripcion = %s,
                    direccion_servicio = %s,
                    telefono_contacto = %s,
                    fecha_servicio = %s,
                    hora_servicio = %s,
                    presupuesto = %s,
                    estado = %s
                WHERE id_solicitud = %s
            """
            cursor.execute(sql, (
                dto.id_usuario, dto.id_profesional, dto.id_servicio,
                dto.descripcion, dto.direccion_servicio, dto.telefono_contacto,
                dto.fecha_servicio, dto.hora_servicio, dto.presupuesto,
                dto.estado, dto.id_solicitud
            ))
        conn.commit()

    def eliminar(self, id_solicitud):
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM solicitudes WHERE id_solicitud = %s", (id_solicitud,))
        conn.commit()


class SolicitudDAOPostgres(SolicitudDAOMySQL):
    # Si necesitas algo específico para PostgreSQL (por ejemplo enums), aquí puedes sobrescribir los métodos
    pass
