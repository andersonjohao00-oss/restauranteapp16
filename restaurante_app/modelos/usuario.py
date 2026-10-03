class Usuario:
    def __init__(self, id_usuario: str, username: str, password: str, rol: str = "Cliente"):
        self.id_usuario = str(id_usuario)
        self.username = username
        self.password = password
        self.rol = rol

    def to_dict(self) -> dict:
        return {
            "id_usuario": self.id_usuario,
            "username": self.username,
            "password": self.password,
            "rol": self.rol
        }

    @staticmethod
    def from_dict(data: dict) -> 'Usuario':
        return Usuario(
            id_usuario=str(data.get("id_usuario", "")),
            username=data.get("username", ""),
            password=data.get("password", ""),
            rol=data.get("rol", "Cliente")
        )