#!/bin/sh

echo "Running Black..."
poetry run black advanced_python_hw2_vdaleke tests

echo "Running isort..."
poetry run isort advanced_python_hw2_vdaleke tests

echo "Running MyPy..."
poetry run mypy advanced_python_hw2_vdaleke tests

echo "Running Poetry check..."
poetry check --lock

echo "Running pytest check..."
poetry run pytest tests/
