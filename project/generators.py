from typing import Generator, Tuple

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

def prime_number_generator(max_count: int = 10000) -> Generator[int, None, None]:
    """
    Generator to produce prime numbers.

    Args:
        max_count (int): Maximum number of prime numbers to generate.

    Yields:
        int: The next prime number.
    """
    is_prime = {}
    current = 2
    total_primes = 0

    while total_primes < max_count:
        if current not in is_prime:
            yield current
            is_prime[current * current] = [current]
            total_primes += 1
        else:
            for prime in is_prime[current]:
                is_prime.setdefault(prime + current, []).append(prime)
            del is_prime[current]
        current += 1

def prime_decorator(func):
    """
    Decorator that returns the k-th prime number.

    Args:
        func: Generator function to produce prime numbers.

    Returns:
        Callable[[int], int]: Wrapped function that returns the k-th prime number.
    """
    def inner(k: int) -> int:
        if k < 1:
            raise ValueError("Index must be a positive integer.")
        if not isinstance(k, int):
            raise TypeError("Index must be an integer.")

        generator_instance = func()
        for index_counter, prime in enumerate(generator_instance, start=1):
            if index_counter == k:
                return prime
        
        raise ValueError("Prime number not found at the specified position.")

    return inner

@prime_decorator
def get_kth_prime_number() -> Generator[int, None, None]:
    """
    Generator for retrieving the k-th prime number.

    Returns:
        Generator[int, None, None]: Generator yielding prime numbers.
    """
    return prime_number_generator(max_count=1000)