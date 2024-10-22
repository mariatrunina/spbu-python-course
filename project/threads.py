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
