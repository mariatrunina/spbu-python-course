from typing import Callable, Any


def curry_explicit(function: Callable[..., Any], arity: int) -> Callable:
    """
    Curries a function with a specified arity.

    This function transforms a regular function into a curried version,
    allowing it to be called with fewer arguments than it expects.
    When enough arguments are provided, it invokes the original function.

    Args:
        function (Callable[..., Any]): The function to be curried.
        arity (int): The number of arguments the function expects.

    Returns:
        Callable: A curried version of the input function.

    Raises:
        ValueError: If arity is negative.
        TypeError: If more arguments are provided than expected.

    Example:
        def add(x, y):
            return x + y

        curried_add = curry_explicit(add, 2)
        result = curried_add(1)(2)  # Returns 3
    """
    if arity < 0:
        raise ValueError("Arity cannot be negative.")

    def curried(*args: Any) -> Callable:
        if len(args) > arity:
            raise TypeError(
                f"Function takes at most {arity} arguments but got {len(args)}."
            )

        if len(args) == arity:
            return function(*args)

        return lambda *more_args: (
            curried(*(args + more_args))
            if len(args) + len(more_args) <= arity
            else None
        )

    if arity == 0:
        return lambda: function()  # Call the function to get the result

    return curried


def uncurry_explicit(curried_function: Callable[..., Any], arity: int) -> Callable:
    """
    Uncurries a curried function back to its original form.

    This function transforms a curried version of a function back
    into a regular function that takes all its arguments at once.

    Args:
        curried_function (Callable[..., Any]): The curried function to be uncurried.
        arity (int): The number of arguments the original function expects.

    Returns:
        Callable: An uncurried version of the input function.

    Raises:
        ValueError: If arity is negative.
        TypeError: If the number of provided arguments does not match the expected arity.

    Example:
        def add(x, y):
            return x + y

        curried_add = curry_explicit(add, 2)
        uncurried_add = uncurry_explicit(curried_add, 2)
        result = uncurried_add(1, 2)  # Returns 3
    """
    if arity < 0:
        raise ValueError("Arity cannot be negative.")

    def uncurried(*args: Any) -> Any:
        if len(args) != arity:
            raise TypeError(
                f"Function takes exactly {arity} arguments but got {len(args)}."
            )

        return curried_function(*args)

    return uncurried