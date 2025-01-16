from conexion.conexion_db import ConexionDB

class Proyecto:
    def __init__(self, nombre, descripcion, fecha_inicio):
        self._nombre = nombre
        self._descripcion = descripcion
        self._fecha_inicio = fecha_inicio
        self.db = ConexionDB()

    def guardar(self):
        try:
            self.db.conectar()
            query = """INSERT INTO proyectos (nombre, descripcion, fecha_inicio) 
                      VALUES (%s, %s, %s)"""
            valores = (self._nombre, self._descripcion, self._fecha_inicio)
            resultado = self.db.ejecutar_query(query, valores)
            return resultado > 0
        finally:
            self.db.desconectar()

    def actualizar(self, id_proyecto):
        try:
            self.db.conectar()
            query = """UPDATE proyectos SET nombre = %s, descripcion = %s, 
                      fecha_inicio = %s WHERE id = %s"""
            valores = (self._nombre, self._descripcion, self._fecha_inicio, id_proyecto)
            resultado = self.db.ejecutar_query(query, valores)
            return resultado > 0
        finally:
            self.db.desconectar()

    def eliminar(self, id_proyecto):
        try:
            self.db.conectar()
            query = "DELETE FROM proyectos WHERE id = %s"
            resultado = self.db.ejecutar_query(query, (id_proyecto,))
            return resultado > 0
        finally:
            self.db.desconectar()

    def buscar(self, id_proyecto):
        try:
            self.db.conectar()
            query = """SELECT id, nombre, descripcion, fecha_inicio 
                      FROM proyectos WHERE id = %s"""
            resultado = self.db.ejecutar_query(query, (id_proyecto,))
            if resultado and len(resultado) > 0:
                return {
                    'id': resultado[0][0],
                    'nombre': resultado[0][1],
                    'descripcion': resultado[0][2],
                    'fecha_inicio': resultado[0][3]
                }
            return None
        finally:
            self.db.desconectar()

    def listar_todos(self):
        try:
            self.db.conectar()
            query = "SELECT id, nombre, descripcion, fecha_inicio FROM proyectos"
            return self.db.ejecutar_query(query)
        finally:
            self.db.desconectar()
