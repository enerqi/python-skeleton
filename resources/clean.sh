#!/usr/bin/env bash
rm -rf $(find -type d -name __pycache__)
rm -f .coverage
rm -rf *.egg_info
rm -rf .cache
rm -rf .egg
rm -rf .eggs
rm -rf .mypy_cache
rm -rf dist
