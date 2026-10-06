"""
Suite principal de automatización para SauceDemo.

Etapa 2:
- Login exitoso.

Etapa 3:
- Navegación y verificación del catálogo.

Flujos automatizados:
1. Login exitoso.
2. Verificación del catálogo:
   - título correcto,
   - presencia de productos,
   - nombre y precio del primer producto,
   - elementos clave de interfaz.
"""

import logging

import pytest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import (
    DEFAULT_TIMEOUT,
    EXPECTED_INVENTORY_PATH,
    SELECTORS,
    esperar_elementos_clave_catalogo,
    login_standard_user,
    obtener_primer_producto,
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

    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    logger.info("Iniciando prueba de login exitoso.")

    # Reutilizamos la función auxiliar de login.
    login_standard_user(driver)

    logger.info("Validando redirección a la página de inventario.")
    assert EXPECTED_INVENTORY_PATH in driver.current_url, (
        f"Se esperaba que la URL contuviera '{EXPECTED_INVENTORY_PATH}', "
        f"pero la URL actual es: {driver.current_url}"
    )

    logger.info("Validando título de la pestaña.")
    assert driver.title == "Swag Labs", (
        f"Se esperaba el título 'Swag Labs', pero se obtuvo: {driver.title}"
    )

    logger.info("Validando encabezado 'Products' en el catálogo.")
    products_header = wait.until(
        EC.visibility_of_element_located(SELECTORS["products_title"])
    )

    assert products_header.text.strip() == "Products", (
        f"Se esperaba ver 'Products' en el encabezado, "
        f"pero se obtuvo: {products_header.text}"
    )

    logger.info("Login exitoso validado correctamente.")


@pytest.mark.catalogo
@pytest.mark.smoke
def test_verificar_catalogo(driver):
    """
    Caso de prueba: Navegación y verificación del catálogo.

    Valida que, luego de iniciar sesión, la página de inventario muestre:
    - título correcto,
    - productos visibles,
    - nombre y precio del primer producto,
    - elementos importantes de la interfaz.
    """

    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    logger.info("Iniciando prueba de verificación de catálogo.")

    # Cada test es independiente: vuelve a hacer login desde cero.
    login_standard_user(driver)

    # ----------------------------------------------------
    # 1. Validar título de la página de inventario
    # ----------------------------------------------------

    logger.info("Validando título de la pestaña del navegador.")
    assert driver.title == "Swag Labs", (
        f"Se esperaba el título 'Swag Labs', pero se obtuvo: {driver.title}"
    )

    logger.info("Validando encabezado visible 'Products'.")
    products_title = wait.until(
        EC.visibility_of_element_located(SELECTORS["products_title"])
    )

    assert products_title.text.strip() == "Products", (
        f"Se esperaba que el encabezado fuera 'Products', "
        f"pero se obtuvo: {products_title.text}"
    )

    # ----------------------------------------------------
    # 2. Comprobar que existan productos visibles
    # ----------------------------------------------------

    logger.info("Buscando productos visibles en el catálogo.")
    inventory_items = driver.find_elements(*SELECTORS["inventory_items"])

    assert len(inventory_items) > 0, (
        "Se esperaba encontrar al menos un producto visible en el catálogo, "
        "pero no se encontró ninguno."
    )

    logger.info("Cantidad de productos encontrados: %s", len(inventory_items))

    # ----------------------------------------------------
    # 3. Listar nombre y precio del primer producto
    # ----------------------------------------------------

    logger.info("Obteniendo nombre y precio del primer producto.")
    first_product = obtener_primer_producto(driver)

    assert first_product["nombre"] != "", (
        "Se esperaba que el primer producto tuviera un nombre visible."
    )

    assert first_product["precio"] != "", (
        "Se esperaba que el primer producto tuviera un precio visible."
    )

    assert first_product["precio"].startswith("$"), (
        f"Se esperaba que el precio comenzara con '$', "
        f"pero se obtuvo: {first_product['precio']}"
    )

    logger.info(
        "Primer producto -> nombre: %s | precio: %s",
        first_product["nombre"],
        first_product["precio"],
    )

    # ----------------------------------------------------
    # 4. Validar elementos importantes de la interfaz
    # ----------------------------------------------------

    logger.info("Validando elementos clave de la interfaz del catálogo.")
    interface_elements = esperar_elementos_clave_catalogo(driver)

    assert interface_elements["menu"].is_displayed(), (
        "El botón de menú hamburguesa no está visible."
    )

    assert interface_elements["filtro"].is_displayed(), (
        "El filtro/orden de productos no está visible."
    )

    assert interface_elements["carrito"].is_displayed(), (
        "El ícono del carrito no está visible."
    )

    logger.info("Catálogo validado correctamente.")