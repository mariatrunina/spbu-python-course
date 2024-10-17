import threading
import queue
import random
import time
import concurrent.futures


class ThreadPool:
    def __init__(self, pool_size):
        self.pool_size = pool_size
        self.tasks = queue.Queue()
        self.threads = []
        self.is_disposed = False

        for _ in range(pool_size):
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

    def worker(self):
        while not self.is_disposed:
            try:
                task = self.tasks.get(timeout=1)  # Таймаут для ожидания задачи
            except queue.Empty:
                continue

            try:
                result = task()  # Выполнение задачи
                print(f"Task completed with result: {result}")
            finally:
                self.tasks.task_done()

    def enqueue(self, task):
        if not self.is_disposed:
            self.tasks.put(task)

    def dispose(self):
        self.is_disposed = True
        for thread in self.threads:
            thread.join()  # Дожидаемся завершения потоков


def sample_task():
    time.sleep(random.uniform(0.1, 0.5))  # Симуляция работы
    return random.randint(1, 100)


def cartesian_product_sum(list1, list2):
    product = [(x, y) for x in list1 for y in list2]
    return sum(x + y for x, y in product)


def compute_sum_with_futures(list1, list2):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(cartesian_product_sum, list1, list2)
        return future.result()
