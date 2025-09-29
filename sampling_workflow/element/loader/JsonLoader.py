import json
from pathlib import Path
from typing import Any

from sampling_workflow.element.Loader import Loader
from sampling_workflow.element.Repository import Repository
from sampling_workflow.element.Set import Set
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.metadata.MetadataValue import MetadataValue


class JsonLoader(Loader):
    def __init__(self, set_path: Path, *metadatas: Metadata):
        super().__init__(*metadatas)
        self.set_path = set_path
        self.set = Set()

    def load_set(self) -> Set:
        if not self.set_path.exists():
            raise RuntimeError(f"File not found: {self.set_path}")

        try:
            with self.set_path.open("r") as reader:
                # Parse JSON array to a list of dictionaries
                json_list: list[dict[str, Any]] = json.load(reader)
                self.set = Set()
                for json_obj in json_list:
                    repository = self.create_repository_from_map(json_obj)
                    self.set.add_element(repository)
                return self.set
        except OSError as e:
            raise RuntimeError("Error reading the JSON file") from e

    def create_repository_from_map(self, json_object: dict[str, Any]) -> Repository:
        repo = Repository(self.metadatas["id"])
        metadata_values: list[MetadataValue] = []
        for metadata in self.metadatas.values():
            value = metadata.type(json_object.get(metadata.name))
            metadata_values.append(metadata.create_metadata_value(value))
        repo.add_metadata_values(metadata_values)
        return repo

    @staticmethod
    def parse_args(args: list[str]) -> dict[str, str]:
        import argparse

        default_input_path = Path(__file__).parent / "input.json"

        parser = argparse.ArgumentParser(description="Sampling Workflow")
        parser.add_argument(
            "-i",
            "--inputPath",
            type=str,
            default=str(default_input_path),
            help="Input path file",
        )
        parsed_args = parser.parse_args(args)
        return vars(parsed_args)
