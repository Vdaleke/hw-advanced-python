#!/bin/sh

echo "Running Black..."
poetry run black hw1 tests

echo "Running isort..."
poetry run isort hw1 tests

echo "Running MyPy..."
poetry run mypy hw1 tests

echo "Running Poetry check..."
poetry check --lock

echo "Running pytest check..."
poetry run pytest tests/
