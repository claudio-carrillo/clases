from .persona import Persona
from conexion.conexion_db import ConexionDB

class Empleado(Persona):
    def __init__(self, nombre, direccion, telefono, email, fecha_inicio, salario):
        super().__init__(nombre, direccion, telefono, email)
        self._fecha_inicio = fecha_inicio
        self._salario = salario
        self._departamento_id = None
        self.db = ConexionDB()

    def guardar(self):
        try:
            self.db.conectar()
            query = """INSERT INTO empleados (nombre, direccion, telefono, email, 
                      fecha_inicio, salario) VALUES (%s, %s, %s, %s, %s, %s)"""
            valores = (self._nombre, self._direccion, self._telefono, 
                      self._email, self._fecha_inicio, self._salario)
            
            resultado = self.db.ejecutar_query(query, valores)
            return resultado > 0
        finally:
            self.db.desconectar()

    def asignar_departamento(self, departamento_id, empleado_id):
        try:
            self.db.conectar()
            # Primero verificar que el departamento existe
            query_check = "SELECT id FROM departamentos WHERE id = %s"
            resultado = self.db.ejecutar_query(query_check, (departamento_id,))
            if not resultado:
                print("Error: El departamento no existe")
                return False

            # Verificar que el empleado existe
            query_check = "SELECT id FROM empleados WHERE id = %s"
            resultado = self.db.ejecutar_query(query_check, (empleado_id,))
            if not resultado:
                print("Error: El empleado no existe")
                return False

            # Realizar la actualización
            query = "UPDATE empleados SET departamento_id = %s WHERE id = %s"
            valores = (departamento_id, empleado_id)
            resultado = self.db.ejecutar_query(query, valores)
            if resultado > 0:
                print("Asignación realizada con éxito")
                return True
            else:
                print("No se pudo realizar la actualización")
                return False
        except Exception as e:
            print(f"Error en la base de datos: {str(e)}")
            return False
        finally:
            self.db.desconectar()
