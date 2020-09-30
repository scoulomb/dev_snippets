""""
Show usage of Python parallel_map.
Source:
LB, PR#196
"""

import multiprocessing
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Iterable, Callable, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


def parallel_map(func: Callable[[Input], Output], iterable: Iterable[Input]) -> Iterable[Output]:
    """
    Parallel version of `map`, backed by threads.
    Only suitable to do IO in parallel (not for CPU intensive tasks)
    """
    number_of_workers = multiprocessing.cpu_count() * 5
    with ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        return executor.map(func, iterable)

