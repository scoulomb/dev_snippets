import json

from serialization.tests.test_model import Nested, Container

if __name__ == "__main__":

    nested_list = [
                Nested("tutu"), Nested("titi"), Nested("toto")
            ]
    container = Container("test", nested_list)

    container_to_json = json.loads(container.as_json_string())
    print(f"main: {container_to_json}")




