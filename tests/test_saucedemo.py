"""
Suite principal de automatización para SauceDemo.

Etapa 2:
- Login exitoso.

Etapa 3:
- Navegación y verificación del catálogo.

Etapa 4:
- Interacción con productos y carrito de compras.

Flujos automatizados:
1. Login exitoso.
2. Verificación del catálogo.
3. Agregado de producto al carrito y validación del carrito.
"""

import logging

import pytest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import (
    DEFAULT_TIMEOUT,
    EXPECTED_CART_PATH,
    EXPECTED_INVENTORY_PATH,
    SELECTORS,
    agregar_primer_producto_al_carrito,
    esperar_elementos_clave_catalogo,
    login_standard_user,
    obtener_contador_carrito,
    obtener_producto_en_carrito,
    obtener_primer_producto,
    navegar_al_carrito,
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


@pytest.mark.carrito
@pytest.mark.smoke
def test_interaccion_con_producto_y_carrito(driver):
    """
    Caso de prueba: Interacción con productos y carrito de compras.

    Valida que:
    - se pueda agregar el primer producto al carrito;
    - el contador del carrito se incremente a 1;
    - se pueda navegar al carrito;
    - el producto agregado aparezca correctamente en el carrito;
    - el nombre y precio del producto en el carrito coincidan con los del catálogo.
    """

    logger.info("Iniciando prueba de interacción con producto y carrito.")

    # Cada test es independiente: vuelve a hacer login desde cero.
    login_standard_user(driver)

    # ----------------------------------------------------
    # 1. Agregar el primer producto al carrito
    # ----------------------------------------------------

    logger.info("Agregando el primer producto al carrito.")
    producto_agregado = agregar_primer_producto_al_carrito(driver)

    assert producto_agregado["nombre"] != "", (
        "Se esperaba que el producto agregado tuviera un nombre visible."
    )

    assert producto_agregado["precio"] != "", (
        "Se esperaba que el producto agregado tuviera un precio visible."
    )

    logger.info(
        "Producto agregado desde catálogo -> nombre: %s | precio: %s",
        producto_agregado["nombre"],
        producto_agregado["precio"],
    )

    # ----------------------------------------------------
    # 2. Verificar que el contador del carrito sea 1
    # ----------------------------------------------------

    logger.info("Validando contador del carrito.")
    contador_carrito = obtener_contador_carrito(driver)

    assert contador_carrito == "1", (
        f"Se esperaba que el contador del carrito mostrara '1', "
        f"pero mostró: {contador_carrito}"
    )

    logger.info("Contador del carrito validado correctamente: %s", contador_carrito)

    # ----------------------------------------------------
    # 3. Navegar al carrito de compras
    # ----------------------------------------------------

    logger.info("Navegando al carrito de compras.")
    navegar_al_carrito(driver)

    assert EXPECTED_CART_PATH in driver.current_url, (
        f"Se esperaba que la URL contuviera '{EXPECTED_CART_PATH}', "
        f"pero la URL actual es: {driver.current_url}"
    )

    logger.info("Redirección al carrito validada correctamente.")

    # ----------------------------------------------------
    # 4. Verificar que el producto agregado aparezca en el carrito
    # ----------------------------------------------------

    logger.info("Obteniendo producto listado en el carrito.")
    producto_en_carrito = obtener_producto_en_carrito(driver)

    assert producto_en_carrito["nombre"] != "", (
        "Se esperaba que el carrito mostrara un producto con nombre visible."
    )

    assert producto_en_carrito["precio"] != "", (
        "Se esperaba que el carrito mostrara un producto con precio visible."
    )

    logger.info(
        "Producto en carrito -> nombre: %s | precio: %s",
        producto_en_carrito["nombre"],
        producto_en_carrito["precio"],
    )

    # ----------------------------------------------------
    # 5. Validar que el producto del carrito sea el mismo agregado
    # ----------------------------------------------------

    assert producto_en_carrito["nombre"] == producto_agregado["nombre"], (
        f"El nombre del producto en el carrito no coincide.\n"
        f"Esperado: {producto_agregado['nombre']}\n"
        f"Obtenido: {producto_en_carrito['nombre']}"
    )

    assert producto_en_carrito["precio"] == producto_agregado["precio"], (
        f"El precio del producto en el carrito no coincide.\n"
        f"Esperado: {producto_agregado['precio']}\n"
        f"Obtenido: {producto_en_carrito['precio']}"
    )

    logger.info("Producto agregado y validado correctamente en el carrito.")