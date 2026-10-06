# Pre-Entrega Automation Testing - SauceDemo

Proyecto de automatización de pruebas web utilizando **Python**, **Pytest** y **Selenium WebDriver**.

El sitio de prueba es:

https://www.saucedemo.com/

---

## Propósito del proyecto

El objetivo de este proyecto es automatizar flujos básicos de navegación web en SauceDemo, aplicando buenas prácticas de testing automatizado.

Se automatizan tres funcionalidades principales:

1. **Login exitoso**
2. **Navegación y verificación del catálogo**
3. **Interacción con productos y carrito de compras**

El proyecto demuestra el uso de:

- Selenium WebDriver;
- Pytest;
- esperas explícitas;
- fixtures;
- markers;
- funciones auxiliares reutilizables;
- generación de reporte HTML;
- logs de ejecución;
- capturas automáticas en caso de fallo;
- control de versiones con Git y GitHub.

---

## Tecnologías utilizadas

- Python 3.11
- Pytest
- Selenium WebDriver
- pytest-html
- Git
- GitHub
- Visual Studio Code
- Git Bash

---

## Estructura del proyecto

```text
pre-entrega-automation-testing-[nombre-apellido]/
│
├── data/
│   └── .gitkeep
│
├── reports/
│   ├── .gitkeep
│   ├── reporte.html
│   ├── pytest.log
│   └── evidencia_captura_fallo.png
│
├── tests/
│   ├── __init__.py
│   └── test_saucedemo.py
│
├── utils/
│   ├── __init__.py
│   └── helpers.py
│
├── .gitignore
├── conftest.py
├── pytest.ini
├── README.md
└── requirements.txt
```

### Descripción de carpetas y archivos

| Ruta | Descripción |
|---|---|
| `tests/` | Contiene los casos de prueba automatizados. |
| `utils/` | Contiene funciones auxiliares reutilizables. |
| `data/` | Carpeta reservada para datos externos, si aplican. |
| `reports/` | Contiene reporte HTML, logs y capturas de evidencia. |
| `conftest.py` | Configuración global de Pytest, fixture de navegador y hook de captura automática. |
| `pytest.ini` | Configuración de Pytest, markers y logs. |
| `requirements.txt` | Dependencias del proyecto. |
| `README.md` | Documentación del proyecto. |

---

## Requisitos previos

Se recomienda tener instalado:

- Python 3.11
- Google Chrome
- Git
- Visual Studio Code

---

## Instalación del entorno virtual

Este proyecto utiliza un entorno virtual para aislar las dependencias.

Desde la raíz del proyecto, en Git Bash:

```bash
py -3.11 -m venv .venv
```

Activar el entorno virtual:

```bash
source .venv/Scripts/activate
```

Actualizar herramientas básicas de Python:

```bash
python -m pip install --upgrade pip setuptools wheel
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Dependencias del proyecto

El archivo `requirements.txt` incluye:

```txt
selenium>=4.20.0
pytest>=8.0.0
pytest-html>=4.1.0
```

---

## Credenciales de prueba

Usuario:

```text
standard_user
```

Contraseña:

```text
secret_sauce
```

---

## Ejecución de pruebas

Ejecutar todos los tests:

```bash
pytest -v
```

Ejecutar solo el archivo de tests de SauceDemo:

```bash
pytest tests/test_saucedemo.py -v
```

Ejecutar solo el test de login:

```bash
pytest tests/test_saucedemo.py::test_login_exitoso -v
```

Ejecutar solo el test de catálogo:

```bash
pytest tests/test_saucedemo.py::test_verificar_catalogo -v
```

Ejecutar solo el test de carrito:

```bash
pytest tests/test_saucedemo.py::test_interaccion_con_producto_y_carrito -v
```

---

## Ejecución por markers

El proyecto utiliza markers personalizados de Pytest.

Ejecutar tests de login:

```bash
pytest -m login -v
```

Ejecutar tests de catálogo:

```bash
pytest -m catalogo -v
```

Ejecutar tests de carrito:

```bash
pytest -m carrito -v
```

Ejecutar tests smoke:

```bash
pytest -m smoke -v
```

---

## Generación de reporte HTML

Para generar el reporte HTML final:

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html --self-contained-html
```

