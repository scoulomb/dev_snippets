from __future__ import annotations

import json
from abc import ABC
from dataclasses import dataclass
from typing import Dict, Any, TypeVar

import jsonpickle
import marshmallow_dataclass

from serialization.dictionary_filter import filter_null_and_empty_value


@dataclass
class Model(ABC):
    def as_json_string(self):
        """"
        We call filter_null_and_empty_value to not serialize none field
        Alternatively we could fill all default value to avoid this call
        But it is not possible for some fields:
        such as _ref, and host.name == host.ipv4addr.hostwith Infoblox API
        https://www.educative.io/edpresso/what-is-the-difference-between-jsonloads-and-jsondumps
        Thus it was not done in as_json_string for the F5
        
        Can we do better than this call chain?
        """""

        # Encoding with pickle
        print(jsonpickle.encode(self, unpicklable=False))
        print(type(jsonpickle.encode(self, unpicklable=False)))

        # Encoding with dumps
        # print(json.dumps(self)) # this work on dict but class would return:
        # "Object of type Container is not JSON serializable"
        print(json.dumps(self, default=lambda o: o.__dict__))  # It i strictly  equivalent to "Encoding with pickle"
        print(type(json.dumps(self, default=lambda o: o.__dict__)))  # And it is a string

        # For both null value are not filtered
        # This is the failing return

        # Convert str to dict
        print(json.loads(json.dumps(self, default=lambda o: o.__dict__)))  # We dump to have dict
        print(type(json.loads(json.dumps(self, default=lambda o: o.__dict__))))  # type here is a dict

        # Filter dict
        print(filter_null_and_empty_value(
            json.loads(json.dumps(self, default=lambda o: o.__dict__))))  # We filter null value in this dict

        # in dns_automation/exception/dns_exception.py we do exactly this with pickle or dumps
        # (as now get rid of this lib in that PR)
        # in exception we stop there as return a dict

        # Convert to string
        print(json.dumps(filter_null_and_empty_value(
            json.loads(json.dumps(self, default=lambda o: o.__dict__)))))  # We convert  back to a string
        # ===> This is the current return where we take the filter_null_and_empty_value done initially for exception
        print(type(json.dumps(
            filter_null_and_empty_value(json.loads(json.dumps(self, default=lambda o: o.__dict__))))))  # type is string

        # Note: did not use marshamallow as it needs the class name
        # https://pypi.org/project/marshmallow-dataclass/

        """"
        Print output is
        {"container_name": "test", "null_value": null, "objects": [{"nested_name": "tutu"}, {"nested_name": "titi"}, {"nested_name": "toto"}]}
        <class 'str'>
        {"container_name": "test", "objects": [{"nested_name": "tutu"}, {"nested_name": "titi"}, {"nested_name": "toto"}], "null_value": null}
        <class 'str'>
        {'container_name': 'test', 'objects': [{'nested_name': 'tutu'}, {'nested_name': 'titi'}, {'nested_name': 'toto'}], 'null_value': None}
        <class 'dict'>
        {'container_name': 'test', 'objects': [{'nested_name': 'tutu'}, {'nested_name': 'titi'}, {'nested_name': 'toto'}]}
        {"container_name": "test", "objects": [{"nested_name": "tutu"}, {"nested_name": "titi"}, {"nested_name": "toto"}]}
        <class 'str'>
        """
        return json.dumps(filter_null_and_empty_value(json.loads(json.dumps(self, default=lambda o: o.__dict__))))
        # return json.dumps(self, default=lambda o: o.__dict__)
        # => this comment initial return, would make a json with none value in dict
        # and thus  make test fail and infoblox API call fail as none value are not ignored

    @classmethod
    def from_dict(cls: SUB_MODEL, data: Dict[str, Any]) -> SUB_MODEL:
        model_schema = marshmallow_dataclass.class_schema(cls)
        return model_schema().load(data)


# SUB_MODEL can only be a class inheriting from Model
SUB_MODEL = TypeVar('SUB_MODEL', bound=Model)
