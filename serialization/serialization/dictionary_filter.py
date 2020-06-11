from typing import Any, Dict, Callable, Union, List


def filter_value(filter_function: Callable[[Any], bool],
                 input_element: Union[Dict, List, Any]) \
        -> Union[Dict, List, Any]:
    """"
    Filter and return a new nested dictionary/list where only
    leaf node values for which filter function returns true are kept
    @:param input_dict: Dictionary to filter
    @:param filter_parameter: Filter function applied to leaf node value
    Example:
    >>> # Identity
    >>> filter_value(lambda v: v,sample)
    >>> # enable to keep boolean values set to false and leaf empty dict/list
    >>> print(filter_value(lambda v: v is not None,sample))
    >>> # Keep boolean set to false and remove leaf empty dict/list
    >>> filter_value(lambda v: len(v) > 0 if isinstance(v, (dict, list))
    >>>                                             else v is not None,sample)
    It is similar to filter built-in function but with nested element management
    >>> l = [1, 2, 3, [], [[], [1, 2, []]]]
    >>> print(filter_value(lambda v: len(v) > 0 if isinstance(v, (
    >>>    dict, list)) else True, l)) # !=
    >>>    print(list(filter(
    >>>    lambda v: len(v) > 0 if isinstance(v, (dict, list)) else True, l)))
    """
    if not isinstance(input_element, (dict, list)):
        return input_element
    if isinstance(input_element, list):
        return [v for v in
                (filter_value(filter_function, v) for v in input_element)
                if
                filter_function(v)]
    return {k: v for k, v in
            ((k, filter_value(filter_function, v)) for k, v in
             input_element.items())
            if filter_function(v)}


def filter_null_and_empty_value(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """"
    Remove empty dictionary, list and null values from a dictionary
    """
    return filter_value(
        lambda v: len(v) > 0 if isinstance(v, (dict, list)) else v is not None,
        input_dict)
