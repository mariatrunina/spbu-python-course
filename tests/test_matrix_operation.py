import pytest
import sys
import os

# Assuming the matrix_operations.py is in the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from project.matrix_operation import add_matrices, multiply_matrices, transpose


def test_add_matrices():
    assert add_matrices([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[6, 8], [10, 12]]
    assert add_matrices([[0, 0], [0, 0]], [[1, 1], [1, 1]]) == [[1, 1], [1, 1]]
    assert add_matrices([[-1, -2], [-3, -4]], [[1, 2], [3, 4]]) == [[0, 0], [0, 0]]


def test_multiply_matrices():
    assert multiply_matrices([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]
    assert multiply_matrices([[0]], [[5]]) == [[0]]  # Multiplying by zero
    with pytest.raises(IndexError):
        multiply_matrices([[1]], [[2], [3]])  # Incompatible dimensions


def test_transpose():
    assert transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
    assert transpose([[1]]) == [[1]]  # Single element
    assert transpose([]) == []  # Empty matrix
