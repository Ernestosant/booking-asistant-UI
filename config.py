from pathlib import Path



# Default environment
DEFAULT_ENVIRONMENT = "local"

# Environment descriptions for UI
ENVIRONMENT_DESCRIPTIONS = {
    "local": "Desarrollo Local - Para pruebas en el entorno local",
    "dev": "Desarrollo - Entorno de desarrollo en Google Cloud",
    "prod": "Producción - Entorno de producción en Google Cloud"
}

# API Configuration
API_TIMEOUT = 300  # seconds
API_MAX_RETRIES = 5
API_RETRY_DELAY = 1  # seconds

# Logging Configuration
LOG_LEVEL = "DEBUG"
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s' 