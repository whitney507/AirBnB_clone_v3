#!/usr/bin/env bash
# This script initializes the testing suite.
# It checks the PEP8 style of all Python files
# and runs all unit tests.

# Check PEP8 style of Python files
pep8 . &&

# Run all unittests
python3 -m unittest discover -v ./tests/ &&

# Validate HTML files using w3c_validator.py
./dev/w3c_validator.py \
    $(find ./web_static -maxdepth 1 -name "*.html" -type f ! -name "4*") &&

# Validate CSS files using w3c_validator.py
./dev/w3c_validator.py \
    $(find ./web_static/styles -maxdepth 1 -name "*.css" -type f) &&

# Store the return value
ret_val=$?

# Clear file.json
> ./dev/file.json

# Remove __pycache__ folder
py3clean .

# Exit with the status from tests
exit "$ret_val"

