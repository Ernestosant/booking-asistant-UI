"""
Configuration file for HEVA Booking Assistant
Contains environment URLs and other configuration settings
"""

import tomli
from pathlib import Path

# Load secrets from secrets.toml
def load_secrets():
    secrets_path = Path(__file__).parent / "secrets.toml"
    with open(secrets_path, "rb") as f:
        return tomli.load(f)

# Load environment URLs from secrets
secrets = load_secrets()
ENVIRONMENT_URLS = secrets["environment_urls"]

# Default environment
DEFAULT_ENVIRONMENT = "local"

# Environment descriptions for UI
ENVIRONMENT_DESCRIPTIONS = {
    "local": "Desarrollo Local - Para pruebas en el entorno local",
    "dev": "Desarrollo - Entorno de desarrollo en Google Cloud",
    "prod": "Producción - Entorno de producción en Google Cloud"
}

# API Configuration
API_TIMEOUT = 30  # seconds
API_MAX_RETRIES = 5
API_RETRY_DELAY = 1  # seconds

# Logging Configuration
LOG_LEVEL = "DEBUG"
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s' 