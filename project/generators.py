from typing import Generator, Tuple


# Константа для лимита RGBA
COMBINATION_LIMIT = 256 * 256 * 256 * 51


def fetch_rgba_by_index(idx: int) -> Tuple[int, int, int, int]:
    """
    Retrieves RGBA color by the given index.

    Args:
        idx (int): Index corresponding to the RGBA vector.

    Returns:
        Tuple[int, int, int, int]: A tuple representing (R, G, B, A).

    Raises:
        IndexError: If the index is out of valid range.
    """
    if idx < 0 or idx >= COMBINATION_LIMIT:
        raise IndexError("Index is out of the valid range.")

    red_channel = (idx // (256 * 256 * 51)) % 256
    green_channel = (idx // (256 * 51)) % 256
    blue_channel = (idx // 51) % 256
    alpha_channel = (idx % 51) * 2

    return red_channel, green_channel, blue_channel, alpha_channel


def prime_number_generator() -> Generator[int, None, None]:
    """
    Generator to produce prime numbers indefinitely.

    Yields:
        int: The next prime number.
    """
    current = 2
    while True:
        is_prime = True
        for i in range(2, int(current**0.5) + 1):
            if current % i == 0:
                is_prime = False
                break
        if is_prime:
            yield current
        current += 1


def prime_decorator(func):
    """
    Decorator that returns the k-th prime number.

    Args:
        func: A generator function to produce prime numbers.

    Returns:
        Callable[[int], int]: Wrapped function that returns the k-th prime number.
    """

    def inner(k: int) -> int:
        if k < 1:
            raise ValueError("Index must be a positive integer.")
        if not isinstance(k, int):
            raise TypeError("Index must be an integer.")

        # Мы сохраняем состояние генератора для будущих вызовов
        generator_instance = func()  # Создаем генератор один раз
        for _ in range(k - 1):  # Пропускаем первые k-1 простых числа
            next(generator_instance)  # Перемещение по генератору
        return next(generator_instance)  # Возвращаем k-ое простое число

    return inner


@prime_decorator
def get_kth_prime_number() -> Generator[int, None, None]:
    """
    Generator for retrieving the k-th prime number.

    Returns:
        Generator[int, None, None]: Generator yielding prime numbers.
    """
    return prime_number_generator()
