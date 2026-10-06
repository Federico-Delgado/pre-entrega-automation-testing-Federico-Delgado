# Pre-Entrega Automation Testing - SauceDemo

Proyecto de automatización de pruebas web utilizando Python, Pytest y Selenium WebDriver.

El sitio de prueba es:

https://www.saucedemo.com/

## Propósito del proyecto

Automatizar flujos básicos de navegación web en SauceDemo, contemplando:

1. Login exitoso.
2. Navegación y verificación del catálogo.
3. Interacción con productos y carrito de compras.

## Tecnologías utilizadas

- Python
- Pytest
- Selenium WebDriver
- pytest-html
- Git
- GitHub

## Estructura del proyecto

```text
pre-entrega-automation-testing-[nombre-apellido]/
│
├── data/
├── reports/
├── tests/
│   ├── __init__.py
│   └── test_saucedemo.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

## Instalación de dependencias

Se recomienda trabajar con un entorno virtual para aislar las dependencias del proyecto.

Con python 3.11 y Git Bash en VS Code. Desde la raíz del proyecto:

```bash
py -3.11 -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## Ejecución de pruebas

Ejecutar todos los tests:

```bash
pytest -v
```

Ejecutar generando reporte HTML:

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html --self-contained-html
```

## Credenciales de prueba

- **Usuario:**

```text
standard_user
```

- **Contraseña:**

```text
secret_sauce
```

## Etapa 1: Creacion de la estructura del proyecto

Este repositorio corresponde a la Etapa 1 de la pre-entrega.
Se encuentra configurada:

- Estructura de carpetas.
- Archivo README.md.
- Configuración de Pytest.
- Dependencias básicas.
- Archivo de tests inicial.
- Módulo de utilidades auxiliares.

## Etapa 2: Implementación del login con Selenium y esperas explícitas

### Qué valida

- Que se pueda navegar correctamente a la página de login de SauceDemo.
- Que el formulario de login cargue utilizando esperas explícitas.
- Que se puedan ingresar credenciales válidas:
  - Usuario: `standard_user`
  - Contraseña: `secret_sauce`
- Que al hacer clic en el botón de login se produzca una redirección válida.
- Que la URL final contenga `/inventory.html`.
- Que el título de la página sea `Swag Labs`.
- Que el encabezado del catálogo muestre el texto `Products`.

### Ejecutar por marcador

Ejecutar únicamente la prueba de login:

```bash
pytest -m login -v
```

### Generar reporte HTML de la Etapa 2

Generar el reporte HTML con los resultados del test de login:

```bash
pytest tests/test_saucedemo.py::test_login_exitoso -v --html=reports/reporte_etapa2.html --self-contained-html
```

## Etapa 3: Navegación y verificación del catálogo

En esta etapa se implementó el caso de prueba `test_verificar_catalogo`.

### Qué valida

- Que luego del login se llegue correctamente a `/inventory.html`.
- Que el título del navegador sea `Swag Labs`.
- Que el encabezado visible de la página sea `Products`.
- Que existan productos

### Ejecutar por marcador

Ejecutar únicamente la prueba de catalogo:

```bash
pytest -m catalogo -v
```

### Generar reporte HTML de la Etapa 3

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte_etapa3.html --self-contained-html
```

## Etapa 4: Interacción con productos y carrito de compras

### Qué valida

- Que se pueda iniciar sesión correctamente en SauceDemo.
- Que se pueda leer el nombre y precio del primer producto del catálogo.
- Que se pueda agregar el primer producto al carrito haciendo clic en el botón correspondiente.
- Que el contador del carrito se incremente correctamente y muestre `1`.
- Que se pueda navegar al carrito de compras.
- Que la URL del carrito contenga `/cart.html`.
- Que el producto agregado aparezca correctamente listado en el carrito.
- Que el nombre y precio del producto en el carrito coincidan con los del catálogo.

### Ejecutar solo el test de carrito

```bash
pytest tests/test_saucedemo.py::test_interaccion_con_producto_y_carrito -v
```

### Ejecutar por marcador

```bash
pytest -m carrito -v
```

### Generar reporte HTML de la Etapa 4

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte_etapa4.html --self-contained-html
```

## Estado actual

El proyecto avanza por etapas.

### Etapa 1: completada
- Creación del repositorio.
- Estructura inicial de carpetas.
- Configuración de Pytest.
- Dependencias básicas.
- Archivo de utilidades inicial.

### Etapa 2: completada
- Automatización del login exitoso.
- Uso de Selenium WebDriver.
- Esperas explícitas con WebDriverWait y expected_conditions.
- Fixture de navegador.
- Logs de ejecución.
- Captura automática en caso de fallo.

### Etapa 3: completada
- Verificación del catálogo.
- Validación de título.
- Validación de presencia de productos.
- Lectura de nombre y precio del primer producto.
- Validación de elementos clave de interfaz.

### Etapa 4: completada
- Interacción con productos.
- Agregado del primer producto al carrito.
- Validación del contador del carrito.
- Navegación al carrito de compras.
- Verificación del producto agregado en el carrito.
- Comparación de nombre y precio entre catálogo y carrito.

### Próximas etapas
- Etapa 5: reporte final, evidencias, limpieza y README definitivo.