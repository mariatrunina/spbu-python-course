def add_matrices(matrix1, matrix2):
    if not matrix1 or not matrix2 or len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        raise ValueError("Matrices must be of the same dimensions and non-empty")
    
    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix1[0])):
            row.append(matrix1[i][j] + matrix2[i][j])
        result.append(row)
    return result


def multiply_matrices(matrix1, matrix2):
    # Проверка на пустые матрицы
    if not matrix1 or not matrix2:
        raise ValueError("Матрицы не могут быть пустыми.")
    
    # Проверка совместимости
    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Несовместимые матрицы для умножения.")
    
    result = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
    
    return result

def transpose(matrix):
    if not matrix:  # Проверка на пустую матрицу
        return []
    
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]