class Cliente:
    def __init__(self, cedula, nombre, correo):
        self._cedula = cedula # Atributo protegido
        self.nombre = nombre
        self.correo = correo # Esto activará el setter de abajo

    @property
    def correo(self):
        return self._correo_electronico

    @correo.setter
    def correo(self, valor):
        # Validación estricta requerida
        if "@" not in valor or "." not in valor:
            raise ValueError("El formato del correo es inválido")
        self._correo_electronico = valor

    def __str__(self):
        return f"Cliente: {self.nombre} | ID: {self._cedula}"