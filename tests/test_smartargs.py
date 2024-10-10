import pytest
import random
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.smartargs_func import (
    smart_args,
    Evaluated,
    check_isolation,
    example_function,
    Isolated,
)


def test_example_function_with_valid_args():
    result = example_function(a=2, c={"a": 3})
    assert result == 6  # 2 + 1 + 3


def test_example_function_with_evaluated():
    result = example_function(b=Evaluated(lambda: 5), c={"a": 2})
    assert result == 7  # 0 + 5 + 2


def test_example_function_with_isolated():
    mutable_dict = {"a": 10}
    result = example_function(c=mutable_dict)
    assert result == 11  # 0 + 1 + (deepcopy of mutable_dict)
    assert mutable_dict == {"a": 10}  # Исходный словарь не должен измениться


def test_check_isolation():
    no_mutable = {"a": 10}

    result = check_isolation(d=no_mutable)

    assert result == {"a": 0}  # Проверяем, что функция вернула измененное значение
    assert no_mutable == {"a": 10}  # Проверяем, что исходный словарь не изменился


if __name__ == "__main__":
    pytest.main()
