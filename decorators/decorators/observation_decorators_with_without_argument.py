import functools
import time

""""
Show usage of basic decorator.
Source:
https://realpython.com/primer-on-python-decorators/
Synthesis Decorators With Arguments and decorator_basic.py file

"""


def repeat_with_chrono(num_time: int):
    print(f"Num time: {num_time}")

    def decorator_repeat_with_chrono(func):  # <- Adding this layer to process args
        @functools.wraps(func)
        def wrapper_repeat_with_chrono(*args, **kwargs):
            print("Inside")
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


@repeat_with_chrono
def print_hello_3_without_parenthesis(username: str):
    time.sleep(0.1)
    print(f"Hello {username}!")


if __name__ == "__main__":
    print("---Decorator with syntax sugar with parenthesis")
    print_hello_3("Rene Coty")

    # If we remove parenthesis to print_hello3 we have nothing printed
    print("---Decorator with syntax sugar without parenthesis")
    print_hello_3_without_parenthesis("Rene Coty")
    # It is equivalent to, thus the the call in decorator basic
    print("---Decorator without syntax sugar, simulating no parenthesis")
    print_hello_2 = (repeat_with_chrono)(print_hello_2)
    print_hello_2("Rene Coty")
    # We can see the function name is printed instead of num time in that case and we do not go further in code
    # as we would need more parenthesis
    # Here tadam error
    try:
        print_hello_2("Rene Coty")()
    except TypeError as e:
        print(e)
    # To make it compatible if we do not have a function we will call the decorator directly (effect of the parenthesis)