El reporte se genera en:

```text
reports/reporte.html
```

---

## Logs de ejecución

El archivo `pytest.ini` configura la generación de logs en:

```text
reports/pytest.log
```

Este archivo contiene el registro de ejecución de los tests y sirve como evidencia adicional.

---

## Capturas automáticas en caso de fallo

El archivo `conftest.py` implementa un hook de Pytest que guarda una captura de pantalla automáticamente cuando un test falla.

Las capturas se guardan en:

```text
reports/
```

Como evidencia del funcionamiento de esta característica, se incluye el archivo:

```text
reports/evidencia_captura_fallo.png
```

Esta captura fue generada mediante un test controlado que falló a propósito para validar el mecanismo automático de captura.

---

## Casos de prueba automatizados

### 1. Login exitoso

Archivo:

```text
tests/test_saucedemo.py
```

Test:

```python
test_login_exitoso
```

Valida:

- navegación a `https://www.saucedemo.com/`;
- ingreso de usuario `standard_user`;
- ingreso de contraseña `secret_sauce`;
- clic en botón de login;
- espera explícita por redirección;
- validación de URL `/inventory.html`;
- validación de título `Swag Labs`;
- validación de encabezado `Products`.

Marker:

```bash
pytest -m login -v
```

---

### 2. Navegación y verificación del catálogo

Test:

```python
test_verificar_catalogo
```

Valida:

- título de la página `Swag Labs`;
- encabezado visible `Products`;
- presencia de productos visibles;
- lectura del nombre del primer producto;
- lectura del precio del primer producto;
- presencia de elementos clave de interfaz:
  - menú hamburguesa;
  - filtro/orden de productos;
  - ícono del carrito.

Marker:

```bash
pytest -m catalogo -v
```

---

### 3. Interacción con productos y carrito

Test:

```python
test_interaccion_con_producto_y_carrito
```

Valida:

- login previo;
- lectura del primer producto del catálogo;
- clic en botón `Add to cart`;
- incremento del contador del carrito a `1`;
- navegación al carrito;
- validación de URL `/cart.html`;
- presencia del producto en el carrito;
- comparación de nombre y precio entre catálogo y carrito.

Marker:

```bash
pytest -m carrito -v
```

---

## Independencia de los tests

Cada test utiliza el fixture `driver` con scope `function`.

Esto significa que cada test:

- abre un navegador nuevo;
- ejecuta su propio flujo;
- cierra el navegador al finalizar.

Por lo tanto, la falla de un test no afecta a los demás.

---

## Buenas prácticas aplicadas

El proyecto aplica las siguientes buenas prácticas:

- uso de entorno virtual;
- separación entre tests y funciones auxiliares;
- uso de constantes para URLs, credenciales y timeouts;
- centralización de selectores;
- uso de esperas explícitas con `WebDriverWait` y `expected_conditions`;
- evitar `time.sleep()`;
- tests independientes;
- nombres descriptivos;
- comentarios y docstrings;
- logs de ejecución;
- reporte HTML;
- capturas automáticas en fallos;
- commits descriptivos;
- `.gitignore` para no subir artefactos innecesarios.

---

## Comandos útiles

Verificar versión de Python:

```bash
python --version
```

Ver paquetes instalados:

```bash
pip list
```

Ejecutar todos los tests:

```bash
pytest -v
```

Ejecutar tests y generar reporte HTML:

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html --self-contained-html
```

---

## Autor

Proyecto desarrollado como pre-entrega del curso de Automatización QA.

Sitio de prueba: SauceDemo.

Herramientas principales: Python, Pytest y Selenium WebDriver.