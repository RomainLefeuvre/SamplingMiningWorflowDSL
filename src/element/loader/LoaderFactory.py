from pathlib import Path

from sampling_workflow.element.loader.JsonLoader import JsonLoader
from sampling_workflow.metadata.Metadata import Metadata


class LoaderFactory:
    @staticmethod
    def json_loader(set_path: str, *metadatas: Metadata):
        return JsonLoader(Path(set_path), *metadatas)

    @staticmethod
    def json_loader_from_path(set_path: Path, *metadatas: Metadata):
        return JsonLoader(set_path, *metadatas)
