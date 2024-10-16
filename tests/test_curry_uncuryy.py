import pytest
import sys
import os
from typing import Callable, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def curry_explicit(function: Callable[..., Any], arity: int) -> Callable:

    if arity < -1:
        raise ValueError(
            "Arity must be a non-negative integer or -1 for variable arguments."
        )

    def curried(*args: Any) -> Any:

        if arity != -1 and len(args) > arity:
            raise TypeError(
                f"Function takes at most {arity} arguments but got {len(args)}."
            )

        # If it's variadic (arity = -1), evaluate the function if any args are provided
        if arity == -1 and len(args) > 0:
            # If called without additional arguments, return the result
            return function(*args)

        elif len(args) == arity:
            return function(*args)

        return lambda *more_args: curried(*(args + more_args))

    return curried if arity != 0 else lambda: function()


def uncurry_explicit(curried_function: Callable[..., Any], arity: int) -> Callable:

    if arity < 0:
        raise ValueError("Arity cannot be negative.")

    def uncurried(*args: Any) -> Any:
        if len(args) != arity:
            raise TypeError(
                f"Function takes exactly {arity} arguments but got {len(args)}."
            )

        return curried_function(*args)

    return uncurried


def test_curry_and_uncurry():
    f2 = curry_explicit(lambda x, y, z: f"<{x},{y},{z}>", 3)
    g2 = uncurry_explicit(f2, 3)

    result_curry = f2(123)(456)(562)
    assert result_curry == "<123,456,562>"

    result_uncurry = g2(123, 456, 562)
    assert result_uncurry == "<123,456,562>"


def test_curry_exceeding_arity():
    f2 = curry_explicit(lambda x, y, z: f"<{x},{y},{z}>", 3)

    with pytest.raises(TypeError):
        f2(1)(2)(3)(4)


def test_uncurry_incorrect_number_of_arguments():
    f2 = curry_explicit(lambda x, y, z: f"<{x},{y},{z}>", 3)
    g2 = uncurry_explicit(f2, 3)

    with pytest.raises(TypeError):
        g2(1, 2)

    with pytest.raises(TypeError):
        g2(1, 2, 3, 4)


def test_curry_zero_arity():
    f0 = curry_explicit(lambda: 42, 0)

    assert f0() == 42


def test_uncurry_zero_arity():
    f0 = curry_explicit(lambda: 42, 0)
    g0 = uncurry_explicit(f0, 0)

    assert g0() == 42


def test_builtin_functions():
    curried_max = curry_explicit(max, 2)

    assert curried_max(5)(10) == 10
    assert uncurry_explicit(curried_max, 2)(5, 10) == 10


if __name__ == "__main__":
    pytest.main()
