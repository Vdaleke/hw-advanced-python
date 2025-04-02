import time
from threading import Thread
from multiprocessing import Process
from typing import List


def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


def run_sync(n, times=10):
    start = time.time()
    for _ in range(times):
        fib(n)
    end = time.time()
    return end - start


def run_threads(n, times=10):
    threads: List[Thread] = []
    start = time.time()
    for _ in range(times):
        t = Thread(target=fib, args=(n,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    end = time.time()
    return end - start


def run_processes(n, times=10):
    processes: List[Process] = []
    start = time.time()
    for _ in range(times):
        p = Process(target=fib, args=(n,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    end = time.time()
    return end - start
