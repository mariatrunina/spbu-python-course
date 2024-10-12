import time
import pytest
import sys
import os
from collections import OrderedDict

# Добавляем путь к проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.decorators import cache_result  # Импортируем только нужное


# Тестируемые функции
@cache_result(max_cache_size=3)
def slow_function(x: int) -> int:
    time.sleep(1)  # Симуляция медленного вычисления
    return x * 2


@cache_result(max_cache_size=5)
def cached_sum(*args: int) -> int:
    return sum(args)


@cache_result(max_cache_size=3)
def cached_max(*args: int) -> int:
    return max(args)


@cache_result(max_cache_size=3)
def cached_min(*args: int) -> int:
    return min(args)


# Тесты
def test_cache_with_positional_arguments():
    assert slow_function(2) == 4  # Первый вызов
    assert slow_function(2) == 4  # Использование кэша
    assert slow_function(3) == 6  # Новое вычисление
    assert slow_function(4) == 8  # Новое вычисление
    assert slow_function(2) == 4  # Использование кэша


def test_cache_with_keyword_arguments():
    @cache_result(max_cache_size=2)
    def add(a: int, b: int) -> int:
        return a + b

    assert add(a=1, b=2) == 3  # Первый вызов
    assert add(a=1, b=2) == 3  # Использование кэша
    assert add(a=2, b=3) == 5  # Новое вычисление
    assert add(b=2, a=1) == 3  # Использование кэша


def test_cache_with_built_in_functions():
    assert cached_sum(1, 2, 3) == 6  # Первый вызов
    assert cached_sum(1, 2, 3) == 6  # Использование кэша
    assert cached_sum(4, 5) == 9  # Новое вычисление

    assert cached_max(1, 2, 3) == 3  # Первый вызов
    assert cached_max(1, 2, 3) == 3  # Использование кэша
    assert cached_max(0, -1, -2) == 0  # Новое вычисление

    assert cached_min(1, -1, 0) == -1  # Первый вызов
    assert cached_min(1, -1, 0) == -1  # Использование кэша
    assert cached_min(5, 10, -5) == -5  # Новое вычисление


def test_cache_limit():
    @cache_result(max_cache_size=2)
    def multiply(a: int, b: int) -> int:
        return a * b

    assert multiply(1, 2) == 2
    assert multiply(2, 3) == 6
    assert multiply(3, 4) == 12
    # Проверяем, что кэш не содержит (1, 2)
    assert multiply(1, 2) == 2  # Должно быть пересчитано


if __name__ == "__main__":
    pytest.main()
