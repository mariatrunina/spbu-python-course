from typing import Callable

def curry_explicit(function: Callable, arity: int) -> Callable:
    if arity < 0:
        raise ValueError("Arity cannot be negative.")
    
    def curried(*args):
        if len(args) > arity:
            raise TypeError(f"Function takes at most {arity} arguments but got {len(args)}.")

        if len(args) == arity:
            return function(*args)

        return lambda *more_args: curried(*(args + more_args)) if len(args) + len(more_args) <= arity else None

    if arity == 0:
        return lambda: function()  # Здесь вызываем функцию, чтобы получить результат
    
    return curried


def uncurry_explicit(func: Callable, arity: int) -> Callable:
    if arity < 0:
        raise ValueError("Arity cannot be negative.")

    # Обработка функций с нулевой арностью
    if arity == 0:
        return func()  # Здесь вызываем функцию для получения результата

    def uncurried(*args):
        if len(args) != arity:
            raise TypeError(f"Function expected exactly {arity} arguments, got {len(args)}.")

        return func(*args)

    return uncurried