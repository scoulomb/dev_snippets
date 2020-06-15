import functools
import time

""""
Show usage of basic decorator.
Source:
https://realpython.com/primer-on-python-decorators/
Synthesis Decorators With Arguments and decorator_basic.py file

"""


def repeat_with_chrono(num_time: int):
    def decorator_repeat_with_chrono(func):  # <- Adding this layer to process args
        @functools.wraps(func)
        def wrapper_repeat_with_chrono(*args, **kwargs):
            start_time = time.perf_counter()

            for _ in range(num_time):
                value = func(*args, **kwargs)

            end_time = time.perf_counter()
            run_time = end_time - start_time
            print(f"Finished {func.__name__!r} in {run_time:.4f} secs")

            return value

        return wrapper_repeat_with_chrono

    return decorator_repeat_with_chrono  # <- Adding this layer to process args


def print_hello_2(username: str):
    time.sleep(0.1)
    print(f"Hello {username}!")


@repeat_with_chrono(5)
def print_hello_3(username: str):
    time.sleep(0.1)
    print(f"Hello {username}!")


if __name__ == "__main__":
    print("---Decorator without syntax sugar")
    print_hello_2 = (repeat_with_chrono(5))(print_hello_2)
    # <- if we compare with decorator_basic file, once we did (repeat_with_chrono(5)),
    # we come back to that nominal case and it matches the added layer to process args in repeat_with_chrono
    print_hello_2("Rene Coty")
    print("---Decorator with syntax sugar")
    print_hello_3("Rene Coty")
    # Check call OK
    # Easy to explain without syntax sugar
    # with_infoblox_api implements this ! and adds an arguments, other stuff sthg else
    # Signature of decorator return value (returned wrapper) must match function it decorates
    # Not unittest directly exception when raising=ng exception

