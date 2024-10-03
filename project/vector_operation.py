import math
from typing import List


def dot_product(a: List[float], b: List[float]) -> float:
    """Calculates the dot product of two vectors.

    Args:
        a (List[float]): The first vector.
        b (List[float]): The second vector.

    Returns:
        float: The dot product of vectors a and b.

    Raises:
        ValueError: If the lengths of vectors a and b do not match.
    """
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length.")

    return sum(x * y for x, y in zip(a, b))


def vector_length(c: List[float]) -> float:
    """Calculates the length (magnitude) of a vector.

    Args:
        c (List[float]): The vector.

    Returns:
        float: The length of vector c.
    """
    return math.sqrt(dot_product(c, c))


def angle_between_vectors(
    a: List[float], b: List[float], verbose: bool = False
) -> float:
    """Calculates the angle between two vectors in radians.

    Args:
        a (List[float]): The first vector.
        b (List[float]): The second vector.
        verbose (bool): If True, prints additional information.

    Returns:
        float: The angle between vectors a and b in radians.

    Raises:
        ValueError: If either vector is zero.
    """
    len_a = vector_length(a)
    len_b = vector_length(b)

    # Check for zero vectors
    if len_a == 0 or len_b == 0:
        raise ValueError("One of the vectors is zero.")

    if verbose:
        print(f"Lengths of vectors: a={len_a}, b={len_b}")

    cos_theta = dot_product(a, b) / (len_a * len_b)

    # Clamping the cosine value to avoid domain errors in acos
    cos_theta = max(-1, min(1, cos_theta))

    if verbose:
        print(f"Cosine of the angle: {cos_theta}")

    angle = math.acos(cos_theta)

    if verbose:
        print(f"Angle (in radians): {angle}")

    return angle
