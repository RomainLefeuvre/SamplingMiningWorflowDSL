import csv
from pathlib import Path
from typing import TYPE_CHECKING, Any
import logging
from sampling_mining_workflows_dsl.element.Loader import Loader
from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.Set import Set
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata

if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.metadata.MetadataValue import MetadataValue


class CsvLoader(Loader):
    def __init__(self, set_path: Path, *metadatas: Metadata):
        super().__init__(*metadatas)
        self.set_path = set_path
        self.set = Set()

    def load_set(self) -> Set:
        try:
            if self.set_path.is_dir():
                csv_files = sorted(self.set_path.glob("*.csv"))
                if not csv_files:
                    raise RuntimeError(
                        f"No CSV files found in directory: {self.set_path}"
                    )
            else:
                if not self.set_path.exists():
                    raise RuntimeError(f"File not found: {self.set_path}")
                csv_files = [self.set_path]

            for csv_file in csv_files:
                print(f"Loading CSV file: {csv_file}")
                with csv_file.open("r", newline="") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        try:
                            repository = self.create_repository_from_map(row)
                            if repository is not None:
                                self.set.add_element(repository)
                        except Exception as e:
                            logging.info(f"Row skipped due to {e} : {row}")
            return self.set
        except OSError as e:
            raise RuntimeError("Error reading the CSV file", e) from e

    def create_repository_from_map(self, csv_row: dict[str, Any]) -> Repository:
        id_metadata_value = csv_row.get(self.metadata_id_name)

        if id_metadata_value is None or id_metadata_value == "":
            raise ValueError(f"Invalid ID {self.metadata_id_name}")

        repo = Repository(self.metadatas.get(self.metadata_id_name))

        metadata_values: list[MetadataValue] = []
        for metadata in self.metadatas.values():
            try:
                metadata_value = metadata.create_metadata_value(csv_row.get(metadata.name))
                metadata_values.append(metadata_value)
            except Exception as e:
                raise ValueError(
                    f"Error creating metadata value for '{metadata.name}' with value '{csv_row.get(metadata.name)}'",
                ) from e

        repo.add_metadata_values(metadata_values)
        return repo
