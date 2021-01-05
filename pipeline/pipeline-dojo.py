from functools import partial
from typing import TypeVar, List, Callable, Any

# from functools import reduce
from toolz import pipe, curry

# python 3.9,
# add bound => https://stackoverflow.com/questions/50185027/why-are-single-type-constraints-disallowed-in-python
ValidSearchTerm = TypeVar('ValidSearchTerm', bound=str)


def validate_input(search_item: str) -> ValidSearchTerm:
    pass


Title = TypeVar('Title', bound=str)


def search(term: ValidSearchTerm) -> List[Title]:
    pass


Summary = TypeVar('Summary', bound=str)


def retrieve_summaries(titles: List[Title]) -> List[Summary]:
    def _retrieve_summary(title: Title) -> Summary:
        pass

    pass


T = TypeVar('T')
U = TypeVar('U')


def compose_v0(f1: Callable[[T], Any], f2, f3: Callable[[Any], U]) -> Callable[[T], U]:
    def composition(x):
        return f1(f2(f3(x)))

    return composition


def compose_v1(f1: Callable[[T], Any], f2, f3: Callable[[Any], U]) -> Callable[[T], U]:
    return lambda x: f1(f2(f3(x)))


def reduce(function: Callable[[T, T], T], items: List[T], initial_value=None) -> T:
    if initial_value is None and len(items) == 0:
        raise RuntimeError('shit')
    if len(items) == 0:
        return initial_value
    if len(items) == 1:
        return items[0]
    previous_iteration = items[0]
    for item in items[1:]:
        a = previous_iteration
        b = item
        previous_iteration = function(a, b)
    return previous_iteration


def compose_v2(f1: Callable[[T], Any], f2, f3: Callable[[Any], U]) -> Callable[[T], U]:
    def compose2(f1, f2) -> Callable:
        return lambda x: f1(f2(x))

    functions = [f1, f2, f3]
    return reduce(compose2, functions)


def compose_v3(*args) -> Callable:
    def compose2(f1, f2) -> Callable:
        return lambda x: f1(f2(x))

    return reduce(compose2, args)


def compose_reverse_v0(f1, f2, f3) -> Callable:
    def composition(x):
        return f3(f2(f1(x)))

    return composition


def compose_reverse_v1(f1, f2, f3) -> Callable:
    return lambda x: f3(f2(f1(x)))


def compose_reverse_v2(f1: Callable[[T], Any], f2, f3: Callable[[Any], U]) -> Callable[[T], U]:
    def compose2(f1, f2) -> Callable:
        return lambda x: f1(f2(x))

    functions = [f3, f2, f1]
    return reduce(compose2, functions)


def compose_reverse_v3(*args) -> Callable:
    def compose2(f1, f2) -> Callable:
        return lambda x: f1(f2(x))

    return reduce(compose2, list(reversed(args)))


def compose_reverse_v4(*args) -> Callable:
    return compose_v3(list(reversed(args)))


def main(search_item: str) -> None:
    # compose = ° (maths)
    pipeline: Callable[[str], List[Summary]] = compose_v0(retrieve_summaries, search, validate_input)
    pipeline(search_item)

    pipeline2: Callable[[str], List[Summary]] = compose_reverse_v1(validate_input, search, retrieve_summaries)
    pipeline2(search_item)

    output: List[Summary] = pipe(search_item,
                                 validate_input,
                                 search,
                                 retrieve_summaries)

    print(output)


def partial_and_curry_are_linked():
    def f(a, b):
        return a + b

    p1 = partial(f, 1)
    p1(2)  # = 3

    @curry  # See https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence
    def g(a, b):
        return a + b

    p2 = g(1)
    p2(2)  # = 3

    # manually
    def h(a, b):
        return a + b

    p3 = lambda b: h(1, b)
    p3(2)  # = 3


    def super_complex_function(logger, http_caller, a, b):
        pass

    simpler_function = partial(super_complex_function, 'logger specific', 'http caller specific')  # dependency injection
    simpler_function('a', 'b')
    # --> class with dependency injection in __init__ === special case of partial application of a function


if __name__ == "__main__":
    search_item = "hello"
    main(search_item)
