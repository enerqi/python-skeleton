# Python-Skeleton

Command line utility for creating a python project skeleton. Requires python 3 to run.

Examples:

```bash

python3 python-new-project.py myproject   # create a new project in ./myproject
python3 python-new-project.py /path/to/myproject   # create a new project in /path/to/myproject
python3 python-new-project.py myproject --force  # create the new project overwriting any existing skeleton files
```

---

# Notes

## Virtual Environment

It's easy to get library/tool version mismatches when not working in an isolated environment on a development machine. It is more feasible to install globally if using something like jails/docker.

- [Pipenv](https://pipenv.org/) is the latest python tooling for creating virtual environments and dealing with dependencies. One problem I've seen
so far is that you can't update the version of one dependency without trying to update every dependency to latest even when unnecessary.
- [Anaconda](https://docs.continuum.io/anaconda/install) is a tool for creating isolated environment management. Virtualenv could also be used but anaconda has better support for building non-python code. When using Pipenv you probably are not going to need it, though pipenv might be
able to use an arbritrary environment.
- `pip` and `virtualenv` can be avoided when using Pipenv - pipenv uses them in its implementation.
- `pip-tools` is a good option for carefully managing production and development dependencies if not using `pipenv`.


## Import Style

Prefer absolute imports, otherwise I find at least one of flask or pytest or the editor/IDE have some import problem.
Pep-008 recommends absolute imports or maybe explicit relative imports. Implicit relative imports are removed from python 3.

```python
import mypkg.sibling
import mypkg.sibling as sibling
from mypkg import sibling
from mypkg.sibling import example
from . import sibling  # relative
from .sibling import example  # relative
```

## Tool config

Most tools (e.g. coverage, pytest, flake8, mypy) now allow their config to go in the one file `setup.cfg` instead of
requiring their own file (e.g. `mypy.ini`, `.flake`, and `pytest.ini`).

### Pytest

```ini
[tool:pytest]
addopts = --doctest-modules --ignore build
```

### MyPy

```ini
[mypy]
python_version = 3.6
ignore_missing_imports = true
```

Makes mypy quiet when it finds 3rd party code that does not have any type annotations.

## Running 'main' type python files (if part of package)

Running something like `app/main.py` within a project results in import errors as the main file does not know it is part of a package. Both setting the `PYTHONPATH` and doing `sys.path.insert` stuff seems ugly. See [Stackoverflow](http://stackoverflow.com/questions/1893598/pythonpath-vs-sys-path).

A shell script per runnable main file seems a reasonable approach, for example:

```bash
#!/bin/bash
BASEDIR=$(dirname "$0")
PYTHONPATH=$BASEDIR python3 app/main.py
```

## Running pytest tests and lints from setup.py

We use the [PBR](https://docs.openstack.org/pbr/latest/) build library to help with such things. With `pytest-runner` as a setup dependency and
setting `test` as an alias for pytest in the `setup.cfg` file it just works.

## Coverage reports on tests

Install the python dependency `pytest-cov` into the virtual environment.
See `pytest --help`. For example, to run coverage in html or xml on `mymodule` and submodules.

`pytest --cov-report=html|xml --cov=mymodule` or `pytest --cov=mymodule` to print to terminal.

## Type hint linting and documentation

If using python3 and specificaly python3.5+ we can use type hints, that at least serves as minimal documentation and
provides some support for type driven development / domain modelling.

The [MyPy](http://mypy.readthedocs.io/en/latest/) project is a linter that will try to check those types statically.
It is however, an alpha status project, despite being > 5 years old.

## Enabling doctests in combination with pytest & flask

Putting this pytest `conftest.py` file in the main package directory(s) to fix this pytest/doctest/flask combination issue.

```python
"""Pytest configuration module to fix pytest/doctest-discovery/flask interaction issue."""
import importlib


def pytest_configure():
    patch_flask_for_doctest()


def patch_flask_for_doctest():
    """
    Patch flask magic objects to keep them from raising
    RuntimeErrors during doctest discovery.
    https://github.com/pallets/flask/issues/1680
    """
    flask = importlib.import_module('flask')
    object.__setattr__(flask.request, '__wrapped__', None)
    object.__setattr__(flask.session, '__wrapped__', None)
    object.__setattr__(flask.current_app, '__wrapped__', None)
```
