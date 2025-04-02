import pytest
from hw4.task1 import run_sync, run_threads, run_processes
from pathlib import Path


@pytest.fixture(scope="module")
def test_params():
    return {
        "n": 35,
        "times": 10,
    }


def test_performance_comparison(test_params):
    n = test_params["n"]
    times = test_params["times"]

    sync_time = run_sync(n, times)
    threads_time = run_threads(n, times)
    processes_time = run_processes(n, times)

    artifact_file = "tests/data/task1/artifact.txt"
    with open(artifact_file, "w") as f:
        f.write("Результаты сравнения производительности:\n\n")
        f.write(f"Синхронное выполнение ({times} раз): {sync_time:.2f} секунд\n")
        f.write(f"Использование потоков ({times} потоков): {threads_time:.2f} секунд\n")
        f.write(
            f"Использование процессов ({times} процессов): {processes_time:.2f} секунд\n\n"
        )

        f.write("Анализ результатов:\n")
        f.write("- Потоки в Python не ускоряют CPU-задачи из-за GIL\n")
        f.write("- Процессы позволяют достичь реального параллелизма\n")
        f.write(f"- Ускорение с процессами: {sync_time/processes_time:.1f}x\n")

    print("\n" + open(artifact_file).read())

    assert Path(artifact_file).exists()
