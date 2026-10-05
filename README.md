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

## Estado actual

Este repositorio corresponde a la Etapa 1 de la pre-entrega.
Se encuentra configurada:

- Estructura de carpetas.
- Archivo README.md.
- Configuración de Pytest.
- Dependencias básicas.
- Archivo de tests inicial.
- Módulo de utilidades auxiliares.

Próximas etapas:

- **Etapa 2:** implementación del login con Selenium y esperas explícitas.
- **Etapa 3:** verificación del catálogo.
- **Etapa 4:** interacción con carrito de compras.
- **Etapa 5:** reporte HTML, capturas de evidencia y README final.