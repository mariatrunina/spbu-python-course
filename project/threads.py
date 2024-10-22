import threading
import queue
import random
import time
import concurrent.futures
from typing import Callable, List


class ThreadPool:
    def __init__(self, pool_size: int) -> None:
        """
        Initializes the ThreadPool with a specified number of threads.

        Args:
            pool_size (int): The number of threads in the pool.
        """
        self.pool_size = pool_size
        self.tasks: queue.Queue[Callable] = queue.Queue()
        self.threads: List[threading.Thread] = []
        self.is_disposed = False

        for _ in range(pool_size):
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

    def worker(self) -> None:
        """
        The worker function that processes tasks from the queue.
        It runs in separate threads and continuously checks for tasks to execute.
        """
        while not self.is_disposed:
            try:
                task: Callable = self.tasks.get(
                    timeout=1
                )  # Timeout for waiting for a task
            except queue.Empty:
                continue

            try:
                result = task()  # Execute the task
                print(f"Task completed with result: {result}")
            finally:
                self.tasks.task_done()

    def enqueue(self, task: Callable) -> None:
        """
        Adds a task to the queue. The task should be callable.

        Args:
            task (Callable): The task to be executed by the thread pool.
        """
        if not self.is_disposed:
            self.tasks.put(task)

    def dispose(self) -> None:
        """
        Disposes of the thread pool, stopping all threads and waiting for them to finish.
        """
        self.is_disposed = True
        for thread in self.threads:
            thread.join()  # Wait for threads to finish


def sample_task() -> int:
    """
    A sample task that simulates work by sleeping for a random amount of time
    and then returns a random integer.

    Returns:
        int: A random integer between 1 and 100.
    """
    time.sleep(random.uniform(0.1, 0.5))  # Simulate some work
    return random.randint(1, 100)


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
