"""
Suite principal de automatización para SauceDemo.

Etapa 2:
Se implementa el caso de prueba de login exitoso.

Flujo automatizado:
1. Abrir página de login.
2. Ingresar credenciales válidas.
3. Hacer clic en Login.
4. Validar redirección a /inventory.html.
5. Validar título Swag Labs.
6. Validar encabezado Products.
"""

import logging

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import (
    BASE_URL,
    DEFAULT_TIMEOUT,
    EXPECTED_INVENTORY_PATH,
    PASSWORD,
    USERNAME,
)


# Logger del módulo.
# Permite registrar pasos de ejecución y facilitar debugging.
logger = logging.getLogger(__name__)


@pytest.mark.login
@pytest.mark.smoke
def test_login_exitoso(driver):
    """
    Caso de prueba: Login exitoso en SauceDemo.

    Valida que un usuario válido pueda ingresar correctamente
    y sea redirigido a la página de inventario.
    """

    # Espera explícita reutilizable para todo el test.
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    logger.info("Abriendo página de login: %s", BASE_URL)
    driver.get(BASE_URL)

    logger.info("Esperando visibilidad del campo de usuario...")
    username_input = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )

    logger.info("Ingresando usuario: %s", USERNAME)
    username_input.clear()
    username_input.send_keys(USERNAME)

    logger.info("Esperando visibilidad del campo de contraseña...")
    password_input = wait.until(
        EC.visibility_of_element_located((By.ID, "password"))
    )

    logger.info("Ingresando contraseña...")
    password_input.clear()
    password_input.send_keys(PASSWORD)

    logger.info("Esperando que el botón de login esté clickeable...")
    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    )

    logger.info("Haciendo clic en el botón de login...")
    login_button.click()

    logger.info("Esperando redirección a la página de inventario...")
    wait.until(EC.url_contains(EXPECTED_INVENTORY_PATH))

    logger.info("Validando que la URL contenga %s", EXPECTED_INVENTORY_PATH)
    assert EXPECTED_INVENTORY_PATH in driver.current_url, (
        f"Se esperaba que la URL contuviera '{EXPECTED_INVENTORY_PATH}', "
        f"pero la URL actual es: {driver.current_url}"
    )

    logger.info("Validando título de la página...")
    assert driver.title == "Swag Labs", (
        f"Se esperaba el título 'Swag Labs', pero se obtuvo: {driver.title}"
    )

    logger.info("Validando encabezado 'Products' en el catálogo...")
    products_header = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.header_secondary_container .title")
        )
    )

    assert "Products" in products_header.text, (
        f"Se esperaba ver 'Products' en el encabezado, "
        f"pero se obtuvo: {products_header.text}"
    )

    logger.info("Login exitoso. Test finalizado correctamente.")