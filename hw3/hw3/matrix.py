from typing import List, Union

import numpy as np


class IOMixin:
    """Mixin for file operations"""

    def to_file(self, filename: str) -> None:
        with open(filename, "w") as f:
            f.write(str(self))

    @classmethod
    def from_file(cls, filename: str) -> "Matrix":
        with open(filename) as f:
            data = [[int(num) for num in line.split()] for line in f]
        return cls(data)


class DisplayMixin:
    """Mixin for pretty matrix display"""

    def __str__(self) -> str:
        str_data = [[str(item) for item in row] for row in self.data]
        col_widths = [
            max(len(str_data[row][col]) for row in range(self.rows))
            for col in range(self.cols)
        ]

        rows = []
        for row in str_data:
            formatted_row = []
            for item, width in zip(row, col_widths):
                formatted_row.append(f"{item:>{width}}")
            rows.append("  ".join(formatted_row))

        return "\n".join(rows)

    def __repr__(self) -> str:
        preview = (
            f"{self.data[0][0]} .. {self.data[0][-1]}\n"
            f"..\n"
            f"{self.data[-1][0]} .. {self.data[-1][-1]}"
            if self.rows > 3 and self.cols > 3
            else str(self)
        )
        return f"Matrix<{self.rows}x{self.cols}>(\n" f"{preview}\n" ")"


class PropertyMixin:
    """Mixin for property access"""

    @property
    def shape(self) -> tuple:
        return (self.rows, self.cols)

    @property
    def T(self) -> "Matrix":
        return Matrix(list(map(list, zip(*self.data))))


class Matrix(IOMixin, DisplayMixin, PropertyMixin):
    def __init__(self, data: List[List[Union[int, float]]]):
        """Initialize matrix with data validation"""
        if not data or not all(isinstance(row, list) for row in data):
            raise ValueError("Matrix data must be a non-empty list of lists")

        row_lengths = [len(row) for row in data]
        if len(set(row_lengths)) != 1:
            raise ValueError("All matrix rows must have equal length")

        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0
        self._cache = {}  # Cache for matrix multiplication

    def __eq__(self, other) -> bool:
        if not isinstance(other, Matrix):
            return False
        return self.data == other.data

    def __hash__(self) -> int:
        total = sum(sum(row) for row in self.data)
        return (total * self.rows + self.cols) % 999999

    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> "Matrix":
        return cls(arr.tolist())

    def __add__(self, other):
        """Matrix addition (+) operator."""
        if not isinstance(other, Matrix):
            raise ValueError("Addition requires another Matrix object")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")
        return Matrix(
            [
                [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
                for i in range(self.rows)
            ]
        )

    def __mul__(self, other):
        """Element-wise multiplication (*) operator."""
        if not isinstance(other, Matrix):
            raise ValueError("Element-wise multiplication requires another Matrix")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                "Matrix dimensions must match for element-wise multiplication"
            )
        return Matrix(
            [
                [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
                for i in range(self.rows)
            ]
        )

    def __matmul__(self, other):
        """Matrix multiplication (@) operator."""
        if not isinstance(other, Matrix):
            raise ValueError("Matrix multiplication requires another Matrix")
        if self.cols != other.rows:
            raise ValueError(
                f"Columns of first matrix ({self.cols}) must match "
                f"rows of second matrix ({other.rows}) for multiplication"
            )

        cache_key = (hash(self), hash(other))
        if cache_key in self._cache:
            return self._cache[cache_key]

        result = Matrix(
            [
                [
                    sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                    for j in range(other.cols)
                ]
                for i in range(self.rows)
            ]
        )
        self._cache[cache_key] = result
        return result
