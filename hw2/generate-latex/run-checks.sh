#!/bin/sh

echo "Running Black..."
poetry run black generate_latex.py

echo "Running isort..."
poetry run isort generate_latex.py

echo "Running MyPy..."
poetry run mypy generate_latex.py

echo "Running Poetry check..."
poetry check --lock
