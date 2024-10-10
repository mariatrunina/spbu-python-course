import inspect
import copy


# Определяем классы Evaluated и Isolated
class Evaluated:
    def __init__(self, func):
        self.func = func


class Isolated:
    pass


# Декоратор smart_args
def smart_args(func):
    signature = inspect.signature(func)

    def wrapper(**kwargs):
        for name in kwargs:
            assert (
                name in signature.parameters
            ), f"Argument '{name}' is not a valid argument."

        final_args = {}

        for name, param in signature.parameters.items():
            if name in kwargs:
                final_args[name] = kwargs[name]
            else:
                default = param.default

                assert not isinstance(default, Evaluated) or not isinstance(
                    default, Isolated
                ), "Cannot use both Evaluated and Isolated together."

                if isinstance(default, Evaluated):
                    final_args[name] = default.func()  # Вызываем функцию
                elif isinstance(default, Isolated):
                    assert name in kwargs, f"Argument '{name}' must be provided."
                    final_args[name] = copy.deepcopy(kwargs[name])
                else:
                    final_args[name] = copy.deepcopy(default)

        return func(**final_args)

    return wrapper


# Функция для проверки изоляции
def check_isolation(d):
    isolated_dict = copy.deepcopy(d)
    isolated_dict["a"] = 0
    return isolated_dict


@smart_args
def example_function(a=0, b=Evaluated(lambda: 1), c=Isolated):
    # Проверяем, является ли c экземпляром Isolated и обрабатываем соответствующим образом
    if isinstance(c, Isolated):
        c = {}  # По умолчанию используем пустой словарь, если не предоставлен

    # Используем b.func() только если b является экземпляром Evaluated
    b_value = b.func() if isinstance(b, Evaluated) else b

    return a + b_value + (c["a"] if isinstance(c, dict) else 0)
