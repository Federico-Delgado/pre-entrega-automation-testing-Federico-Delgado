"""
Configuración global de Pytest para el proyecto.

Este archivo define:
- el fixture driver, que crea y cierra el navegador por cada test;
- la creación automática de la carpeta reports/;
- un hook para guardar captura de pantalla cuando un test falla.
"""

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from utils.helpers import REPORTS_DIR, ensure_directory, take_screenshot


def pytest_configure(config):
    """
    Asegura que la carpeta reports/ exista antes de ejecutar los tests.

    Esto es útil para:
    - reporte HTML;
    - logs;
    - capturas de pantalla automáticas.
    """
    ensure_directory(REPORTS_DIR)


@pytest.fixture(scope="function")
def driver():
    """
    Fixture que crea una instancia de ChromeDriver para cada test.

    Scope function:
        Cada test recibe un navegador nuevo.
        Esto garantiza independencia entre pruebas.
    """
    options = Options()

    # Ventana maximizada para facilitar la visualización manual.
    options.add_argument("--start-maximized")

    # Opcionales para mayor estabilidad en algunos entornos.
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Descomentar para ejecutar sin interfaz gráfica, útil más adelante en CI/CD.
    # options.add_argument("--headless=new")

    # Selenium 4 puede gestionar el driver automáticamente mediante Selenium Manager.
    service = Service()

    browser = webdriver.Chrome(service=service, options=options)

    # Timeout de carga de página.
    browser.set_page_load_timeout(30)

    yield browser

    # Cierre seguro del navegador al finalizar cada test.
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de Pytest para capturar el resultado de cada fase del test.

    Si el test falla durante la fase call, se guarda una captura de pantalla
    automáticamente en la carpeta reports/.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        browser = getattr(item, "funcargs", {}).get("driver")

        if browser is not None:
            test_name = getattr(item, "name", "test_fallido")
            take_screenshot(browser, test_name)