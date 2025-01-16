import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'empresa_db'
        self.user = 'root'
        self.password = ''
        self.conexion = None
        self.cursor = None

    def conectar(self):
        try:
            if not self.conexion:
                self.conexion = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                self.cursor = self.conexion.cursor(buffered=True)
            return True
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return False

    def desconectar(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conexion:
                if self.conexion.is_connected():
                    self.conexion.close()
        except Error as e:
            print(f"Error al desconectar: {e}")

    def ejecutar_query(self, query, valores=None):
        try:
            if valores:
                self.cursor.execute(query, valores)
            else:
                self.cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                resultados = self.cursor.fetchall()
                return resultados
            else:
                self.conexion.commit()
                return self.cursor.rowcount
        except Error as e:
            print(f"Error al ejecutar query: {str(e)}")
            # Si es un error de clave foránea, dar un mensaje más amigable
            if e.errno == 1452:  # Error de clave foránea
                print("Error: No se puede realizar la operación porque la referencia no existe")
            return None
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return None
