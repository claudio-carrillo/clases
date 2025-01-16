from conexion.conexion_db import ConexionDB

class RegistroTiempo:
    def __init__(self, empleado_id, proyecto_id, fecha, horas, descripcion):
        self._empleado_id = empleado_id
        self._proyecto_id = proyecto_id
        self._fecha = fecha
        self._horas = horas
        self._descripcion = descripcion
        self.db = ConexionDB()

    def guardar(self):
        try:
            self.db.conectar()
            query = """INSERT INTO registros_tiempo 
                      (empleado_id, proyecto_id, fecha, horas, descripcion)
                      VALUES (%s, %s, %s, %s, %s)"""
            valores = (self._empleado_id, self._proyecto_id, self._fecha,
                      self._horas, self._descripcion)
            resultado = self.db.ejecutar_query(query, valores)
            return resultado > 0
        finally:
            self.db.desconectar()

    def obtener_registros_empleado(self, empleado_id):
        try:
            self.db.conectar()
            query = """
                SELECT rt.fecha, rt.horas, rt.descripcion, 
                       p.nombre as proyecto_nombre
                FROM registros_tiempo rt
                LEFT JOIN proyectos p ON rt.proyecto_id = p.id
                WHERE rt.empleado_id = %s
                ORDER BY rt.fecha DESC"""
            resultados = self.db.ejecutar_query(query, (empleado_id,))
            return resultados
        finally:
            self.db.desconectar()
