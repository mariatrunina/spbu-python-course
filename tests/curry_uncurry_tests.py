import pytest
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.curry_uncurry_funkctions import curry_explicit, uncurry_explicit


def test_curry_and_uncurry():
    """Тестирование каррирования и ункаррирования функции"""
    f2 = curry_explicit(lambda x, y, z: f"<{x},{y},{z}>", 3)
    g2 = uncurry_explicit(f2, 3)

    # Проверяем каррированную функцию
    result_curry = f2(123)(456)(562)
    assert result_curry == "<123,456,562>"

    # Проверяем ункаррированную функцию
    result_uncurry = g2(123, 456, 562)
    assert result_uncurry == "<123,456,562>"


def test_curry_exceeding_arity():
    """Тестирование превышения арности в каррированной функции"""
    f2 = curry_explicit(lambda x, y, z: f"<{x},{y},{z}>", 3)

    with pytest.raises(TypeError):
        f2(1)(2)(3)(4)  # Это должно вызвать исключение


def test_uncurry_incorrect_number_of_arguments():
    """Тестирование неправильного количества аргументов в ункаррированной функции"""
    f2 = curry_explicit(lambda x, y, z: f"<{x},{y},{z}>", 3)
    g2 = uncurry_explicit(f2, 3)

    with pytest.raises(TypeError):
        g2(1, 2)  # Это должно вызвать исключение

    with pytest.raises(TypeError):
        g2(1, 2, 3, 4)  # Это тоже должно вызвать исключение


def test_curry_zero_arity():
    """Тестирование функции с нулевой арностью"""
    f0 = curry_explicit(lambda: "No arguments", 0)

    assert f0() == "No arguments"


def test_uncurry_zero_arity():

    f0 = curry_explicit(lambda: "No arguments", 0)
    g0 = uncurry_explicit(f0, 0)

    assert g0() == "No arguments"


if __name__ == "__main__":
    pytest.main()
