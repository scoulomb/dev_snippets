import json
import unittest
from dataclasses import field, dataclass
from typing import List, Optional

from serialization.model import Model


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


if __name__ == '__main__':
    unittest.main()
