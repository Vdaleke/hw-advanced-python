#!/bin/sh

echo "Running Black..."
poetry run black hw3 tests

echo "Running isort..."
poetry run isort hw3 tests

echo "Running Poetry check..."
poetry check --lock

echo "Running pytest check..."
poetry run pytest tests/
