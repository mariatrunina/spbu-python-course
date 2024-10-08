from typing import Callable


def curry_explicit(function: Callable, arity: int) -> Callable:
    if arity < 0:
        raise ValueError("Arity cannot be negative.")
    if arity == 0:
        return function()

    def curried(*args):
        if len(args) > arity:
            raise TypeError(
                f"Function takes at most {arity} arguments but got {len(args)}."
            )

        # Если достигнута нужная арность, вызываем функцию
        if len(args) == arity:
            return function(*args)

        # Возвращаем новую функцию, ожидающую оставшиеся аргументы
        return lambda *more_args: (
            curried(*(args + more_args))
            if len(args) + len(more_args) <= arity
            else None
        )

    return curried


def uncurry_explicit(func: Callable, arity: int) -> Callable:
    if arity < 0:
        raise ValueError("Arity cannot be negative.")

    # Обработка функций с нулевой арностью
    if arity == 0:
        return func()

    def uncurried(*args):
        if len(args) != arity:
            raise TypeError(
                f"Function expected exactly {arity} arguments, got {len(args)}."
            )

        return func(*args)

    return uncurried
