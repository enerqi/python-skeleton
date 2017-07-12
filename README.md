# Python-Skeleton

Utility for creating a python project skeleton

```bash

./python-new-project.sh NAME
```



# Notes

## Virtual Environment

It's easy to get library/tool version mismatches when not working in an isolated environment on a development machine. It is more feasible to install globally if using something like jails/docker.

- Install [https://docs.continuum.io/anaconda/install](Anaconda) for isolated environment management. Virtualenv could also be used but anaconda has better support for building non-python code.
- Add `~/anaconda3/bin` (or anaconda etc. as per install documentation) to the front of PATH (so it comes before globally installed python)
- `conda create -n projectname` to create a new virtual environment somewhere under ~/anaconda3.
- `source (activate|deactivate) projectname` to use/turn off that isolated environment.
- Normally we need to make the IDE/editor/tools aware of which python interpreter we are using per project, e.g. `~//anaconda3/envs/my-environment-name/bin/python`.
- Use `pip` to install any required dependencies into the isolated environment: `pip install -r requirements-to-freeze.txt` (or requirements.txt etc.)
- Freeze the versions when the project stabilises: `pip freeze > requirements.txt`

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

## Pytest.ini to enable doctests and ignore pointless directories

```
[pytest]
addopts = --doctest-modules --ignore build
```

## Running 'main' type python files (if part of package)

Running something like `app/main.py` within a project results in import errors as the main file does not know it is part of a package. Both setting the `PYTHONPATH` and doing `sys.path.insert` stuff seems ugly. See [http://stackoverflow.com/questions/1893598/pythonpath-vs-sys-path](stackoverflow).

A shell script per runnable main file seems a reasonable approach, for example:

```bash
#!/bin/bash
BASEDIR=$(dirname "$0")
PYTHONPATH=$BASEDIR python3 app/main.py
```

## Running pytest tests and lints from setup.py

Install the python plugin dependency `pytest-runner` with `pip install pytest-runner` (or via requirements.txt) inside the virtual environment for the tests. Install `flake8` and `mccabe` for linting. Edit `setup.py`:

```
setup(
    #...,
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest', ...],
    #...,
)
```

Make a `setup.cfg` file. The options from pytest.ini are duplicated into [tool:pytest].

```
[aliases]
test=pytest

[tool:pytest]
addopts = --doctest-modules --ignore build

[flake8]
max-line-length = 120
```

`python setup.py test` and `python setup.py flake8` now run tests and do linting (or `python3 ...` when run globally).


## Coverage reports on tests

Install the python dependency `pytest-cov` into the virtual environment. See `pytest --help`. For example, to run coverage in html or xml on `mymodule` and submodules.

`pytest --cov-report=html|xml --cov=mymodule` or `pytest --cov=mymodule` to print to terminal.

## Type hint documentation

If using python3 and specificaly python3.5+ we can use type hints, that at least serve as minimal documentation.

The [http://mypy.readthedocs.io/en/latest/](mypy) project is a linter that will try to check those types statically. It is however, an alpha status project, despite being > 5 years old.

To make mypy quiet when it finds 3rd party code that does not have any type annotations have a `mypy.ini` file:

```
[mypy]
python_version = 3.6
ignore_missing_imports = true
```
