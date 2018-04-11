from setuptools import setup

setup(setup_requires=['flake8', 'pbr', 'pytest-runner'],
      pbr=True,
      tests_require=['pytest'])
