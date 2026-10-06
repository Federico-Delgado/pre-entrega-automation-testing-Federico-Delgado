"""
Funciones auxiliares reutilizables para el proyecto de pre-entrega.

Este módulo contiene:
- constantes del sitio SauceDemo,
- rutas base del proyecto,
- utilidades para crear carpetas,
- sanitización de nombres de archivo,
- captura de pantalla en caso de fallos.
"""

import os
from datetime import datetime


# Carpeta base del proyecto.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carpeta donde se guardarán reportes, logs y capturas.
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


# ================================
# Constantes del sitio de prueba
# ================================

BASE_URL = "https://www.saucedemo.com/"

USERNAME = "standard_user"
PASSWORD = "secret_sauce"

EXPECTED_INVENTORY_PATH = "/inventory.html"

# Tiempo máximo en segundos para esperas explícitas.
DEFAULT_TIMEOUT = 10


# ================================
# Funciones auxiliares
# ================================


def ensure_directory(directory):
    """
    Crea un directorio si no existe y devuelve su ruta.
    """
    os.makedirs(directory, exist_ok=True)
    return directory


def sanitize_filename(name):
    """
    Convierte un nombre de test en un nombre seguro para archivo.

    Ejemplo:
    test_login_exitoso -> test_login_exitoso
    test login exitoso -> test_login_exitoso
    """
    return "".join(
        char if char.isalnum() or char in ("-", "_") else "_"
        for char in name
    )


def take_screenshot(driver, test_name, directory=None):
    """
    Guarda una captura de pantalla del navegador.

    Args:
        driver: instancia de Selenium WebDriver.
        test_name: nombre del test o descripción de la captura.
        directory: carpeta destino. Por defecto, reports/.

    Returns:
        Ruta completa del archivo guardado, o None si falla.
    """
    target_dir = ensure_directory(directory or REPORTS_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = sanitize_filename(test_name)
    filename = f"{safe_name}_{timestamp}.png"
    filepath = os.path.join(target_dir, filename)

    try:
        driver.save_screenshot(filepath)
        print(f"Captura guardada en: {filepath}")
        return filepath
    except Exception as error:
        print(f"No se pudo guardar la captura '{filename}': {error}")
        return None