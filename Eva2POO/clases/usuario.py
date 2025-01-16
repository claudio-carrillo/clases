from conexion.conexion_db import ConexionDB
import bcrypt

class Usuario:
    def __init__(self, username, password, rol):
        self._username = username
        self._password = password
        self._rol = rol
        self.db = ConexionDB()

    def _hash_password(self, password):
        # Generar un hash bcrypt de la contraseña
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    def _check_password(self, password, hashed):
        try:
            # Asegurar que hashed sea bytes
            if isinstance(hashed, str):
                hashed = hashed.encode()
            # Verificar la contraseña con bcrypt
            return bcrypt.checkpw(password.encode(), hashed)
        except Exception as e:
            print(f"Error al verificar contraseña: {e}")
            return False

    def _validar_password(self, password):
        # Validar que la contraseña tenga al menos 6 caracteres
        return len(password) >= 6

    def guardar(self):
        if not self._validar_password(self._password):
            print("La contraseña debe tener al menos 6 caracteres")
            return False

        try:
            self.db.conectar()
            # Hashear la contraseña antes de guardarla
            hashed_password = self._hash_password(self._password)
            query = "INSERT INTO usuarios (username, password, rol) VALUES (%s, %s, %s)"
            valores = (self._username, hashed_password, self._rol)
            resultado = self.db.ejecutar_query(query, valores)
            return resultado > 0
        finally:
            self.db.desconectar()

    def verificar_credenciales(self):
        try:
            self.db.conectar()
            query = "SELECT password, rol FROM usuarios WHERE username = %s"
            valores = (self._username,)
            resultado = self.db.ejecutar_query(query, valores)
            
            if resultado and len(resultado) > 0:
                hashed_password = resultado[0][0]
                if self._check_password(self._password, hashed_password):
                    return resultado[0][1]  # Retorna el rol del usuario
            return None
        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
            return None
        finally:
            self.db.desconectar()
