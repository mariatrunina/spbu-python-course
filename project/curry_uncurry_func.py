from typing import Callable, Any


def curry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Curries a function with a specified arity.

    This function transforms a given function into a curried version that can be
    called with fewer arguments than it expects. If the number of provided arguments
    is less than the specified arity, it returns a new function that accepts more
    arguments until the required number is reached.

    Parameters:
        function (Callable[..., Any]): The function to be curried.
        arity (int): The number of arguments that the function expects.
                     Use -1 for variable-length arguments.

    Returns:
        Callable[..., Any]: A curried version of the provided function.

    Raises:
        ValueError: If arity is less than -1.
        TypeError: If more arguments are provided than specified by arity.
    """
    if arity < -1:
        raise ValueError(
            "Arity must be a non-negative integer or -1 for variable arguments."
        )

    def curried(*args: Any) -> Any:

        if arity != -1 and len(args) > arity:
            raise TypeError(
                f"Function takes at most {arity} arguments but got {len(args)}."
            )

        if arity == -1 and len(args) > 0:

            return function(*args)

        elif len(args) == arity:
            return function(*args)

        return lambda *more_args: curried(*(args + more_args))  # type: ignore

    return curried if arity != 0 else lambda: function()  # type: ignore


def uncurry_explicit(
    curried_function: Callable[..., Any], arity: int
) -> Callable[..., Any]:
    """
    Uncurries a curried function back to its original form.

    This function transforms a curried function into its original form, allowing
    it to be called with the exact number of arguments specified by the arity.

    Parameters:
        curried_function (Callable[..., Any]): The curried function to be uncurried.
        arity (int): The number of arguments that the original function expects.

    Returns:
        Callable[..., Any]: An uncurried version of the provided curried function.

    Raises:
        ValueError: If arity is negative.
        TypeError: If the number of provided arguments does not match the expected arity.
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
