from concurrent.futures import ThreadPoolExecutor, as_completed


def worker(f, a, step, start, end):
    partial_acc = 0
    for i in range(start, end):
        partial_acc += f(a + i * step) * step
    return partial_acc


def integrate(f, a, b, *, n_jobs=1, n_iter=10000000, executor_class=ThreadPoolExecutor):
    step = (b - a) / n_iter
    futures = []

    chunk_size = n_iter // n_jobs
    with executor_class(max_workers=n_jobs) as executor:
        for i in range(n_jobs):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i != n_jobs - 1 else n_iter
            futures.append(executor.submit(worker, f, a, step, start, end))

        total = sum(f.result() for f in as_completed(futures))

    return total
