#! /usr/bin/env python3
"""python-new-project

Python project skeleton generator.

Usage:
    python-new-project <project_name_or_path> [--force]

The 'project_name_or_path' specifies a relative project directory (to the current working directory) or the
path to a project directory (relative or absolute). The project directory need not exist.

The '--force' positional argument will delete the project directory if it already exists.
"""
# [DocOpt](http://docopt.org/) is nice, but it's a 3rd party dependency

import os
from os.path import join
import shutil
from subprocess import check_output
import sys
import textwrap


def abort(msg):
    print(msg)
    print(__doc__)
    sys.exit(1)


def log(msg):
    print(msg)


args = sys.argv[1:]
if not args:
    abort("Missing <project_name_or_path> argument")

project_name_or_path_arg = args[0]
force_arg = len(args) > 1 and args[1].strip().lower() == "--force"

if "/" in project_name_or_path_arg or os.path.sep in project_name_or_path_arg:
    project_name = os.path.split(project_name_or_path_arg)[-1]
    is_project_path = True
else:
    project_name = project_name_or_path_arg
    is_project_path = False

pwd = os.getcwd()
project_dir = join(pwd, project_name) if not is_project_path else project_name_or_path_arg

project_dir_already_exists = os.path.exists(project_dir)

if project_dir_already_exists and not force_arg:
    abort("Project directory already exists - remove and try again or use --force (case insensitive)")


def mkdirs(directory):
    try:
        os.makedirs(directory)
    except OSError:
        # Already exists
        pass


def touch(file_path):
    open(file_path, 'a').close()


def nuke_tree(directory):
    if sys.platform.startswith("win"):
        print(check_output(["rmdir /S /Q", directory], shell=True))
    else:
        shutil.rmtree(directory)


def clean_abort(msg):
    if not project_dir_already_exists:
        nuke_tree(project_dir)

    abort(msg)


def copy_file_to_project(template_file_name, new_project_relative_path):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    shutil.copyfile(join(script_dir, "resources", template_file_name),
                    join(project_dir, new_project_relative_path))


def readme():
    readme_text = rf"""
    # {project_name}

    A brand new project. Summarise me. Getting started:

    - Add/remove dependencies to the `Pipfile`
    - Use [PipEnv](https://pipenv.org/) to install project dependencies and create a virtual environment
    - Edit `setup.cfg`


    ## Python Environment

    Developed and works best with `python 3.6`+. Use [PipEnv](https://pipenv.org/) to install project dependencies and create a virtual environment.


    ## Tests

    Run linter code quality checks:

    `flake8`


    Run static type checker:

    `mypy app tests`


    Run all functional tests:

    `pytest tests --cov app`  # optonally with required code coverage `--cov-fail-under 80`

    ## CI Docker Build

    Install docker and get the command line [drone](https://drone.io/) client and run `drone exec`.


    ## Configuration & Running
    ...

    """

    readme_text = textwrap.dedent(readme_text)
    open(join(project_dir, "README.md"), "w").write(readme_text)


try:

    log(f"Making a new project in directory {project_dir}...")
    mkdirs(project_dir)

    tests_dir = join(project_dir, "tests")
    log(f"Making the tests directory {tests_dir} and __init__.py...")
    mkdirs(tests_dir)
    touch(join(tests_dir, "__init__.py"))

    app_dir = join(project_dir, "app")
    mkdirs(app_dir)
    log(f"Making the app directory {app_dir} and __init__.py...")
    touch(join(app_dir, "__init__.py"))

    log("Adding project skeleton files...")
    copy_file_to_project(".drone.yml", ".drone.yml")
    copy_file_to_project(".gitignore", ".gitignore")
    copy_file_to_project("clean.sh", "clean.sh")
    copy_file_to_project("conftest.py", "conftest.py")
    copy_file_to_project("Pipfile", "Pipfile")
    copy_file_to_project("setup.cfg", "setup.cfg")
    copy_file_to_project("setup.py", "setup.py")
    copy_file_to_project("tests_conftest.py", "tests/conftest.py")
    copy_file_to_project("CHANGELOG.md", "CHANGELOG.md")
    readme()

except Exception as e:
    clean_abort(str(e))

log(f"Suggestion: cd {project_dir} and run 'pipenv --python 3.6' if you need to create your project's virtual environment.")
