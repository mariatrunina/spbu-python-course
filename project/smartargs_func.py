import inspect
import copy
from typing import Callable, Any, Dict


class Evaluated:
    """
    A class that wraps a function to be evaluated when called.

    Attributes:
        func (Callable): The function to be evaluated.
    """

    def __init__(self, func: Callable[[], Any]):
        self.func = func


class Isolated:
    """A marker class used to indicate that an argument should be isolated."""

    pass


def smart_args(func: Callable) -> Callable:
    """
    A decorator that processes keyword arguments for a function,
    handling default values that may be instances of Evaluated or Isolated.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: A wrapper function that processes the arguments.

    Raises:
        AssertionError: If an invalid argument is provided or if both Evaluated and Isolated are used together.
    """
    signature = inspect.signature(func)

    def wrapper(**kwargs: Any) -> Any:
        for name in kwargs:
            assert (
                name in signature.parameters
            ), f"Argument '{name}' is not a valid argument."

        final_args: Dict[str, Any] = {}

        for name, param in signature.parameters.items():
            if name in kwargs:
                final_args[name] = kwargs[name]
            else:
                default = param.default

                assert not isinstance(default, Evaluated) or not isinstance(
                    default, Isolated
                ), "Cannot use both Evaluated and Isolated together."

                if isinstance(default, Evaluated):
                    final_args[name] = default.func()  # Call the function
                elif isinstance(default, Isolated):
                    assert name in kwargs, f"Argument '{name}' must be provided."
                    final_args[name] = copy.deepcopy(kwargs[name])
                else:
                    final_args[name] = copy.deepcopy(default)

        return func(**final_args)

    return wrapper


def check_isolation(d: Dict[str, Any]) -> Dict[str, Any]:
    """
    Checks isolation of a dictionary by creating a deep copy and modifying it.

    Args:
        d (Dict[str, Any]): The dictionary to check.

    Returns:
        Dict[str, Any]: A new dictionary with modified values.
    """
    isolated_dict = copy.deepcopy(d)
    isolated_dict["a"] = 0
    return isolated_dict


@smart_args
def example_function(
    a: int = 0, b: Evaluated = Evaluated(lambda: 1), c: Any = Isolated
) -> int:
    """
    An example function demonstrating the use of smart_args.

    Args:
        a (int): An integer value (default is 0).
        b (Evaluated): An instance of Evaluated (default evaluates to 1).
        c (Any): An instance of Isolated or a dictionary (default is an instance of Isolated).

    Returns:
        int: The sum of a, the evaluated value of b, and the value of c["a"] if c is a dictionary.

    Raises:
        TypeError: If c is an instance of Isolated and not provided as an argument.
    """

    if isinstance(c, Isolated):
        c = {}  # Use an empty dictionary by default if not provided

    # Use b.func() only if b is an instance of Evaluated
    b_value = b.func() if isinstance(b, Evaluated) else b

    return a + b_value + (c["a"] if isinstance(c, dict) else 0)
