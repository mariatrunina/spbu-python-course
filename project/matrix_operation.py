from typing import List


def add_matrices(
    matrix1: List[List[float]], matrix2: List[List[float]]
) -> List[List[float]]:
    """Adds two matrices of the same size.

    Args:
        matrix1 (List[List[float]]): The first matrix.
        matrix2 (List[List[float]]): The second matrix.

    Raises:
        ValueError: If the matrices have different sizes or are empty.

    Returns:
        List[List[float]]: The resulting matrix, which is the sum of matrix1 and matrix2.
    """
    if (
        not matrix1
        or not matrix2
        or len(matrix1) != len(matrix2)
        or len(matrix1[0]) != len(matrix2[0])
    ):
        raise ValueError("Matrices must be of the same dimensions and non-empty")

    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix1[0])):
            row.append(matrix1[i][j] + matrix2[i][j])
        result.append(row)
    return result


def multiply_matrices(
    matrix1: List[List[float]], matrix2: List[List[float]]
) -> List[List[float]]:
    """Multiplies two matrices.

    Args:
        matrix1 (List[List[float]]): The first matrix.
        matrix2 (List[List[float]]): The second matrix.

    Raises:
        ValueError: If either matrix is empty or if they are incompatible for multiplication.

    Returns:
        List[List[float]]: The resulting matrix, which is the product of matrix1 and matrix2.
    """
    if not matrix1 or not matrix2:
        raise ValueError("Матрицы не могут быть пустыми.")

    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Несовместимые матрицы для умножения.")

    result = [[0.0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

    return result


def transpose(matrix: List[List[float]]) -> List[List[float]]:
    """Transposes a matrix.

    Args:
        matrix (List[List[float]]): The original matrix.

    Returns:
        List[List[float]]: Transposed matrix.

    If the input matrix is ​​empty, returns an empty matrix.
    """
    if not matrix:
        return []

    return [
        [float(matrix[j][i]) for j in range(len(matrix))] for i in range(len(matrix[0]))
    ]
