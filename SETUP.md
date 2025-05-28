# 🚀 Configuración Rápida - HEVA Booking Assistant

## Nuevas Funcionalidades

### ✅ Selector de Entornos
Ahora puedes seleccionar entre diferentes entornos directamente desde la interfaz:

- **LOCAL** - Para desarrollo local
- **DEV** - Entorno de desarrollo  
- **PROD** - Entorno de producción

### 🔄 Cambio Automático de Conversación
Al cambiar de entorno, la conversación se reinicia automáticamente para evitar conflictos entre diferentes backends.

## Inicio Rápido

1. **Ejecutar la aplicación:**
```bash
streamlit run app.py
```

2. **En la barra lateral:**
   - 🌐 **Selecciona el entorno** (Local/Dev/Prod)
   - 🕐 **Configura tu zona horaria**
   - 🔑 **Introduce tu token de acceso**
   - 👤 **Selecciona tu Provider ID (1-31)**

3. **¡Listo!** Puedes empezar a chatear con el asistente

## Configuración de URLs

Las URLs de los diferentes entornos se configuran en el archivo `config.py`. Este archivo contiene la configuración técnica y no es necesario modificarlo a menos que necesites cambiar las URLs de los entornos:

```python
ENVIRONMENT_URLS = {
    "local": "http://localhost:8000",
    "dev": "https://tu-backend-dev.com",
    "prod": "https://tu-backend-prod.com"
}
```

## Verificación

Si quieres verificar que todo está funcionando correctamente, puedes ejecutar:

```bash
python -c "import app; print('✅ Configuración correcta')"
```

## Funcionalidades Destacadas

- 🔀 **Cambio dinámico de entorno** sin reiniciar la aplicación
- 🌍 **Soporte completo de zonas horarias** con búsqueda
- 🔒 **Interfaz simplificada** con información relevante
- 🔄 **Reinicio automático** de conversación al cambiar entorno
- ⚙️ **Configuración centralizada** en `config.py`

¡Disfruta de la nueva funcionalidad de múltiples entornos! 🎉 