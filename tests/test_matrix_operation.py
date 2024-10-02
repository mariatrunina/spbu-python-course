import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from project.matrix_operation import (
    add_matrices,
    multiply_matrices,
    transpose,
)


def test_add_matrices():
    # Обычное сложения
    matrix1 = [[1, 2], [3, 4]]
    matrix2 = [[5, 6], [7, 8]]
    expected_result = [[6, 8], [10, 12]]
    assert add_matrices(matrix1, matrix2) == expected_result

    # Сложение с нулевой матрицей
    matrix1 = [[0, 0], [0, 0]]
    matrix2 = [[5, 6], [7, 8]]
    expected_result = [[5, 6], [7, 8]]
    assert add_matrices(matrix1, matrix2) == expected_result

    # Сложение двух нулевых матриц
    matrix1 = [[0, 0], [0, 0]]
    matrix2 = [[0, 0], [0, 0]]
    expected_result = [[0, 0], [0, 0]]
    assert add_matrices(matrix1, matrix2) == expected_result


def test_multiply_matrices():
    # Обычное умножение
    matrix1 = [[1, 2], [3, 4]]
    matrix2 = [[5, 6], [7, 8]]
    expected_result = [[19, 22], [43, 50]]
    assert multiply_matrices(matrix1, matrix2) == expected_result

    # Умножение на единичную матрицу
    identity_matrix = [[1, 0], [0, 1]]
    result = multiply_matrices(matrix1, identity_matrix)
    assert result == matrix1

    # Умножение на нулевую матрицу
    zero_matrix = [[0, 0], [0, 0]]
    expected_result = [[0, 0], [0, 0]]
    assert multiply_matrices(matrix1, zero_matrix) == expected_result

    matrix5 = [[1, 2], [3, 4]]
    matrix6 = [[5, 6]]

    try:
        multiply_matrices(matrix5, matrix6)
        assert False, "Expected ValueError for incompatible matrices"
    except ValueError:
        pass


def test_transpose():
    # Тест для обычной матрицы
    matrix = [[1, 2, 3], [4, 5, 6]]
    expected_result = [[1, 4], [2, 5], [3, 6]]
    assert transpose(matrix) == expected_result

    # Тест для квадратной матрицы
    square_matrix = [[1, 2], [3, 4]]
    expected_result_square = [[1, 3], [2, 4]]
    assert transpose(square_matrix) == expected_result_square

    # Тест для единичной матрицы
    identity_matrix = [[1]]
    assert transpose(identity_matrix) == identity_matrix


def test_add_empty_matrices():
    empty_matrix1 = []
    empty_matrix2 = []

    with pytest.raises(ValueError):
        add_matrices(empty_matrix1, empty_matrix2)


def test_transpose_empty_matrix():
    empty_matrix = []

    assert transpose(empty_matrix) == []


if __name__ == "__main__":
    pytest.main()
