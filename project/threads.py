import threading
from typing import Callable, List


class ThreadPool:
    def __init__(self, pool_size: int) -> None:
        """
        Initializes the ThreadPool with a specified number of threads.

        Args:
            pool_size (int): The number of threads in the pool.
        """
        self.pool_size = pool_size
        self.tasks: List[Callable] = []
        self.lock = threading.Lock()
        self.threads: List[threading.Thread] = []
        self.is_disposed = False
        self._init_threads()

    def _init_threads(self) -> None:
        """Initializes the worker threads."""
        for _ in range(self.pool_size):
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

    def worker(self) -> None:
        """
        The worker function that processes tasks from the tasks list.
        It runs in separate threads and continuously checks for tasks to execute.
        """
        while not self.is_disposed:
            with self.lock:
                if self.tasks:
                    task = self.tasks.pop(0)
                else:
                    task = None

            if task is not None:

                task()

    def enqueue(self, task: Callable) -> None:
        """
        Adds a task to the tasks list. The task should be callable.

        Args:
            task (Callable): The task to be executed by the thread pool.
        """
        if not self.is_disposed:
            with self.lock:
                self.tasks.append(task)

    def dispose(self) -> None:
        """
        Disposes of the thread pool, stopping all threads and waiting for them to finish.
        """
        self.is_disposed = True
        for thread in self.threads:
            thread.join()
