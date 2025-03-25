import os

import numpy as np
import pytest

from hw3 import NumpyBasedMatrix

GENERATE = False


@pytest.fixture
def matrices():
    np.random.seed(0)
    return (
        NumpyBasedMatrix(np.random.randint(0, 10, (10, 10)).tolist()),
        NumpyBasedMatrix(np.random.randint(0, 10, (10, 10)).tolist()),
    )


def test_matrix_addition(matrices):
    a, b = matrices
    result: NumpyBasedMatrix = a + b

    expected_file = "tests/data/numpy_matrix+.txt"

    if GENERATE:
        result.to_file(expected_file)
    else:
        expected = NumpyBasedMatrix.from_file(expected_file)
        assert np.array_equal(result.array, expected.array)


def test_elementwise_multiplication(matrices):
    a, b = matrices
    result: NumpyBasedMatrix = a * b

    expected_file = "tests/data/numpy_matrix*.txt"

    if GENERATE:
        result.to_file(expected_file)
    else:
        expected = NumpyBasedMatrix.from_file(expected_file)
        assert np.array_equal(result.array, expected.array)


def test_matrix_multiplication(matrices):
    a, b = matrices
    result: NumpyBasedMatrix = a @ b

    expected_file = "tests/data/numpy_matrix@.txt"

    if GENERATE:
        result.to_file(expected_file)
    else:
        expected = NumpyBasedMatrix.from_file(expected_file)
        assert np.array_equal(result.array, expected.array)
