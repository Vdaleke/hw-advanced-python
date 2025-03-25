from typing import Any, List, Union

import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin


class PrettyDisplayMixin:
    """Mixin for pretty matrix display"""

    def __str__(self) -> str:
        max_width = max(len(f"{num:.2f}") for row in self._data for num in row)
        return "\n".join(
            " ".join(f"{num:>{max_width}.2f}" for num in row) for row in self._data
        )


class FileIOMixin:
    """Mixin for file operations"""

    def to_file(self, filename: str) -> None:
        np.savetxt(filename, self._array, fmt="%.2f")

    @classmethod
    def from_file(cls, filename: str) -> "NumpyBasedMatrix":
        array = np.loadtxt(filename)
        return cls(array.tolist())


class NumpyBasedMatrix(NDArrayOperatorsMixin, PrettyDisplayMixin, FileIOMixin):
    """Matrix class with numpy integration and additional features"""

    def __init__(self, data: List[List[Union[int, float]]]) -> None:
        if not data or not all(isinstance(row, list) for row in data):
            raise ValueError("Matrix data must be a non-empty list of lists")

        if len({len(row) for row in data}) != 1:
            raise ValueError("All matrix rows must have equal length")

        self._data = data
        self._array = np.array(data)

    @property
    def data(self) -> List[List[Union[int, float]]]:
        return self._data

    @data.setter
    def data(self, value: List[List[Union[int, float]]]) -> None:
        self._validate_data(value)
        self._data = value
        self._array = np.array(value)

    @property
    def array(self) -> np.ndarray:
        return self._array

    @array.setter
    def array(self, value: np.ndarray) -> None:
        self._data = value.tolist()
        self._array = value

    def _validate_data(self, data: List[List[Union[int, float]]]) -> None:
        """Helper method for data validation"""
        if not data or not all(isinstance(row, list) for row in data):
            raise ValueError("Matrix data must be a non-empty list of lists")
        if len({len(row) for row in data}) != 1:
            raise ValueError("All matrix rows must have equal length")

    def __array__(self, dtype: Any = None) -> np.ndarray:
        return self._array if dtype is None else self._array.astype(dtype)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if method != "__call__":
            return NotImplemented

        inputs = tuple(
            x.array if isinstance(x, NumpyBasedMatrix) else x for x in inputs
        )
        result = getattr(ufunc, method)(*inputs, **kwargs)

        return type(self)(result.tolist()) if isinstance(result, np.ndarray) else result

    def __repr__(self) -> str:
        return f"Matrix({self._data})"

    @property
    def shape(self) -> tuple[int, int]:
        return self._array.shape

    @property
    def T(self) -> "NumpyBasedMatrix":
        return type(self)(self._array.T.tolist())
