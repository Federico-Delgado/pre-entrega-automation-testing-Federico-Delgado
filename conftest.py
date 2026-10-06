"""
Configuración global de Pytest para el proyecto.

Este archivo define:
- el fixture driver, que crea y cierra el navegador por cada test,
- un hook para guardar captura de pantalla cuando un test falla.
"""

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from utils.helpers import take_screenshot


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

    # Descomentar para ejecutar sin interf gráfica, útil más adelante en CI/CD.
    # options.add_argument("--headless=new")

    # Selenium 4 puede gestionar el driver automáticamente mediante Selenium Manager.
    service = Service()

    browser = webdriver.Chrome(service=service, options=options)

    # Timeout de carga de página.
    browser.set_page_load_timeout(30)

    yield browser

    # Cierre seguro del navegador al finalizar cada test.
    browser.quit()


def pytest_exception_interact(node, call, report):
    """
    Hook de Pytest que se ejecuta cuando ocurre una excepción interactuable.

    Lo usamos para guardar una captura de pantalla si el test falla
    durante la ejecución del cuerpo del test.
    """
    if report.when == "call" and report.failed:
        browser = getattr(node, "funcargs", {}).get("driver")

        if browser is not None:
            test_name = getattr(node, "name", "test_fallido")
            take_screenshot(browser, test_name)