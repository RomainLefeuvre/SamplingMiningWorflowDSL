from pathlib import Path

from newDSL2.element.loader.JsonLoader import JsonLoader
from newDSL2.metadata.Metadata import Metadata


class LoaderFactory:
    @staticmethod
    def json_loader(set_path: str, *metadatas: Metadata):
        return JsonLoader(Path(set_path), *metadatas)

    @staticmethod
    def json_loader_from_path(set_path: Path, *metadatas: Metadata):
        return JsonLoader(set_path, *metadatas)