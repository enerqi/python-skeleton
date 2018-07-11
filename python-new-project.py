#! /usr/bin/env python3
"""python-new-project

Python project skeleton generator.

Usage:
    python-new-project <project_name_or_path> --app|--lib [--force]

The 'project_name_or_path' is a plain name relative to the current directory or a path that is relative or
absolute for the project to go in. It need not exist.

One of --app (application) or --lib (library) must be selected. Applications use pipfiles to lock down concrete
dependencies whilst libraries specify abstract dependencies in the setup.py file. An application does not need
a setup.py file as it need not be packaged, just deployed and configured.

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


def arg_exists(arg_name, arg_list):
    return any(arg.strip() == arg_name for arg in arg_list)


args = sys.argv[1:]
if not args:
    abort("Missing arguments")

project_name_or_path_arg = args[0]
flag_args = args[1:]
force_arg = arg_exists("--force", flag_args)
is_app = arg_exists("--app", flag_args)
is_lib = arg_exists("--lib", flag_args)

if not any([is_app, is_lib]) or all([is_app, is_lib]):
    abort("A project must be specified as one of app or lib.")

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
    app_readme_text = rf"""
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

    lib_readme_text = rf"""
    # {project_name}

    A brand new project. Summarise me. Getting started:

    - Add/remove dependencies to the `setup.py` file
    - Use [PipEnv](https://pipenv.org/) to install project dependencies and create a virtual environment
    - Edit `setup.py`


    ## {project_name} as a library dependency

    Requires `python 3.6`+. Follows semantic versioning.

    ## Develop {project_name}

    This is library code - use pipenv to install the abstract dependencies in a virtual environment from
    the `setup.py` file.

    `pipenv install -e .` for just the main packages

    `pipenv install -e '.[dev]'` for the dev packages alongside the main packages


    ## Tests

    Run linter code quality checks:

    `flake8`


    Run static type checker:

    `mypy {project_name} tests`


    Run all functional tests:

    `pytest tests --cov {project_name}`  # optonally with required code coverage `--cov-fail-under 80`

    ## CI Docker Build

    Install docker and get the command line [drone](https://drone.io/) client and run `drone exec`.

    ## Release

    To package:

    `python setup.py sdist`

    """

    text = lib_readme_text if is_lib else app_readme_text
    readme_text = textwrap.dedent(text)
    open(join(project_dir, "README.md"), "w").write(readme_text)


def setup_py():

    extras_dict_source = """{'dev': dev_packages}"""
    setup_code = rf"""
    import os
    from setuptools import setup, find_packages

    packages = [
        'daiquiri',
        'docopt',
        'result'
    ]

    dev_packages = [
        'colorama',
        'flake8',
        'hypothesis',
        'hypothesis-pytest',
        'ipython',
        'mypy',
        'pudb',
        'pytest',
        'pytest-cov',
        'pytest-flake8',
        'pytest-mock',
        'pytest-mypy',
        'pytest-pep8',
        'pytest-profiling',
        'pytest-pudb',
        'pytest-runner',
        'pytest-sugar',
        'pytest-xdist'
    ]

    setup(name='{project_name}',
          use_scm_verson=True,
          author='',
          author_email='',
          description='',
          long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
          url='',
          classifiers=[
              "Programming Language :: Python :: 3.6",
              "Operating System :: OS Independent",
          ],
          setup_requires=['setuptools_scm'],
          tests_require=['pytest'],
          packages=find_packages(exclude=['tests']),
          install_requires=packages,
          extras_require={extras_dict_source})
    """
    setup_text = textwrap.dedent(setup_code)
    setup_text = setup_text[setup_text.find('\n') + 1:]  # remove the annoying first line break
    open(join(project_dir, "setup.py"), "w").write(setup_text)


try:

    log(f"Making a new project in directory {project_dir}...")
    mkdirs(project_dir)

    tests_dir = join(project_dir, "tests")
    log(f"Making the tests directory {tests_dir} and __init__.py...")
    mkdirs(tests_dir)
    touch(join(tests_dir, "__init__.py"))

    main_dir = join(project_dir, "app" if is_app else project_name)
    mkdirs(main_dir)
    log(f"Making the main directory {main_dir} and __init__.py...")
    if is_app:
        touch(join(main_dir, "__init__.py"))
    else:
        copy_file_to_project("lib_init.py", f"{project_name}/__init__.py")

    log("Adding project skeleton files...")

    if is_app:
        copy_file_to_project(".drone.yml_app", ".drone.yml")
        copy_file_to_project(".gitignore_app", ".gitignore")
        copy_file_to_project("Pipfile", "Pipfile")  # app only
    else:
        copy_file_to_project(".drone.yml_lib", ".drone.yml")
        drone_with_project_name = open(join(project_dir, ".drone.yml")).read()\
            .replace("{project_name}", project_name)
        open(join(project_dir, ".drone.yml"), "w").write(drone_with_project_name)

        copy_file_to_project(".gitignore_lib", ".gitignore")
        setup_py()  # lib only

    copy_file_to_project("setup.cfg", "setup.cfg")
    copy_file_to_project("tests_conftest.py", "tests/conftest.py")
    copy_file_to_project("CHANGELOG.md", "CHANGELOG.md")
    readme()

    scripts_dir = join(project_dir, "scripts")
    mkdirs(scripts_dir)
    copy_file_to_project("clean.sh", "scripts/clean.sh")

except Exception as e:
    clean_abort(str(e))
