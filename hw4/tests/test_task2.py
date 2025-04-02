import math
from pathlib import Path
import time
import pytest
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from hw4.task2 import integrate


@pytest.fixture
def cpu_count():
    return os.cpu_count() or 1


def generate_report(executor_class, max_workers):
    results = []
    func = math.cos
    a, b = 0, math.pi / 2

    for n_jobs in range(1, max_workers + 1):
        start_time = time.time()
        integrate(func, a, b, n_jobs=n_jobs, executor_class=executor_class)
        duration = time.time() - start_time
        results.append((n_jobs, duration))

    return results


def test_performance_comparison(cpu_count):
    max_workers = cpu_count * 2

    thread_results = generate_report(ThreadPoolExecutor, max_workers)

    process_results = generate_report(ProcessPoolExecutor, max_workers)

    summary_report = Path("tests/data/task2/artifact.txt")
    with open(summary_report, "w") as f:
        f.write(
            "Сравнение производительности ThreadPoolExecutor и ProcessPoolExecutor\n\n"
        )
        f.write("Количество воркеров, Потоки (сек), Процессы (сек)\n")

        for (n_jobs, thread_time), (_, process_time) in zip(
            thread_results, process_results
        ):
            f.write(f"{n_jobs},{thread_time:.4f},{process_time:.4f}\n")

        f.write("\nВыводы:\n")
        f.write(
            "1. Для CPU-интенсивных задач (как интегрирование) процессы обычно быстрее потоков\n"
        )
        f.write("2. Количество воркеров для потоков почти не влияет на результат\n")
        f.write(
            "3. Оптимальное количество воркеров для процессов обычно около числа физических ядер CPU,"
            " в моем случае 10 ядер M1 Pro, но в нём 8 ядер производительности что и является оптимальным в данном случае.\n"
        )
        f.write(
            "4. Слишком большое количество воркеров может снизить производительность"
        )

    assert os.path.exists(summary_report)
