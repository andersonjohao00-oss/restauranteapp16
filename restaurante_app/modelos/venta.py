from datetime import datetime

class Venta:
    def __init__(self, id_venta: str, usuario: str, codigo_producto: str, nombre_producto: str, total: float, fecha: str = None):
        self.id_venta = id_venta
        self.usuario = usuario
        self.codigo_producto = codigo_producto
        self.nombre_producto = nombre_producto
        self.total = float(total)
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "usuario": self.usuario,
            "codigo_producto": self.codigo_producto,
            "nombre_producto": self.nombre_producto,
            "total": round(self.total, 2),
            "fecha": self.fecha
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_venta=data.get("id_venta", ""),
            usuario=data.get("usuario", ""),
            codigo_producto=data.get("codigo_producto", ""),
            nombre_producto=data.get("nombre_producto", ""),
            total=float(data.get("total", 0.0)),
            fecha=data.get("fecha", "")
        )