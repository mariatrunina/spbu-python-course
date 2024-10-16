from typing import Callable, Any, OrderedDict, Tuple, Dict


def cache_result(
    max_cache_size: int = 0,
    verbose: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator for caching the results of a function based on its arguments.

    This decorator stores the results of function calls in an ordered cache.
    If the same arguments are passed to the function again, the cached result
    will be returned instead of recalculating it. The cache can be configured
    to hold a limited number of results. When the cache exceeds this limit,
    the oldest result will be removed.

    Args:
        max_cache_size (int): The maximum number of cached results to keep.
                               If set to 0, caching is disabled.
        verbose (bool): If True, prints messages indicating whether a result
                        was retrieved from the cache or calculated anew.

    Returns:
        Callable: A wrapper function that caches results of the decorated function.

    Example:
        @cache_result(max_cache_size=5, verbose=True)
        def slow_function(x: int) -> int:
            time.sleep(1)
            return x * 2

        result = slow_function(2)  # This will take time to compute.
        result = slow_function(2)  # This will return the cached result immediately.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        cache: OrderedDict[Tuple[Any, frozenset], Any] = OrderedDict()

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Create a cache key based on args and kwargs
            key = (args, frozenset(kwargs.items()))
            if key in cache:
                if verbose:
                    print("Retrieving result from cache...")
                return cache[key]

            result = func(*args, **kwargs)
            cache[key] = result

            # Maintain cache size
            if max_cache_size > 0 and len(cache) > max_cache_size:
                cache.popitem(last=False)  # Remove the oldest item

            if verbose:
                print("Calculating new result...")

            return result

        return wrapper

    return decorator
