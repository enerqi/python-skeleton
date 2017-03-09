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

function cleanupFailedAttempt {
    if [[ $directoryAlreadyExisted = false ]]
        then
            rm -rf ${NAME}
    fi
}
trap cleanupFailedAttempt ERR


function write_setuppy {
    cat > ${NAME}/setup.py <<EOL
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='${NAME}',
    version='0.1.0',
    description='',
    long_description=readme,
    url='',
    license='',
    packages=find_packages(exclude=('tests', 'docs'))
)
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

function write_tests_setuppythonpath {

    cat > ${NAME}/tests/setuppythonpath.py <<EOL
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
EOL
}

function write_test_requirements {

    cat > ${NAME}/requirements-test.txt <<EOL
-r requirements.txt
hypothesis
hypothesis-pytest
pytest
pytest-capturelog
pytest-cov
pytest-mock
pytest-pep8
flake8
EOL
}


touch ${NAME}/README.md
touch ${NAME}/requirements.txt

if [[ ! -e ${NAME}/setup.py ]]
    then
        write_setuppy
fi

if [[ ! -e ${NAME}/requirements-test.txt ]]
    then
        write_test_requirements
fi

mkdir -p ${NAME}/tests
touch "${NAME}/tests/__init__.py"

if [[ ! -e ${NAME}/tests/setuppythonpath.py ]]
    then
        write_tests_setuppythonpath
fi

if [[ ! -e ${NAME}/.gitignore ]]
    then
        write_gitignore
fi
