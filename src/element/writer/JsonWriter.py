import json
from pathlib import Path

from src.element.Repository import Repository
from src.element.Set import Set


class JsonWriter:
    def __init__(self, set_path: str):
        self.set_path = Path(set_path)

    def write_set(self, set_obj):
        flattened_set = set_obj.flatten_set()
        json_output = json.dumps(flattened_set, cls=CustomEncoder, indent=4)
        try:
            with self.set_path.open("w", encoding="utf-8") as f:
                f.write(json_output)
            print(f"JSON has been written to {self.set_path}")
        except OSError as e:
            raise RuntimeError("Error while saving file", e) from e


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # Serialize Repository
        if isinstance(obj, Repository):
            return {
                meta.name: val.get_value()
                for meta, val in obj.get_all_metadata_values().items()
            }

        # Serialize Set
        if isinstance(obj, Set):
            return [self.default(e) for e in obj.get_elements()]

        # Default fallback
        return super().default(obj)
