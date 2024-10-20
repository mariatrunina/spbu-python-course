import pytest
import sys
import os
import itertools
from typing import Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.generators import (
    fetch_rgba_by_index,
    get_kth_prime_number,
    COMBINATION_LIMIT,
)


def test_fetch_rgba_by_index() -> None:
    assert fetch_rgba_by_index(50) == (0, 0, 0, 100)


def test_fetch_rgba_out_of_bounds() -> None:
    with pytest.raises(IndexError):
        fetch_rgba_by_index(COMBINATION_LIMIT)


def test_fetch_rgba_negative_value() -> None:
    with pytest.raises(IndexError):
        fetch_rgba_by_index(-5)


@pytest.mark.parametrize(
    "index, expected_rgba",
    [
        (0, (0, 0, 0, 0)),
        (1, (0, 0, 0, 2)),
        (COMBINATION_LIMIT - 1, (255, 255, 255, 100)),
    ],
)
def test_fetch_rgba_multiple_cases(
    index: int, expected_rgba: Tuple[int, int, int, int]
) -> None:
    assert fetch_rgba_by_index(index) == expected_rgba


@pytest.mark.parametrize(
    "k, expected_prime", [(1, 2), (2, 3), (5, 11), (10, 29), (100, 541), (1000, 7919)]
)
def test_kth_prime_number(k: int, expected_prime: int) -> None:
    assert get_kth_prime_number(k) == expected_prime


def test_kth_prime_zero() -> None:
    with pytest.raises(ValueError):
        get_kth_prime_number(0)


def test_kth_prime_negative() -> None:
    with pytest.raises(ValueError):
        get_kth_prime_number(-3)


def test_kth_prime_non_integer() -> None:
    with pytest.raises(TypeError):
        get_kth_prime_number(3.5)
