import functools
import time

""""
Show usage of basic decorator.
Source:
https://realpython.com/primer-on-python-decorators/
Synthesis until: Timing Functions

"""


def do_twice_with_chrono(func):
    @functools.wraps(func)
    def wrapper_do_twice_with_chrono(*args, **kwargs):
        start_time = time.perf_counter()

        func(*args, **kwargs)
        value = func(*args, **kwargs)

        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")

        return value

    return wrapper_do_twice_with_chrono


def print_hello_0(username: str):
    time.sleep(0.1)
    print(f"Hello {username}!")


@do_twice_with_chrono
def print_hello_1(username: str):
    time.sleep(0.1)
    print(f"Hello {username}!")


if __name__ == "__main__":
    print_hello_0("Rene Coty")

    print("---Decorator without syntax sugar")
    print_hello_0 = do_twice_with_chrono(print_hello_0)
    print_hello_0("Rene Coty")
    print("---Decorator with syntax sugar")
    print_hello_1("Rene Coty")

