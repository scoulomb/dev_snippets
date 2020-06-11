import unittest
from typing import Dict, Any, Callable, List
from unittest.mock import Mock

from serialization.dictionary_filter import filter_null_and_empty_value, filter_value


def make_input_dictionary():
    input_dictionary = {
        "title": "INTERNAL SERVER ERROR",
        "status": 500,
        "code": None,
        "falseBoolValue": False,
        "trueBoolValue": True,
        "source": {
            "pointer": "/path/to",
            "parameter": None,
            "example": "a sample string",
            "anId": 1,
            "emptyDict": {},
            "emptyList": [],
            "superNesting":
                {
                    "example": None,
                    "anId": 1,
                    "emptyDict": {},
                    "emptyList": [],
                }
        },
        "errors": [
            {"id": 1},
            {"desc": None}
        ]
    }
    return input_dictionary


class TestDictionaryFilter(unittest.TestCase):

    def test_filter_generic_nested_dict(self):
        identity_function: Callable[[Any], bool] = lambda v: v
        spy_identity_function = Mock(wraps=identity_function)

        input_dictionary: Dict[str, Any] = make_input_dictionary()
        expected_dictionary: Dict[str, Any] = {
            "title": "INTERNAL SERVER ERROR",
            "status": 500,
            "trueBoolValue": True,
            "source": {
                "pointer": "/path/to",
                "example": "a sample string",
                "anId": 1,
                "superNesting":
                    {
                        "anId": 1
                    }
            },
            "errors": [
                {"id": 1},
            ]
        }
        output = filter_value(spy_identity_function, input_dictionary)
        self.assertTrue(
            len(spy_identity_function.mock_calls) > len(input_dictionary))
        self.assertEqual(expected_dictionary,
                         output)

    def test_filter_generic_nested_list(self):
        filter_function: Callable[[Any], bool] = lambda v: len(
            v) > 0 if isinstance(v, (dict, list)) else True
        spy_filter_function = Mock(wraps=filter_function)

        input_list = [1, 2, 3, [], [[], [1, 2, []]]]
        expected_list: List[Any] = [1, 2, 3, [[1, 2, ]]]

        output = filter_value(spy_filter_function, input_list)
        self.assertTrue(
            len(spy_filter_function.mock_calls) == 10)
        self.assertEqual(expected_list,
                         output)

    def test_filter_null_and_empty_value(self):
        input_dictionary: Dict[str, Any] = make_input_dictionary()
        expected_dictionary: Dict[str, Any] = {
            "title": "INTERNAL SERVER ERROR",
            "status": 500,
            "falseBoolValue": False,
            "trueBoolValue": True,
            "source": {
                "pointer": "/path/to",

                "example": "a sample string",
                "anId": 1,
                "superNesting":
                    {
                        "anId": 1
                    }
            },
            "errors": [
                {"id": 1},
            ]
        }
        self.assertEqual(expected_dictionary,
                         filter_null_and_empty_value(input_dictionary))
