import pytest
import sys
import os
import random
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.threads import ThreadPool


@pytest.fixture
def thread_pool():
    pool_size = 5
    pool = ThreadPool(pool_size=pool_size)
    yield pool
    pool.dispose()


def test_enqueue_task(thread_pool):
    thread_pool.enqueue(sample_task)
    assert len(thread_pool.tasks) == 1  # Изменено на len для проверки количества задач


def test_thread_count(thread_pool):
    assert len(thread_pool.threads) == thread_pool.pool_size


def test_task_completion(thread_pool):
    results = []

    def collect_result():
        result = sample_task()
        results.append(result)

    for _ in range(10):
        thread_pool.enqueue(collect_result)

    # Даем время для выполнения задач
    time.sleep(2)

    # Проверяем, что все задачи были выполнены
    assert len(results) == 10


def test_dispose(thread_pool):
    thread_pool.dispose()
    assert thread_pool.is_disposed is True


def sample_task() -> int:
    """
    A sample task that simulates work by sleeping for a random amount of time
    and then returns a random integer.

    Returns:
        int: A random integer between 1 and 100.
    """
    time.sleep(random.uniform(0.1, 0.5))  # Simulate some work
    return random.randint(1, 100)
