def add_matrices(matrix1, matrix2):
    """Складывает две матрицы одинаковых размеров.

    Args:
        matrix1 (List[List[float]]): Первая матрица.
        matrix2 (List[List[float]]): Вторая матрица.

    Raises:
        ValueError: Если матрицы имеют разные размеры или пустые.

    Returns:
        List[List[float]]: Результирующая матрица, являющаяся суммой matrix1 и matrix2.
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


def multiply_matrices(matrix1, matrix2):
    """Умножает две матрицы.

    Args:
        matrix1 (List[List[float]]): Первая матрица.
        matrix2 (List[List[float]]): Вторая матрица.

    Raises:
        ValueError: Если одна из матриц пустая или если они несовместимы для умножения.

    Returns:
        List[List[float]]: Результирующая матрица, являющаяся произведением matrix1 и matrix2.
    """
    if not matrix1 or not matrix2:
        raise ValueError("Матрицы не могут быть пустыми.")

    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Несовместимые матрицы для умножения.")

    result = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

    return result


def transpose(matrix):
    """Транспонирует матрицу.

    Args:
        matrix (List[List[float]]): Исходная матрица.

    Returns:
        List[List[float]]: Транспонированная матрица.

    Если входная матрица пустая, возвращает пустую матрицу.
    """
    if not matrix:
        return []

    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
