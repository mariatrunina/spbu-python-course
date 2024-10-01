import math


def dot_product(a, b):
    """Вычисляет скалярное произведение двух векторов.

    Args:
        a (List[float]): Первый вектор.
        b (List[float]): Второй вектор.

    Returns:
        float: Скалярное произведение векторов a и b.

    Raises:
        ValueError: Если длины векторов a и b не совпадают.
    """
    return sum(x * y for x, y in zip(a, b))


def vector_length(c):
    """Вычисляет длину (модуль) вектора.

    Args:
        c (List[float]): Вектор.

    Returns:
        float: Длина вектора c.
    """
    return math.sqrt(dot_product(c, c))


def angle_between_vectors(a, b, verbose=False):
    """Вычисляет угол между двумя векторами в радианах.

    Args:
        a (List[float]): Первый вектор.
        b (List[float]): Второй вектор.
        verbose (bool): Если True, выводит дополнительную информацию.

    Returns:
        float: Угол между векторами a и b в радианах.

    Raises:
        ValueError: Если один из векторов является нулевым.
    """
    len_a = vector_length(a)
    len_b = vector_length(b)

    # Проверка на нулевые векторы
    if len_a == 0 or len_b == 0:
        raise ValueError("Один из векторов является нулевым.")

    if verbose:
        print(f"Длина векторов: a={len_a}, b={len_b}")

    cos_theta = dot_product(a, b) / (len_a * len_b)
    cos_theta = max(-1, min(1, cos_theta))
    if verbose:
        print(f"Косинус угла: {cos_theta}")
    angle = math.acos(cos_theta)

    if verbose:
        print(f"Угол (в радианах): {angle}")

    return angle
