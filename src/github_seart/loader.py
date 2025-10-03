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

