import tkinter as tk
from tkinter import ttk, messagebox
from servicios.restaurante_servicio import RestauranteServicio
from ui.main_view import MainView

class LoginView:
    def __init__(self, root: tk.Tk, servicio: RestauranteServicio):
        self.root = root
        self.servicio = servicio
        self.root.title("Inicio de Sesión - Restaurante")
        self.root.geometry("400x320")
        self.root.resizable(False, False)

        # Contenedor central
        frame = ttk.Frame(self.root, padding=25)
        frame.pack(expand=True, fill=tk.BOTH)

        lbl_titulo = ttk.Label(frame, text="Sistema de Restaurante", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=(0, 20))

        ttk.Label(frame, text="Usuario:").pack(anchor=tk.W, pady=(0, 2))
        self.entry_usuario = ttk.Entry(frame, width=30)
        self.entry_usuario.pack(fill=tk.X, pady=(0, 10))
        self.entry_usuario.focus_set()

        ttk.Label(frame, text="Contraseña:").pack(anchor=tk.W, pady=(0, 2))
        self.entry_clave = ttk.Entry(frame, width=30, show="*")
        self.entry_clave.pack(fill=tk.X, pady=(0, 20))

        # Atajo Enter para iniciar sesión
        self.entry_usuario.bind("<Return>", lambda e: self._accion_ingresar())
        self.entry_clave.bind("<Return>", lambda e: self._accion_ingresar())

        self.btn_ingresar = ttk.Button(frame, text="Ingresar al Sistema", command=self._accion_ingresar)
        self.btn_ingresar.pack(fill=tk.X, pady=5)

    def _accion_ingresar(self):
        usuario = self.entry_usuario.get().strip()
        clave = self.entry_clave.get().strip()

        if not usuario or not clave:
            messagebox.showwarning("Atención", "Por favor ingrese usuario y contraseña.")
            return

        # Búsqueda y validación detallada de credenciales
        usuarios = self.servicio.obtener_usuarios()
        user_match = next((u for u in usuarios if u.username == usuario), None)

        if not user_match:
            messagebox.showerror("Error de autenticación", "El usuario no existe.")
            self.entry_usuario.focus_set()
            return

        # Validación explícita de contraseña errónea
        if user_match.password != clave:
            messagebox.showerror("Error de autenticación", "La contraseña es incorrecta.")
            self.entry_clave.delete(0, tk.END)
            self.entry_clave.focus_set()
            return

        # Autenticación exitosa
        self.servicio.usuario_autenticado = user_match
        self.root.withdraw()
        
        # Apertura de la ventana principal
        main_window = MainView(self.root, self.servicio)
        main_window.protocol("WM_DELETE_WINDOW", self.root.destroy)