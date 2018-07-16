#!/usr/bin/env bash
rm -rf $(find -type d -name __pycache__)
rm -rf $(find -type d -name .pytest_cache)
rm -f .coverage
rm -rf *.egg-info
rm -rf .cache
rm -rf .egg
rm -rf .eggs
rm -rf .mypy_cache
rm -rf .pytest_cache
rm -rf .hypothesis
rm -rf dist
