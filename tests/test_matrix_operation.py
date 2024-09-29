import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from project.matrix_operation import print_matrix, add_matrices, multiply_matrices, transpose


def test_add_matrices():
    matrix1 = [[1, 2], [3, 4]]
    matrix2 = [[5, 6], [7, 8]]
    expected_result = [[6, 8], [10, 12]]
    assert add_matrices(matrix1, matrix2) == expected_result

def test_multiply_matrices():
    matrix1 = [[1, 2], [3, 4]]
    matrix2 = [[5, 6], [7, 8]]
    expected_result = [[19, 22], [43, 50]]
    assert multiply_matrices(matrix1, matrix2) == expected_result

def test_transpose():
    matrix = [[1, 2, 3], [4, 5, 6]]
    expected_result = [[1, 4], [2, 5], [3, 6]]
    assert transpose(matrix) == expected_result

def test_print_matrix(capsys):
    matrix = [[1, 2], [3, 4]]
    print_matrix(matrix)
    
    captured = capsys.readouterr()
    expected_output = "1 2\n3 4\n\n"
    assert captured.out == expected_output

# Запуск тестов
if __name__ == "__main__":
    pytest.main()