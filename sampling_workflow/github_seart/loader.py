from pathlib import Path
from typing import TYPE_CHECKING, Any

from sampling_workflow.element.loader.CsvLoader import CsvLoader
from sampling_workflow.element.Repository import Repository
from sampling_workflow.element.Set import Set
from sampling_workflow.github_seart.metadata import all_metadatas

if TYPE_CHECKING:
    from sampling_workflow.metadata.MetadataValue import MetadataValue

class SEARTGithubLoader(CsvLoader):
    def __init__(self, set_path: Path):
        super().__init__(*all_metadatas)
        self.set_path = set_path
        self.set = Set()

    def create_repository_from_map(self, csv_row: dict[str, Any]) -> Repository:
        id_metadata_value = csv_row.get(self.metadata_id_name)

        if id_metadata_value is None or id_metadata_value == "":
            raise ValueError(f"Invalid ID '{self.metadata_id_name}' in row: {csv_row}")

        repo = Repository(self.metadatas.get(self.metadata_id_name))

        metadata_values: list[MetadataValue] = []
        for metadata in self.metadatas.values():
            # Convert string value from CSV using the type defined in metadata
            if metadata.type is list:
                string_list = csv_row.get(metadata.name)
                value = (
                    metadata.type(csv_row.get(metadata.name).split(";"))
                    if string_list != ""
                    else []
                )
                metadata_value = metadata.create_metadata_value(value)
            else:
                try:
                    metadata_value = metadata.create_metadata_value(
                        csv_row.get(metadata.name)
                    )
                except Exception as _:
                    return None # Skip this repository if conversion fails

            if metadata_value is not None:
                metadata_values.append(metadata_value)

        repo.add_metadata_values(metadata_values)
        return repo
