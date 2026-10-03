import os
import tkinter as tk
from tkinter import ttk, messagebox
from servicios.restaurante_servicio import RestauranteServicio

class MainView(tk.Toplevel):
    def __init__(self, master_or_service, servicio: RestauranteServicio = None):
        if servicio is None:
            super().__init__()
            self.servicio = master_or_service
        else:
            super().__init__(master_or_service)
            self.servicio = servicio

        self.title("Restaurante App - Sistema Principal")
        self.geometry("1020x680")
        self.minsize(940, 600)

        # Referencias de imágenes para evitar recolección de basura
        self.imagenes = {}
        self._cargar_recursos_assets()

        # Encabezado con Logo e información de sesión
        self._construir_encabezado()

        # Cuaderno de pestañas principal
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 15))

        # 1. Pestaña de Productos (Semana 15)
        self.frame_productos = ttk.Frame(self.notebook)
        self.notebook.add(
            self.frame_productos, 
            text=" Productos", 
            image=self.imagenes.get("productos", ""), 
            compound="left"
        )
        self._construir_modulo_productos()

        # 2. Pestaña de Ventas (Semana 15)
        self.frame_ventas = ttk.Frame(self.notebook)
        self.notebook.add(
            self.frame_ventas, 
            text=" Ventas", 
            image=self.imagenes.get("ventas", ""), 
            compound="left"
        )
        self._construir_modulo_ventas()

        # 3. Pestaña de Usuarios (Semana 16 - Solo Administrador)
        if self.servicio.usuario_autenticado and self.servicio.usuario_autenticado.rol == "Administrador":
            self.frame_usuarios = ttk.Frame(self.notebook)
            self.notebook.add(
                self.frame_usuarios, 
                text=" Gestión de Usuarios", 
                image=self.imagenes.get("usuarios", ""), 
                compound="left"
            )
            self._construir_modulo_usuarios()

    def _cargar_recursos_assets(self):
        """Carga y dimensiona los iconos y logo de la carpeta assets/."""
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
        archivos = {
            "logo": "logo.png",
            "productos": "icon_productos.png",
            "ventas": "icon_ventas.png",
            "usuarios": "icon_usuarios.png"
        }
        for clave, archivo in archivos.items():
            ruta = os.path.join(base_path, archivo)
            if os.path.exists(ruta):
                try:
                    img = tk.PhotoImage(file=ruta)
                    if clave != "logo" and (img.width() > 32 or img.height() > 32):
                        factor_x = max(1, img.width() // 20)
                        factor_y = max(1, img.height() // 20)
                        img = img.subsample(factor_x, factor_y)
                    elif clave == "logo" and (img.width() > 80 or img.height() > 80):
                        factor_x = max(1, img.width() // 48)
                        factor_y = max(1, img.height() // 48)
                        img = img.subsample(factor_x, factor_y)
                    self.imagenes[clave] = img
                except Exception:
                    self.imagenes[clave] = ""
            else:
                self.imagenes[clave] = ""

    def _construir_encabezado(self):
        header_frame = ttk.Frame(self, padding=(15, 10))
        header_frame.pack(fill=tk.X)

        if self.imagenes.get("logo"):
            lbl_logo = ttk.Label(header_frame, image=self.imagenes["logo"])
            lbl_logo.pack(side=tk.LEFT, padx=(0, 15))

        info_frame = ttk.Frame(header_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(info_frame, text="Restaurante App", font=("Arial", 15, "bold")).pack(anchor=tk.W)
        usr_nom = self.servicio.usuario_autenticado.username if self.servicio.usuario_autenticado else "Invitado"
        usr_rol = self.servicio.usuario_autenticado.rol if self.servicio.usuario_autenticado else "Sin Rol"
        ttk.Label(info_frame, text=f"Sesión activa: {usr_nom} | Rol: {usr_rol}", font=("Arial", 9, "italic")).pack(anchor=tk.W)

    # =========================================================================
    # SECCIÓN 1: PRODUCTOS
    # =========================================================================
    def _construir_modulo_productos(self):
        form_frame = ttk.LabelFrame(self.frame_productos, text="Datos del Producto", padding=15)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(form_frame, text="Nombre del Producto:").pack(anchor=tk.W, pady=(0, 2))
        self.entry_prod_nombre = ttk.Entry(form_frame, width=28)
        self.entry_prod_nombre.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Precio ($):").pack(anchor=tk.W, pady=(0, 2))
        self.entry_prod_precio = ttk.Entry(form_frame, width=28)
        self.entry_prod_precio.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Categoría:").pack(anchor=tk.W, pady=(0, 2))
        self.combo_prod_cat = ttk.Combobox(
            form_frame, 
            values=["Platos Fuertes", "Bebidas", "Postres", "Entradas"], 
            state="readonly"
        )
        self.combo_prod_cat.set("Platos Fuertes")
        self.combo_prod_cat.pack(fill=tk.X, pady=(0, 15))

        btn_box = ttk.Frame(form_frame)
        btn_box.pack(fill=tk.X)

        ttk.Button(btn_box, text="Guardar Producto", command=self._guardar_producto).pack(fill=tk.X, pady=2)
        ttk.Button(btn_box, text="Eliminar Producto", command=self._eliminar_producto).pack(fill=tk.X, pady=2)
        ttk.Button(btn_box, text="Limpiar Formulario", command=self._limpiar_prod_form).pack(fill=tk.X, pady=2)

        tree_frame = ttk.Frame(self.frame_productos)
        tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        cols = ("id", "nombre", "precio", "categoria")
        self.tree_prod = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        self.tree_prod.heading("id", text="ID")
        self.tree_prod.heading("nombre", text="Nombre")
        self.tree_prod.heading("precio", text="Precio")
        self.tree_prod.heading("categoria", text="Categoría")

        self.tree_prod.column("id", width=80, anchor=tk.CENTER)
        self.tree_prod.column("nombre", width=200)
        self.tree_prod.column("precio", width=100, anchor=tk.E)
        self.tree_prod.column("categoria", width=140, anchor=tk.CENTER)

        scroll_prod = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_prod.yview)
        self.tree_prod.configure(yscrollcommand=scroll_prod.set)
        self.tree_prod.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_prod.pack(side=tk.RIGHT, fill=tk.Y)

        self._cargar_productos_treeview()

    def _cargar_productos_treeview(self):
        for item in self.tree_prod.get_children():
            self.tree_prod.delete(item)
        
        productos = self.servicio.obtener_productos()
        actualizar_json = False

        for idx, p in enumerate(productos, start=1):
            # Asignación segura del ID para evitar campos vacíos
            p_id = p.get("id") or p.get("id_producto")
            if not p_id or str(p_id).strip() == "":
                p_id = f"P-{idx:03d}"
                p["id"] = p_id
                actualizar_json = True

            nombre = p.get("nombre", "")
            precio_val = float(p.get("precio", 0.0))
            categoria = p.get("categoria", "")

            self.tree_prod.insert("", tk.END, values=(
                p_id,
                nombre,
                f"${precio_val:.2f}",
                categoria
            ))

        if actualizar_json:
            self.servicio.archivo_servicio.guardar_json(self.servicio.ruta_productos, productos)

    def _guardar_producto(self):
        nombre = self.entry_prod_nombre.get().strip()
        precio_txt = self.entry_prod_precio.get().strip()
        cat = self.combo_prod_cat.get()

        if not nombre or not precio_txt:
            messagebox.showwarning("Atención", "Complete todos los campos del producto.")
            return
        try:
            precio = float(precio_txt)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        self.servicio.guardar_producto(nombre, precio, cat)
        messagebox.showinfo("Éxito", "Producto guardado correctamente.")
        self._cargar_productos_treeview()
        self._limpiar_prod_form()
        if hasattr(self, 'combo_venta_prod'):
            self._actualizar_combo_productos_ventas()

    def _eliminar_producto(self):
        sel = self.tree_prod.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar.")
            return
        valores = self.tree_prod.item(sel[0], "values")
        p_id = valores[0]
        self.servicio.eliminar_producto(p_id)
        messagebox.showinfo("Éxito", "Producto eliminado.")
        self._cargar_productos_treeview()
        if hasattr(self, 'combo_venta_prod'):
            self._actualizar_combo_productos_ventas()

    def _limpiar_prod_form(self):
        self.entry_prod_nombre.delete(0, tk.END)
        self.entry_prod_precio.delete(0, tk.END)
        self.combo_prod_cat.set("Platos Fuertes")

    # =========================================================================
    # SECCIÓN 2: VENTAS
    # =========================================================================
    def _construir_modulo_ventas(self):
        form_frame = ttk.LabelFrame(self.frame_ventas, text="Registrar Venta", padding=15)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(form_frame, text="Seleccionar Producto:").pack(anchor=tk.W, pady=(0, 2))
        self.combo_venta_prod = ttk.Combobox(form_frame, state="readonly", width=26)
        self.combo_venta_prod.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Cantidad:").pack(anchor=tk.W, pady=(0, 2))
        self.spin_cantidad = ttk.Spinbox(form_frame, from_=1, to=100, width=26)
        self.spin_cantidad.set(1)
        self.spin_cantidad.pack(fill=tk.X, pady=(0, 15))

        ttk.Button(form_frame, text="Procesar Venta", command=self._registrar_venta).pack(fill=tk.X, pady=5)

        tree_frame = ttk.Frame(self.frame_ventas)
        tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        cols = ("id", "producto", "cantidad", "total")
        self.tree_ventas = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        self.tree_ventas.heading("id", text="ID Venta")
        self.tree_ventas.heading("producto", text="Producto")
        self.tree_ventas.heading("cantidad", text="Cantidad")
        self.tree_ventas.heading("total", text="Total Pagado")

        self.tree_ventas.column("id", width=80, anchor=tk.CENTER)
        self.tree_ventas.column("producto", width=200)
        self.tree_ventas.column("cantidad", width=80, anchor=tk.CENTER)
        self.tree_ventas.column("total", width=100, anchor=tk.E)

        scroll_ventas = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scroll_ventas.set)
        self.tree_ventas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_ventas.pack(side=tk.RIGHT, fill=tk.Y)

        self._actualizar_combo_productos_ventas()
        self._cargar_ventas_treeview()

    def _actualizar_combo_productos_ventas(self):
        prods = self.servicio.obtener_productos()
        self.lista_nombres_prods = [f"{p.get('nombre')} (${float(p.get('precio', 0)):.2f})" for p in prods]
        self.combo_venta_prod['values'] = self.lista_nombres_prods
        if self.lista_nombres_prods:
            self.combo_venta_prod.current(0)

    def _cargar_ventas_treeview(self):
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        for idx, v in enumerate(self.servicio.obtener_ventas(), start=1):
            v_id = v.get("id") or v.get("id_venta") or f"V-{idx:03d}"
            self.tree_ventas.insert("", tk.END, values=(
                v_id,
                v.get("producto", ""),
                v.get("cantidad", 1),
                f"${float(v.get('total', 0)):.2f}"
            ))

    def _registrar_venta(self):
        idx = self.combo_venta_prod.current()
        if idx < 0:
            messagebox.showwarning("Atención", "No hay productos disponibles para vender.")
            return

        prods = self.servicio.obtener_productos()
        prod = prods[idx]

        try:
            cant = int(self.spin_cantidad.get())
            if cant <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
            return

        total = float(prod.get("precio", 0)) * cant
        self.servicio.registrar_venta(prod.get("nombre"), cant, total)
        messagebox.showinfo("Venta Exitosa", f"Venta registrada. Total: ${total:.2f}")
        self._cargar_ventas_treeview()

    # =========================================================================
    # SECCIÓN 3: GESTIÓN DE USUARIOS (SEMANA 16: EVENTOS & BIND)
    # =========================================================================
    def _construir_modulo_usuarios(self):
        form_frame = ttk.LabelFrame(self.frame_usuarios, text="Datos del Usuario", padding=15)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.lbl_usr_id = ttk.Label(form_frame, text="ID: (Nuevo)")
        self.lbl_usr_id.pack(anchor=tk.W, pady=(0, 10))

        ttk.Label(form_frame, text="Usuario:").pack(anchor=tk.W)
        self.entry_usr_username = ttk.Entry(form_frame, width=28)
        self.entry_usr_username.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Contraseña:").pack(anchor=tk.W)
        self.entry_usr_password = ttk.Entry(form_frame, width=28, show="*")
        self.entry_usr_password.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Rol:").pack(anchor=tk.W)
        self.combo_usr_rol = ttk.Combobox(
            form_frame,
            values=["Empleado", "Cliente", "Administrador"],
            state="readonly"
        )
        self.combo_usr_rol.set("Cliente")
        self.combo_usr_rol.pack(fill=tk.X, pady=(0, 5))

        self.lbl_usr_info_rol = ttk.Label(form_frame, text="Acceso básico de cliente", font=("Arial", 8, "italic"))
        self.lbl_usr_info_rol.pack(anchor=tk.W, pady=(0, 15))

        btn_box = ttk.Frame(form_frame)
        btn_box.pack(fill=tk.X, pady=5)

        ttk.Button(btn_box, text="Registrar", command=self._accion_registrar_usuario).grid(row=0, column=0, padx=2, pady=2, sticky="ew")
        ttk.Button(btn_box, text="Actualizar", command=self._accion_actualizar_usuario).grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        ttk.Button(btn_box, text="Eliminar", command=self._accion_eliminar_usuario).grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        ttk.Button(btn_box, text="Limpiar", command=self._limpiar_usuario_form).grid(row=1, column=1, padx=2, pady=2, sticky="ew")

        btn_box.columnconfigure(0, weight=1)
        btn_box.columnconfigure(1, weight=1)

        tree_frame = ttk.Frame(self.frame_usuarios)
        tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        cols = ("id", "username", "rol")
        self.tree_usr = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        self.tree_usr.heading("id", text="ID")
        self.tree_usr.heading("username", text="Usuario")
        self.tree_usr.heading("rol", text="Rol")

        self.tree_usr.column("id", width=90, anchor=tk.CENTER)
        self.tree_usr.column("username", width=190)
        self.tree_usr.column("rol", width=120, anchor=tk.CENTER)

        scroll_usr = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_usr.yview)
        self.tree_usr.configure(yscrollcommand=scroll_usr.set)
        self.tree_usr.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_usr.pack(side=tk.RIGHT, fill=tk.Y)

        # EVENTOS VINCULADOS CON bind()
        self.tree_usr.bind("<<TreeviewSelect>>", self._on_treeview_usr_select)
        self.entry_usr_username.bind("<Return>", lambda e: self._accion_registrar_usuario())
        self.entry_usr_password.bind("<Return>", lambda e: self._accion_registrar_usuario())
        self.frame_usuarios.bind_all("<Escape>", lambda e: self._limpiar_usuario_form())
        self.combo_usr_rol.bind("<<ComboboxSelected>>", self._on_combobox_usr_selected)

        self.usuario_seleccionado_id = None
        self._cargar_usuarios_treeview()

    def _cargar_usuarios_treeview(self):
        for item in self.tree_usr.get_children():
            self.tree_usr.delete(item)
        for u in self.servicio.obtener_usuarios():
            self.tree_usr.insert("", tk.END, values=(u.id_usuario, u.username, u.rol))

    def _on_treeview_usr_select(self, event):
        sel = self.tree_usr.selection()
        if not sel:
            return
        valores = self.tree_usr.item(sel[0], "values")
        id_sel = valores[0]
        usuario = self.servicio.buscar_usuario_por_id(id_sel)
        if usuario:
            self.usuario_seleccionado_id = usuario.id_usuario
            self.lbl_usr_id.config(text=f"ID: {usuario.id_usuario}")
            self.entry_usr_username.delete(0, tk.END)
            self.entry_usr_username.insert(0, usuario.username)
            self.entry_usr_password.delete(0, tk.END)
            self.entry_usr_password.insert(0, usuario.password)
            self.combo_usr_rol.set(usuario.rol)
            self._actualizar_info_rol(usuario.rol)

    def _on_combobox_usr_selected(self, event):
        self._actualizar_info_rol(self.combo_usr_rol.get())

    def _actualizar_info_rol(self, rol: str):
        mensajes = {
            "Administrador": "Acceso total al sistema y gestión de usuarios.",
            "Empleado": "Gestión de inventario de productos y ventas.",
            "Cliente": "Acceso de consulta general al menú."
        }
        self.lbl_usr_info_rol.config(text=mensajes.get(rol, ""))

    def _accion_registrar_usuario(self):
        usr = self.entry_usr_username.get()
        pwd = self.entry_usr_password.get()
        rol = self.combo_usr_rol.get()

        ok, msg = self.servicio.registrar_usuario(usr, pwd, rol)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self._cargar_usuarios_treeview()
            self._limpiar_usuario_form()
        else:
            messagebox.showwarning("Atención", msg)

    def _accion_actualizar_usuario(self):
        if not self.usuario_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un usuario de la tabla.")
            return

        usr = self.entry_usr_username.get()
        pwd = self.entry_usr_password.get()
        rol = self.combo_usr_rol.get()

        ok, msg = self.servicio.actualizar_usuario(self.usuario_seleccionado_id, usr, pwd, rol)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self._cargar_usuarios_treeview()
            self._limpiar_usuario_form()
        else:
            messagebox.showerror("Error", msg)

    def _accion_eliminar_usuario(self):
        if not self.usuario_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un usuario para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmación", "¿Está seguro de eliminar este usuario?")
        if confirmar:
            ok, msg = self.servicio.eliminar_usuario(self.usuario_seleccionado_id)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self._cargar_usuarios_treeview()
                self._limpiar_usuario_form()
            else:
                messagebox.showerror("Error", msg)

    def _limpiar_usuario_form(self):
        self.usuario_seleccionado_id = None
        self.lbl_usr_id.config(text="ID: (Nuevo)")
        self.entry_usr_username.delete(0, tk.END)
        self.entry_usr_password.delete(0, tk.END)
        self.combo_usr_rol.set("Cliente")
        self._actualizar_info_rol("Cliente")
        if self.tree_usr.selection():
            self.tree_usr.selection_remove(self.tree_usr.selection()[0])
        self.entry_usr_username.focus_set()