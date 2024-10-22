import threading
import queue
import random
import time
import concurrent.futures
from typing import Callable, List


def cartesian_product_sum(list1: List[int], list2: List[int]) -> int:
    """
    Computes the sum of the Cartesian product of two lists.

    Args:
        list1 (List[int]): The first list of integers.
        list2 (List[int]): The second list of integers.

    Returns:
        int: The sum of the Cartesian product of the two lists.
    """
    product = [(x, y) for x in list1 for y in list2]
    return sum(x + y for x, y in product)


def compute_sum_with_futures(list1: List[int], list2: List[int]) -> int:
    """
    Computes the sum of the Cartesian product of two lists using futures.

    Args:
        list1 (List[int]): The first list of integers.
        list2 (List[int]): The second list of integers.

    Returns:
        int: The sum of the Cartesian product of the two lists.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(cartesian_product_sum, list1, list2)
        return future.result()
