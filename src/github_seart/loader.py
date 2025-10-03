from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.element.loader.CsvLoader import CsvLoader
from src.element.Repository import Repository
from src.element.Set import Set
from src.github_seart.metadata import all_metadatas

if TYPE_CHECKING:
    from src.metadata.MetadataValue import MetadataValue

class SEARTGithubLoader(CsvLoader):
    def __init__(self, set_path: Path):
        super().__init__(*all_metadatas)
        self.set_path = set_path
        self.set = Set()

