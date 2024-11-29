import pytest
import random
import sys
import os
import inspect
import copy
from typing import Callable, Any, Dict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.smartargs_func import smart_args, example_function, Evaluated, Isolated


def test_example_function_with_valid_args():
    result = example_function(a=2, c={"a": 3})
    assert result == 6  # 2 + 1 + 3


def test_example_function_with_evaluated():
    result = example_function(b=Evaluated(lambda: 5), c={"a": 2})
    assert result == 7  # 0 + 5 + 2


def test_evaluated_recalculation():
    def random_value():
        return random.randint(1, 10)

    result_1 = example_function(b=Evaluated(lambda: random_value()), c={"a": 1})
    result_2 = example_function(b=Evaluated(lambda: random_value()), c={"a": 2})

    print(f"Result 1: {result_1}, Result 2: {result_2}")
    assert result_1 != result_2, "Results should be different, but they're the same."


def test_example_function_with_isolated():
    mutable_dict = {"a": 10}
    result = example_function(c=mutable_dict)
    assert result == 11  # 0 + 1 + (deepcopy of mutable_dict)
    assert mutable_dict == {"a": 10}


def test_example_function_with_keyword_only_arguments():
    @smart_args
    def keyword_only_example(*, d: Any) -> int:
        return d["b"] if isinstance(d, dict) else -1

    result = keyword_only_example(d=Isolated())

    assert isinstance(result, int)


def test_keyword_only_argument_with_isolated():
    @smart_args
    def keyword_only_example(*, d: Any) -> int:
        return d["b"] if isinstance(d, dict) else -1

    result = keyword_only_example(d=Isolated())

    assert isinstance(result, int)


if __name__ == "__main__":
    pytest.main()
