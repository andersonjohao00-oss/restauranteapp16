# Restaurante App - Gestión de Eventos y Ventas (Semana 15)

Evolución modular del sistema de restaurante orientada a eventos básicos en Tkinter.

## Novedades Semana 15
- **Manejo de Eventos**: Implementación de `command=` y callbacks vinculados a la interacción del usuario sin bloquear la interfaz.
- **Entidad Venta**: Modelo desacoplado `Venta` con persistencia en `datos/ventas.json`.
- **Arquitectura en Capas**: Flujo estricto `Usuario -> Vista -> Callback -> RestauranteServicio -> Persistencia -> UI`.
- **Identidad Visual**: Soporte estructurado de íconos y marca institucional en la carpeta `assets/`.

## Ejecución
```bash
python main.py