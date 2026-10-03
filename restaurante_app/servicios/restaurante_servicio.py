import uuid
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self, ruta_usuarios="datos/usuarios.json", ruta_productos="datos/productos.json", ruta_ventas="datos/ventas.json"):
        self.ruta_usuarios = ruta_usuarios
        self.ruta_productos = ruta_productos
        self.ruta_ventas = ruta_ventas
        self.archivo_servicio = ArchivoServicio()
        self.usuario_autenticado: Usuario | None = None

    # --- AUTENTICACIÓN ---
    def autenticar(self, usuario: str, clave: str) -> Usuario | None:
        usuarios = self.obtener_usuarios()
        for u in usuarios:
            if u.username == usuario and u.password == clave:
                self.usuario_autenticado = u
                return u
        return None

    def autenticar_usuario(self, usuario: str, clave: str) -> Usuario | None:
        return self.autenticar(usuario, clave)

    # --- GESTIÓN DE USUARIOS (SEMANA 16) ---
    def obtener_usuarios(self) -> list[Usuario]:
        datos = self.archivo_servicio.cargar_json(self.ruta_usuarios)
        return [Usuario.from_dict(u) for u in datos]

    def buscar_usuario_por_id(self, id_usuario: str) -> Usuario | None:
        for u in self.obtener_usuarios():
            if str(u.id_usuario) == str(id_usuario):
                return u
        return None

    def registrar_usuario(self, username: str, password: str, rol: str) -> tuple[bool, str]:
        username = username.strip()
        password = password.strip()
        if not username or not password:
            return False, "Todos los campos son obligatorios."
        if rol not in ["Administrador", "Empleado", "Cliente"]:
            return False, "El rol seleccionado no es válido."

        usuarios = self.obtener_usuarios()
        if any(u.username.lower() == username.lower() for u in usuarios):
            return False, f"El usuario '{username}' ya existe."

        nuevo_id = f"usr-{str(uuid.uuid4())[:4]}"
        nuevo = Usuario(id_usuario=nuevo_id, username=username, password=password, rol=rol)
        usuarios.append(nuevo)
        self.archivo_servicio.guardar_json(self.ruta_usuarios, [u.to_dict() for u in usuarios])
        return True, "Usuario registrado con éxito."

    def actualizar_usuario(self, id_usuario: str, username: str, password: str, rol: str) -> tuple[bool, str]:
        username = username.strip()
        password = password.strip()
        if not id_usuario:
            return False, "Seleccione un usuario de la lista."
        if not username or not password:
            return False, "Usuario y contraseña no pueden estar vacíos."

        usuarios = self.obtener_usuarios()
        for u in usuarios:
            if str(u.id_usuario) != str(id_usuario) and u.username.lower() == username.lower():
                return False, f"El nombre de usuario '{username}' ya está en uso."

        encontrado = False
        for u in usuarios:
            if str(u.id_usuario) == str(id_usuario):
                u.username = username
                u.password = password
                u.rol = rol
                encontrado = True
                break

        if not encontrado:
            return False, "Usuario no encontrado."

        self.archivo_servicio.guardar_json(self.ruta_usuarios, [u.to_dict() for u in usuarios])
        return True, "Usuario actualizado correctamente."

    def eliminar_usuario(self, id_usuario: str) -> tuple[bool, str]:
        if not id_usuario:
            return False, "Seleccione un usuario para eliminar."

        # Regla de comprobación: Impedir auto-eliminación
        if self.usuario_autenticado and str(self.usuario_autenticado.id_usuario) == str(id_usuario):
            return False, "No puede eliminar la cuenta con la que ha iniciado sesión."

        usuarios = self.obtener_usuarios()
        filtrados = [u for u in usuarios if str(u.id_usuario) != str(id_usuario)]
        if len(usuarios) == len(filtrados):
            return False, "No se encontró el usuario a eliminar."

        self.archivo_servicio.guardar_json(self.ruta_usuarios, [u.to_dict() for u in filtrados])
        return True, "Usuario eliminado correctamente."

    # --- MÉTODOS DE PRODUCTOS Y VENTAS (SEMANA 15) ---
    def obtener_productos(self) -> list[dict]:
        return self.archivo_servicio.cargar_json(self.ruta_productos)

    def guardar_producto(self, nombre: str, precio: float, categoria: str) -> tuple[bool, str]:
        prods = self.obtener_productos()
        nuevo_id = f"p-{len(prods) + 1:02d}"
        prods.append({"id": nuevo_id, "nombre": nombre, "precio": precio, "categoria": categoria})
        self.archivo_servicio.guardar_json(self.ruta_productos, prods)
        return True, "Producto guardado con éxito."

    def eliminar_producto(self, id_producto: str) -> tuple[bool, str]:
        prods = self.obtener_productos()
        filtrados = [p for p in prods if str(p.get("id", p.get("id_producto", ""))) != str(id_producto)]
        self.archivo_servicio.guardar_json(self.ruta_productos, filtrados)
        return True, "Producto eliminado."

    def obtener_ventas(self) -> list[dict]:
        return self.archivo_servicio.cargar_json(self.ruta_ventas)

    def registrar_venta(self, producto: str, cantidad: int, total: float) -> tuple[bool, str]:
        ventas = self.obtener_ventas()
        nuevo_id = f"v-{len(ventas) + 1:03d}"
        ventas.append({
            "id": nuevo_id,
            "producto": producto,
            "cantidad": cantidad,
            "total": total
        })
        self.archivo_servicio.guardar_json(self.ruta_ventas, ventas)
        return True, "Venta registrada."