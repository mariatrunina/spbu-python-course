import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.concurent_futures import (
    compute_sum_with_futures,
)


def test_cartesian_product_sum():
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    result = compute_sum_with_futures(list1, list2)
    assert result == 63
