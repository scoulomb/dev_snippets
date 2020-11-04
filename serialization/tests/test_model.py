import json
import unittest
from dataclasses import field, dataclass
from typing import List, Optional, Dict, cast, Any
# pycharm may change it but with docker it is  from serialization.model import Model same for others
from serialization.model import Model

from serialization.dictionary_filter import filter_null_and_empty_value


@dataclass
class Nested(Model):
    nested_name: str


@dataclass
class Container(Model):
    container_name: str
    objects: List[Nested] = field(default_factory=list)
    null_value: Optional[str] = None


# pylint: disable=unsubscriptable-object
class TestModel(unittest.TestCase):

    def test_json_to_object_to_json(self):
        nested_list = [
            Nested("tutu"), Nested("titi"), Nested("toto")
        ]
        container = Container("test", nested_list)
        container_to_json = json.loads(container.as_json_string())
        self.assertEqual(container, Container.from_dict(container_to_json))

    def test_json_dict_to_object(self):
        json_dict = {"container_name": "test",
                     "objects": [{"nested_name": "tutu"}, {"nested_name": "titi"}, {"nested_name": "toto"}]}

        expected_nested_list = [
            Nested("tutu"), Nested("titi"), Nested("toto")
        ]
        expected_container = Container("test", expected_nested_list)

        self.assertEqual(expected_container, Container.from_dict(json_dict))

    def test_object_with_null_value_to_json_string(self):
        nested_list = [
            Nested("tutu"), Nested("titi"), Nested("toto")
        ]
        container = Container("test", nested_list)
        expected_string = '{"container_name": "test", ' \
                          '"objects": [{"nested_name": "tutu"}, {"nested_name": "titi"}, {"nested_name": "toto"}]}'

        self.assertEqual(expected_string, container.as_json_string())

    def test_as_json_str_v1_produces_same_as_v2(self):
        # fix made in model nameserver pr#61
        nested_list = [
            Nested("tutu"), Nested("titi"), Nested("toto")
        ]
        container = Container("test", nested_list)
        self.assertEqual(container.as_json_string(), container.as_json_string_v2())
        print(f"container.as_json_string_v2(): {container.as_json_string_v2()}")

    def test_myexception(self):
        # Assume we now have an exception
        class MyBaseException(Exception):
            def __init__(self,
                         title: str = "INTERNAL SERVER ERROR",
                         ):
                self.title = f"My title {title}"

            def as_dict(self) -> Dict[str, Any]:
                # Here I can not use as_dict and do same as_json_string_v2 since it is not a dataclass
                s = json.loads(json.dumps(self, default=lambda o: o.__dict__))
                output = filter_null_and_empty_value(s)
                return cast(Dict[str, Any], output)

        # mimics what happens in try_run of api_handlers where we serialize an exception class containing an object
        nested_list = [
            Nested("tutu"), Nested("titi"), Nested("toto")
        ]
        container = Container("test", nested_list)

        print(
            f"Test of container within exception with container as json: {MyBaseException(container.as_json_string()).as_dict()}")
        print(
            f"Test of container within exception with container as dict : {MyBaseException(container.as_dict()).as_dict()}")
        print(
            f"Test of container within exception with container : {MyBaseException(container).as_dict()}")

        self.assertEqual(MyBaseException(container.as_json_string()).as_dict(),
                         {
                             'title': 'My title {"container_name": "test", "objects":'
                                      ' [{"nested_name": "tutu\"}, {"nested_name": "titi"},'
                                      ' {"nested_name": "toto"}]}'
                         }
                         )
        # => container is a valid quoted JSON (double), while exception is a dict (simple)
        # Python uses simple quote to not escape

        self.assertEqual(MyBaseException(container.as_dict()).as_dict(),
                         {
                             'title': "My title {'container_name': 'test', 'objects':"
                                      " [{'nested_name': 'tutu'}, {'nested_name': 'titi'},"
                                      " {'nested_name': 'toto'}]}"}
                         )
        # -> container is an invalid JSON (simple quote) but a python dict as the exception
        # Similar to
        # https://stackoverflow.com/questions/25242262/dump-to-json-adds-additional-double-quotes-and-escaping-of-quotes

        # We can also choose to not serialize
        self.assertEqual(
            MyBaseException(container).as_dict(),
            {'title': "My title Container(container_name='test', objects="
                      "[Nested(nested_name='tutu'), Nested(nested_name='titi'), "
                      "Nested(nested_name='toto')], null_value=None)"}
        )

        # finally when doing
        print(
            f"Test of container within exception with container as json with an exception dump to str"
            f"{json.dumps(MyBaseException(container.as_json_string()).as_dict())}")
        # it has to quote
        # unlike
        print(
            f"Test of container within exception with container as dict with an exception dump to str"
            f"{json.dumps(MyBaseException(container.as_dict()).as_dict())}")
        # No quote is added but it is an invalid JSON
        # mimics what happens in try_run when outputing the response

        # Both are not very satisfying, reason why we decided to move to list of error nameserver pr#63,66

        if __name__ == '__main__':
            unittest.main()
