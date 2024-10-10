import inspect  
import copy     
import pytest
import random

# Определяем классы Evaluated и Isolated
class Evaluated:
    def __init__(self, func):
        self.func = func

class Isolated:
    pass

# Ваш декоратор
def smart_args(func):
    signature = inspect.signature(func)

    def wrapper(**kwargs):
        for name in kwargs:
            assert name in signature.parameters, f"Argument '{name}' is not a valid argument."

        final_args = {}
        
        for name, param in signature.parameters.items():
            if name in kwargs:
                final_args[name] = kwargs[name]
            else:
                default = param.default
                
                assert not isinstance(default, Evaluated) or not isinstance(default, Isolated), \
                    "Cannot use both Evaluated and Isolated together."

                if isinstance(default, Evaluated):
                    final_args[name] = default.func()
                elif isinstance(default, Isolated):
                    assert name in kwargs, f"Argument '{name}' must be provided."
                    final_args[name] = copy.deepcopy(kwargs[name])
                else:
                    final_args[name] = copy.deepcopy(default)

        return func(**final_args)

    return wrapper
