"""
Funciones auxiliares reutilizables para el proyecto de pre-entrega.

Este módulo contiene:
- constantes del sitio SauceDemo,
- selectores reutilizables,
- rutas base del proyecto,
- utilidades para crear carpetas,
- sanitización de nombres de archivo,
- captura de pantalla en caso de fallos,
- funciones auxiliares para login, catálogo y carrito.
"""

import os
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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
EXPECTED_CART_PATH = "/cart.html"

# Tiempo máximo en segundos para esperas explícitas.
DEFAULT_TIMEOUT = 10


# ================================
# Selectores reutilizables
# ================================

SELECTORS = {
    # Login
    "username_input": (By.ID, "user-name"),
    "password_input": (By.ID, "password"),
    "login_button": (By.ID, "login-button"),

    # Catálogo / inventario
    "products_title": (By.CSS_SELECTOR, "div.header_secondary_container .title"),
    "burger_menu_button": (By.ID, "react-burger-menu-btn"),
    "product_sort_container": (By.CSS_SELECTOR, "select.product_sort_container"),
    "shopping_cart_link": (By.CSS_SELECTOR, "a.shopping_cart_link"),

    # Productos
    "inventory_items": (By.CLASS_NAME, "inventory_item"),
    "first_inventory_item": (By.CSS_SELECTOR, "div.inventory_item"),
    "product_name": (By.CLASS_NAME, "inventory_item_name"),
    "product_price": (By.CLASS_NAME, "inventory_item_price"),

    # Carrito
    "add_to_cart_button": (By.CSS_SELECTOR, "button[data-test^='add-to-cart']"),
    "cart_badge": (By.CSS_SELECTOR, "span.shopping_cart_badge"),
    "cart_items": (By.CLASS_NAME, "cart_item"),
    "first_cart_item": (By.CSS_SELECTOR, "div.cart_item"),
    "cart_item_name": (By.CLASS_NAME, "inventory_item_name"),
    "cart_item_price": (By.CLASS_NAME, "inventory_item_price"),
}


# ================================
# Funciones auxiliares generales
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


# ================================
# Funciones auxiliares para Selenium
# ================================


def _wait(driver, timeout=None):
    """
    Devuelve una instancia de WebDriverWait con el timeout configurado.

    Si no se pasa timeout, usa DEFAULT_TIMEOUT.
    """
    return WebDriverWait(driver, timeout or DEFAULT_TIMEOUT)


def login_standard_user(driver, username=USERNAME, password=PASSWORD):
    """
    Realiza el login en SauceDemo con un usuario válido.

    Esta función centraliza el flujo de login para que pueda ser reutilizado
    por distintos tests, manteniendo los casos independientes entre sí.

    Args:
        driver: instancia de Selenium WebDriver.
        username: usuario a ingresar. Por defecto, standard_user.
        password: contraseña a ingresar. Por defecto, secret_sauce.

    Returns:
        La misma instancia del driver, ya posicionada en /inventory.html.
    """
    wait = _wait(driver)

    driver.get(BASE_URL)

    username_input = wait.until(
        EC.visibility_of_element_located(SELECTORS["username_input"])
    )
    username_input.clear()
    username_input.send_keys(username)

    password_input = wait.until(
        EC.visibility_of_element_located(SELECTORS["password_input"])
    )
    password_input.clear()
    password_input.send_keys(password)

    login_button = wait.until(
        EC.element_to_be_clickable(SELECTORS["login_button"])
    )
    login_button.click()

    wait.until(EC.url_contains(EXPECTED_INVENTORY_PATH))

    # Nos aseguramos de que el catálogo ya esté visible antes de devolver el driver.
    wait.until(
        EC.visibility_of_element_located(SELECTORS["products_title"])
    )

    return driver


