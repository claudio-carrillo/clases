class Persona:
    def __init__(self, nombre, direccion, telefono, email):
        self._nombre = nombre
        self._direccion = direccion
        self._telefono = telefono
        self._email = email

    @property
    def nombre(self):
        return self._nombre

    @property
    def direccion(self):
        return self._direccion

    @property
    def telefono(self):
        return self._telefono

    @property
    def email(self):
        return self._email
