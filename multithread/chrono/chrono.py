import functools
import time


def with_chrono(func):  # see decorator
    @functools.wraps(func)
    def wrapper_with_chrono(*args, **kwargs):
        start_time = time.perf_counter()

        func(*args, **kwargs)
        value = func(*args, **kwargs)

        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")

        return value

    return wrapper_with_chrono
