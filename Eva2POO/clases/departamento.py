from conexion.conexion_db import ConexionDB

class Departamento:
    def __init__(self, nombre, gerente_id=None):
        self._nombre = nombre
        self._gerente_id = gerente_id
        self.db = ConexionDB()

    def guardar(self):
        try:
            self.db.conectar()
            query = "INSERT INTO departamentos (nombre, gerente_id) VALUES (%s, %s)"
            valores = (self._nombre, self._gerente_id)
            resultado = self.db.ejecutar_query(query, valores)
            return resultado > 0
        finally:
            self.db.desconectar()

    def actualizar(self, id_departamento):
        try:
            self.db.conectar()
            query = "UPDATE departamentos SET nombre = %s, gerente_id = %s WHERE id = %s"
            valores = (self._nombre, self._gerente_id, id_departamento)
            resultado = self.db.ejecutar_query(query, valores)
            return resultado > 0
        finally:
            self.db.desconectar()

    def eliminar(self, id_departamento):
        try:
            self.db.conectar()
            query = "DELETE FROM departamentos WHERE id = %s"
            resultado = self.db.ejecutar_query(query, (id_departamento,))
            return resultado > 0
        finally:
            self.db.desconectar()

    def buscar(self, id_departamento):
        try:
            self.db.conectar()
            query = "SELECT id, nombre, gerente_id FROM departamentos WHERE id = %s"
            resultado = self.db.ejecutar_query(query, (id_departamento,))
            if resultado and len(resultado) > 0:
                return {
                    'id': resultado[0][0],
                    'nombre': resultado[0][1],
                    'gerente_id': resultado[0][2]
                }
            return None
        finally:
            self.db.desconectar()

    def listar_todos(self):
        try:
            self.db.conectar()
            query = "SELECT id, nombre, gerente_id FROM departamentos"
            return self.db.ejecutar_query(query)
        finally:
            self.db.desconectar()

    @property
    def nombre(self):
        return self._nombre
