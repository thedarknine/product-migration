# product-migration

Migrate from OpenProject to Plane using API.

## How to

### Install

```bash
make init
```

### Poetry dependencies management

Add a dependency

```bash
poetry add [package-name]
```

Install dependencies

```bash
poetry install
```

Run python script using poetry

```bash
poetry run python [script-name].py
```

### Modules to install

* python-dotenv
* httpx
* rich
* pytest
* pylint
* black
* arrow

---

## OpenProject API

* https://docs.openproject.org/api/v3/reference/
* https://openproject.leviia.com/api/v3/spec.yml
* https://www.openproject.org/docs/api/endpoints/projects/

---

## Plane API

* Documentation: https://developers.plane.so/api-reference/introduction
* From source code: https://github.com/makeplane/plane/tree/preview/apiserver/plane/api/urls

---

## Python modules

### python-dotenv

* **Description**: Python-dotenv reads key-value pairs from a .env file and can set them as environment variables. It helps in the development of applications following the 12-factor principles.
* **Homepage**: <https://github.com/theskumar/python-dotenv>

### HTTPX

* **Description**: HTTPX is a fully featured HTTP client for Python 3, which provides sync and async APIs, and support for both HTTP/1.1 and HTTP/2.
* **Homepage**: <https://www.python-httpx.org/>

### Rich

* **Description**: Rich is a Python library for rich text and beautiful formatting in the terminal.
* **Homepage**: <https://github.com/Textualize/rich>
* **List of colors**: <https://rich.readthedocs.io/en/latest/appendix/colors.html#appendix-colors>

Usage:

```python
rprint("TEST Rich Python")
console.print("Hello, World", style = cyan_style + Style(underline=True))
console.print("Danger, Will Robinson!", style=danger_style)
```

### pytest

* **Description**: The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.
* **Homepage**: <https://docs.pytest.org/>

### Pylint

* **Description**: Pylint is a static code analyser for Python 2 or 3.
* **Homepage**: <https://pylint.readthedocs.io/en/stable/>

### Black

* **Description**: Black is the uncompromising Python code formatter.
* **Homepage**: <https://github.com/psf/black>

### Arrow

* **Description**: Arrow is a Python library that offers a sensible and human-friendly approach to creating, manipulating, formatting and converting dates, times and timestamps.
* **Homepage**: <https://arrow.readthedocs.io/>
