import pytest
import random
import sys
import os

# Установка пути к модулю с декоратором
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.smartargs_func import (
    smart_args,
    Evaluated,
    Isolated,
)  # Импортируем необходимые классы


# Пример функции с использованием Isolated
@smart_args
def check_isolation(*, d=Isolated()):
    d["a"] = 0
    return d


# Пример функции с использованием Evaluated
def get_random_number():
    return random.randint(0, 100)


@smart_args
def check_evaluation(*, x=get_random_number(), y=Evaluated(get_random_number)):
    return x, y


def test_check_isolation():
    no_mutable = {"a": 10}

    result = check_isolation(d=no_mutable)

    assert result == {"a": 0}  # Проверяем, что функция вернула измененное значение
    assert no_mutable == {"a": 10}  # Проверяем, что исходный словарь не изменился


def test_check_evaluation():
    # Для проверки генерации случайных чисел используем фиксированное зерно
    random.seed(42)

    # Проверяем, что x всегда одинаковое значение
    result1 = check_evaluation()
    result2 = check_evaluation()

    assert result1[0] == result2[0]  # x должно быть одинаковым в обоих вызовах

    # Проверяем, что y может быть разным при каждом
