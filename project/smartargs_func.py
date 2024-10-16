import inspect
import copy
from typing import Callable, Any, Dict


class Evaluated:
    """A class that wraps a function to be evaluated when called."""

    def __init__(self, func: Callable[[], Any]):
        self.func = func


class Isolated:
    """A marker class used to indicate that an argument should be isolated."""

    pass


def smart_args(func: Callable) -> Callable:
    """A decorator that processes keyword arguments for a function."""
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


@smart_args
def example_function(
    a: int = 0, b: Evaluated = Evaluated(lambda: 1), c: Any = Isolated()
) -> int:
    if isinstance(c, Isolated):
        c = {}  # Инициализируем c как пустой словарь

    b_value = b.func() if isinstance(b, Evaluated) else b

    return a + b_value + (c.get("a", 0) if isinstance(c, dict) else 0)
