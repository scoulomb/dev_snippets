import functools
import time

""""
Show usage of basic decorator.
Source:
https://realpython.com/primer-on-python-decorators/
Synthesis Both Please, But Never Mind the Bread and observation_decorators_with_without_argument.py file

"""


def repeat_with_chrono(_func=None, *, num_time: int = 2):
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

    # The decorator did not receive a function but num_time argument so as decorators with argument
    # The call to func is done by client (direct orsugar synthax)
    if _func is None:
        return decorator_repeat_with_chrono  # <- Adding this layer to process args
    else:
        # We need to call the function ourself
        return decorator_repeat_with_chrono(_func)


# Same test as in observation (except end of main and that we need to add num_time=5 in
# @repeat_with_chrono(num_time=5)
# def print_hello_3(username: str):

def print_hello_2(username: str):
    time.sleep(0.1)
    print(f"Hello {username}!")


@repeat_with_chrono(num_time=5)  # Need to add num_time key
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

    # If we remove parenthesis to print_hello3 we have NOW something printed
    print("---Decorator with syntax sugar without parenthesis")
    print_hello_3_without_parenthesis("Rene Coty")
    # It is equivalent to, thus the the call in decorator basic
    print("---Decorator without syntax sugar, simulating no parenthesis")
    print_hello_2 = (repeat_with_chrono)(print_hello_2)
    print_hello_2("Rene Coty")

# Note when using syntax sugar num_time printed out of the main
