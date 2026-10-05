"""
Suite principal de automatización para SauceDemo.

Etapa 1:
Se crea el archivo base del proyecto.

En etapas siguientes se implementarán los casos obligatorios:
1. Login exitoso.
2. Navegación y verificación del catálogo.
3. Interacción con productos y carrito.
"""


def test_estructura_inicial():
    """
    Smoke test simple para validar que Pytest encuentra la carpeta tests/
    y que el proyecto está correctamente configurado.
    """
    assert True


# TODO Etapa 2:
# - Importar pytest, selenium, By, WebDriverWait y expected_conditions.
# - Implementar test_login_exitoso con marcador @pytest.mark.login.

# TODO Etapa 3:
# - Implementar test_verificar_catalogo con marcador @pytest.mark.catalogo.

# TODO Etapa 4:
# - Implementar test_agregar_producto_al_carrito con marcador @pytest.mark.carrito.