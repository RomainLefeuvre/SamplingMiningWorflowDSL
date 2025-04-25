import json
from typing import Any, Dict, List

from newDSL.element.Repository import Repository
from newDSL.element.Set import Set
from newDSL.element.Writter import Writter
from newDSL.metadata.Metadata import Metadata
from newDSL.metadata.MetadataValue import MetadataValue


class JsonWriter(Writter):
    def __init__(self, set_path: str):
        self.set_path = set_path

    def write_set(self, set_: Set):
        """
        Serialize the set to JSON and write it to a file.
        """
        # Serialize the set using custom serializers
        json_output = json.dumps(
            set_,
            default=self._serialize_element,
            indent=4
        )

        # Save JSON output to file
        try:
            with open(self.set_path, "w") as writer:
                writer.write(json_output)
                print(f"JSON has been written to {self.set_path}")
        except IOError as e:
            raise RuntimeError("Error while saving file") from e

    def _serialize_element(self, element: Any) -> Any:
        """
        Custom serializer for Repository and Set objects.
        """
        if isinstance(element, Repository):
            return self._serialize_repository(element)
        elif isinstance(element, Set):
            return self._serialize_set(element)
        else:
            raise TypeError(f"Object of type {type(element).__name__} is not JSON serializable")

    def _serialize_repository(self, repository: Repository) -> Dict[str, Any]:
        """
        Serialize a Repository object to a dictionary.
        """
        json_object = {}
        for metadata, metadata_value in repository.get_all_metadata_values().items():
            json_object[metadata.name] = str(metadata_value.get_value())
        return json_object

    def _serialize_set(self, set_: Set) -> List[Any]:
        """
        Serialize a Set object to a list of serialized elements.
        """
        elements_array = []
        for child_element in set_.get_elements():
            elements_array.append(self._serialize_element(child_element))
        return elements_array