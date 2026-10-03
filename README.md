# Restaurante App (Semana 16)

Evolución modular del sistema de restaurante con Tkinter, integrando gestión integral de eventos y control de acceso basado en roles.

---

## 🎯 Contexto y Objetivos (Semana 16)

La versión de la **Semana 16** consolida las funcionalidades previas del sistema (`LoginView`, gestión de productos y registro de ventas) e incorpora un módulo administrativo de **Gestión de Usuarios** con separación de privilegios y manejo dinámico de eventos en Tkinter.

### Flujo de Interacción Implementado:
`Usuario` ➔ `Evento` ➔ `bind()` ➔ `Callback` ➔ `RestauranteServicio` ➔ `Persistencia JSON` ➔ `Respuesta Visual`

---

## ⚡ Novedades y Manejo de Eventos

Se implementó el enlace de eventos mediante `bind()` para desacoplar la lógica de interfaz de las reglas de negocio:

| Evento | Widget Asociado | Callback / Acción |
| :--- | :--- | :--- |
| `<<TreeviewSelect>>` | Tabla de Usuarios (`ttk.Treeview`) | Carga automáticamente los datos de la fila seleccionada en el formulario de edición sin exponer contraseñas en la tabla. |
| `<Return>` | Entradas de texto (Username / Password) | Permite confirmar y registrar un usuario de manera rápida con la tecla **Enter** reutilizando el callback de registro. |
| `<Escape>` | Formulario / Vista global | Atajo para limpiar los campos, restablecer valores por defecto y cancelar la selección en la tabla. |
| `<<ComboboxSelected>>` | Selector de Rol (`ttk.Combobox`) | Actualiza dinámicamente etiquetas informativas con la descripción del nivel de acceso del rol. |
| `command=` | Botones de Acción | Mantiene el despacho estándar para las acciones de Registrar, Actualizar, Eliminar y Limpiar. |

---

## 👥 Control de Acceso y Roles de Usuario

Se añadió el atributo `rol` en el modelo `Usuario` y en el archivo de persistencia `datos/usuarios.json`:

* **Administrador:**
  * Acceso exclusivo a la pestaña **Gestión de Usuarios**.
  * Capacidad de registrar, actualizar y eliminar registros de tipo Empleado y Cliente.
  * **Regla de seguridad:** Validación para impedir que la cuenta activa en sesión pueda autoeliminarse accidentalmente.
* **Empleado:**
  * Acceso operativo a las secciones de inventario de **Productos** y registro de **Ventas**.
* **Cliente:**
  * Consulta de productos y catálogo sin privilegios administrativos.

---

## 📁 Estructura del Proyecto

```text
restaurante_app/
├── assets/
│   ├── icon_productos.png
│   ├── icon_usuarios.png
│   ├── icon_ventas.png
│   └── logo.png
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── .gitignore
├── main.py
└── README.md
