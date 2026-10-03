import json
import os

class ArchivoServicio:
    def __init__(self):
        pass

    def cargar_json(self, ruta_archivo: str) -> list:
        if not os.path.exists(ruta_archivo):
            return []
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    return []
                return json.loads(contenido)
        except Exception:
            return []

    def guardar_json(self, ruta_archivo: str, datos: list) -> bool:
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            return True
        except Exception:
            return False

    def leer_json(self, ruta_archivo: str) -> list:
        return self.cargar_json(ruta_archivo)

    def guardar(self, ruta_archivo: str, datos: list) -> bool:
        return self.guardar_json(ruta_archivo, datos)