import pytest
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.threads import (
    ThreadPool,
    sample_task,
    compute_sum_with_futures,
)  


@pytest.fixture
def thread_pool():
    pool_size = 5
    pool = ThreadPool(pool_size=pool_size)
    yield pool
    pool.dispose()  

def test_enqueue_task(thread_pool):
    thread_pool.enqueue(sample_task)
    assert thread_pool.tasks.qsize() == 1  # Проверка, что задача добавлена


def test_thread_count(thread_pool):
    assert len(thread_pool.threads) == thread_pool.pool_size  # Проверка размера пула


def test_task_completion(thread_pool):
    results = []

    def collect_result():
        result = sample_task()
        results.append(result)
        return result

    for _ in range(10):
        thread_pool.enqueue(collect_result)

    # Дождаться завершения всех задач перед вызовом dispose
    thread_pool.tasks.join()  # Ожидание завершения всех задач

    # Теперь можно вызывать dispose, так как все результаты должны быть собраны
    thread_pool.dispose()

    assert len(results) == 10  # Проверка, что все задачи выполнены


def test_dispose(thread_pool):
    thread_pool.dispose()
    assert thread_pool.is_disposed is True  # Проверка, что пул закрыт


def test_cartesian_product_sum():
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    result = compute_sum_with_futures(list1, list2)
    assert result == 63  # Ожидаемое значение обновлено на 63
