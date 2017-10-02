#!/bin/bash

set -u # Exit if we try to use an uninitialised variable
set -e # Return early if any command returns a non-0 exit status

if [[ $# -eq 0 ]]
  then
    echo "provide a project name" && exit 1
fi

NAME=$1
echo Making new project in directory ${NAME}

if [[ -d ${NAME} ]]
    then
        directoryAlreadyExisted=true
    else
        directoryAlreadyExisted=false
fi

mkdir -p ${NAME}
mkdir -p ${NAME}/app

function cleanupFailedAttempt {
    if [[ $directoryAlreadyExisted = false ]]
        then
            rm -rf ${NAME}
    fi
}
trap cleanupFailedAttempt ERR


function write_setuppy {
    cat > ${NAME}/setup.py <<EOL
from setuptools import setup

setup(setup_requires=['flake8', 'pbr', 'pytest-runner'],
      pbr=True,
      tests_require=['pytest'])
EOL
}

function write_setup_cfg {
    cat > ${NAME}/setup.cfg <<EOL
[flake8]
max-line-length = 120

[aliases]
test=pytest

[test]
addopts = tests

[pytest]
addopts = --cov app --doctest-modules --ignore build --verbose

[metadata]
name =
author =
author-email =
summary =
description-file = README.md
home-page =
requires-python = >= 3.6

[files]
packages =
    app

EOL
}

function write_gitignore {
                      # Quoting heredoc string to turn off variable injection with $
    cat > ${NAME}/.gitignore <<"EOL"
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*,cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# dotenv
.env

# virtualenv
.venv/
venv/
ENV/

# Spyder project settings
.spyderproject

# Rope project settings
.ropeproject

# Sublime text
*.sublime-workspace

# Intellij - user specfic
.idea/workspace.xml
.idea/tasks.xml
# Intellij - Sensitive or high-churn files:
.idea/dataSources/
.idea/dataSources.ids
.idea/dataSources.xml
.idea/dataSources.local.xml
.idea/sqlDataSources.xml
.idea/dynamic.xml
.idea/uiDesigner.xml

EOL
}


function write_dev_requirements {

    cat > ${NAME}/dev-requirements.in <<EOL
bpython
flake8
hypothesis
hypothesis-pytest
ipython
pip-tools
pudb
pytest
pytest-capturelog
pytest-cov
pytest-flake8
pytest-mock
pytest-mypy
pytest-pep8
pytest-profiling
pytest-pudb
pytest-runner
pytest-sugar
pytest-xdist
EOL
}

function write_requirements {
    cat > ${NAME}/requirements.in <<EOL
daiquiri
docopt
pbr
EOL
}

function write_pytest_ini {
    cat > ${NAME}/pytest.ini <<EOL
[pytest]
addopts = --doctest-modules --ignore build
EOL
}

function write_mypy {
    cat > ${NAME}/mypy.ini <<EOL
[mypy]
python_version = 3.6
ignore_missing_imports = true
EOL
}

function write_readme {
    cat > ${NAME}/README.md <<EOL
# `python -c "import sys; print(sys.argv[1].title())" ${NAME}`

EOL
    cat >> ${NAME}/README.md <<"EOL"

# Name Me

A brand new project. Summarise me.

- Install `pip-tools` from pypi.
- Put any initial package requirements into `requirements.in` and `dev-requirements.in`.
- Run `pip-compile --output-file requirements.txt requirements.in` to create the requirements.txt file.
- Run `pip-compile --output-file dev-requirements.txt dev-requirements.in` for the dev/testing only dependencies.
- Edit `setup.cfg`


## Python Environment

Developed and works best with `python 3.6.1`+. Setup a VM environment with `conda` or `virtualenv`.

The project dependencies can then be restored with:

`pip install -r requirements.txt -r dev-requirements.txt`


## Tests

Run linter code quality checks:

`python setup.py flake8` or `pytest --flake8 app`


Run static type checker:

`pytest --mypy app` or `mypy app`


Run all functional tests:

`python setup.py test` or `pytest tests`


## Configuration & Running
...

EOL
}

function write_conftest {
    cat > ${NAME}/tests/conftest.py <<EOL
import os
import sys

import pytest

PROJECT_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, PROJECT_ROOT_DIR)
EOL

cat > ${NAME}/conftest.py <<EOL
collect_ignore = ["setup.py"]
EOL
}

if [[ ! -e ${NAME}/README.md ]]
    then
        write_readme
fi

if [[ ! -e ${NAME}/mypy.ini ]]
    then
        write_mypy
fi

if [[ ! -e ${NAME}/setup.py ]]
    then
        write_setuppy
fi

if [[ ! -e ${NAME}/setup.cfg ]]
    then
        write_setup_cfg
fi

if [[ ! -e ${NAME}/dev-requirements.in ]]
    then
        write_dev_requirements
fi

if [[ ! -e ${NAME}/requirements.in ]]
    then
        write_requirements
fi

mkdir -p ${NAME}/tests
touch "${NAME}/tests/__init__.py"

if [[ ! -e ${NAME}/tests/conftest.py ]]
    then
        write_conftest
fi


if [[ ! -e ${NAME}/.gitignore ]]
    then
        write_gitignore
fi

if [[ ! -e ${NAME}/pytest.ini ]]
    then
        write_pytest_ini
fi

# Finally try to setup a virtual environment if the program is found and the env does not exist.
hash conda 2>/dev/null && conda info --envs | grep ${NAME} || conda create -n ${NAME} python=3.6
