import time
import pytest
import sys
import os
from collections import OrderedDict


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.decorators import cache_result


# Test functions
@cache_result(max_cache_size=3, verbose=True)
def slow_function(x: int) -> int:
    time.sleep(1)  # Simulating slow computation
    return x * 2


@cache_result(max_cache_size=5, verbose=True)
def cached_sum(*args: int) -> int:
    return sum(args)


@cache_result(max_cache_size=3, verbose=True)
def cached_max(*args: int) -> int:
    return max(args)


@cache_result(max_cache_size=3, verbose=True)
def cached_min(*args: int) -> int:
    return min(args)


# Tests
def test_cache_with_positional_arguments():
    assert slow_function(2) == 4  # First call
    assert slow_function(2) == 4  # Using cache
    assert slow_function(3) == 6  # New computation
    assert slow_function(4) == 8  # New computation
    assert slow_function(2) == 4  # Using cache


def test_cache_with_keyword_arguments():
    @cache_result(max_cache_size=2, verbose=True)
    def add(a: int, b: int) -> int:
        return a + b

    assert add(a=1, b=2) == 3  # First call
    assert add(a=1, b=2) == 3  # Using cache
    assert add(a=2, b=3) == 5  # New computation
    assert add(b=2, a=1) == 3  # Using cache


def test_cache_with_built_in_functions():
    assert cached_sum(1, 2, 3) == 6  # First call
    assert cached_sum(1, 2, 3) == 6  # Using cache
    assert cached_sum(4, 5) == 9  # New computation

    assert cached_max(1, 2, 3) == 3  # First call
    assert cached_max(1, 2, 3) == 3  # Using cache
    assert cached_max(0, -1, -2) == 0  # New computation

    assert cached_min(1, -1, 0) == -1  # First call
    assert cached_min(1, -1, 0) == -1  # Using cache
    assert cached_min(5, 10, -5) == -5  # New computation


def test_cache_limit():
    @cache_result(max_cache_size=2, verbose=True)
    def multiply(a: int, b: int) -> int:
        return a * b

    assert multiply(1, 2) == 2
    assert multiply(2, 3) == 6
    assert multiply(3, 4) == 12  # This will remove (1,2)

    # Check that the cache does not contain (1,2)
    assert multiply(1, 2) == 2  # Should be recalculated


if __name__ == "__main__":
    pytest.main()