def obtener_primer_producto(driver):
    """
    Obtiene el nombre y precio del primer producto visible en el catálogo.

    Args:
        driver: instancia de Selenium WebDriver posicionada en /inventory.html.

    Returns:
        Diccionario con la estructura:
        {
            "nombre": "...",
            "precio": "..."
        }
    """
    wait = _wait(driver)

    first_item = wait.until(
        EC.visibility_of_element_located(SELECTORS["first_inventory_item"])
    )

    name_element = first_item.find_element(*SELECTORS["product_name"])
    price_element = first_item.find_element(*SELECTORS["product_price"])

    return {
        "nombre": name_element.text.strip(),
        "precio": price_element.text.strip(),
    }


def esperar_elementos_clave_catalogo(driver):
    """
    Espera y devuelve elementos importantes de la interfaz del catálogo.

    Valida visualmente:
    - botón de menú hamburguesa,
    - filtro/orden de productos,
    - ícono del carrito.

    Args:
        driver: instancia de Selenium WebDriver posicionada en /inventory.html.

    Returns:
        Diccionario con los elementos Web encontrados.
    """
    wait = _wait(driver)

    burger_menu = wait.until(
        EC.visibility_of_element_located(SELECTORS["burger_menu_button"])
    )

    product_sort = wait.until(
        EC.visibility_of_element_located(SELECTORS["product_sort_container"])
    )

    shopping_cart = wait.until(
        EC.visibility_of_element_located(SELECTORS["shopping_cart_link"])
    )

    return {
        "menu": burger_menu,
        "filtro": product_sort,
        "carrito": shopping_cart,
    }


def agregar_primer_producto_al_carrito(driver):
    """
    Agrega el primer producto del catálogo al carrito de compras.

    Antes de hacer clic, lee el nombre y precio del producto para poder
    validarlo después dentro del carrito.

    Args:
        driver: instancia de Selenium WebDriver posicionada en /inventory.html.

    Returns:
        Diccionario con el nombre y precio del producto agregado.
    """
    wait = _wait(driver)

    producto = obtener_primer_producto(driver)

    add_to_cart_button = wait.until(
        EC.element_to_be_clickable(SELECTORS["add_to_cart_button"])
    )
    add_to_cart_button.click()

    return producto


def obtener_contador_carrito(driver):
    """
    Obtiene el valor del contador del carrito de compras.

    Args:
        driver: instancia de Selenium WebDriver posicionada en /inventory.html.

    Returns:
        Texto del badge del carrito, por ejemplo: "1".
    """
    wait = _wait(driver)

    cart_badge = wait.until(
        EC.visibility_of_element_located(SELECTORS["cart_badge"])
    )

    return cart_badge.text.strip()


def navegar_al_carrito(driver):
    """
    Hace clic en el ícono del carrito y espera a estar en la página /cart.html.

    Args:
        driver: instancia de Selenium WebDriver posicionada en /inventory.html.

    Returns:
        La misma instancia del driver, ya posicionada en /cart.html.
    """
    wait = _wait(driver)

    shopping_cart_link = wait.until(
        EC.element_to_be_clickable(SELECTORS["shopping_cart_link"])
    )
    shopping_cart_link.click()

    wait.until(EC.url_contains(EXPECTED_CART_PATH))

    # Esperamos a que al menos un item del carrito esté visible.
    wait.until(
        EC.visibility_of_element_located(SELECTORS["first_cart_item"])
    )

    return driver


def obtener_producto_en_carrito(driver):
    """
    Obtiene el nombre y precio del primer producto listado en el carrito.

    Args:
        driver: instancia de Selenium WebDriver posicionada en /cart.html.

    Returns:
        Diccionario con la estructura:
        {
            "nombre": "...",
            "precio": "..."
        }
    """
    wait = _wait(driver)

    first_cart_item = wait.until(
        EC.visibility_of_element_located(SELECTORS["first_cart_item"])
    )

    name_element = first_cart_item.find_element(*SELECTORS["cart_item_name"])
    price_element = first_cart_item.find_element(*SELECTORS["cart_item_price"])

    return {
        "nombre": name_element.text.strip(),
        "precio": price_element.text.strip(),
    }