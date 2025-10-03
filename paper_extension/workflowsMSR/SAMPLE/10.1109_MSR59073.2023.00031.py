from pathlib import Path

from sampling_workflow.element.Loader import Loader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# Wasmizer: Curating WebAssembly-driven Projects on GitHub.


# start from github
# filter repo with more than 10 stars
# filter repo with more than 12 forks
# filter repo using C/C++
# filter repo that have wasm or webassembly or emscripten or web assembly as key word
# add a metadata with NLP tooling "WebAssemblyinReadme"
# filter repo having webassembly has important key word in readme
# add a metadata based on their heuristic "compilation_target_webassembly"
# filter repo having "compilation_target_webassembly"


def main():
    input_path = Path("github_dataset.json")  # * Start from GitHub

    # --- Metadata definitions ---
    url = Metadata.of_string("id")
    stars = Metadata.of_integer("stars")
    forks = Metadata.of_integer("forks")
    language = Metadata.of_string("language")
    keywords = Metadata.of_list("keywords", str)

    wasm_in_readme = Metadata.of_boolean("wasm_in_readme")
    compilation_target_wasm = Metadata.of_boolean("compilation_target_wasm")

    workflow = (
        WorkflowBuilder()
        # Input loader: all metadata included
        .input(
            Loader(
                input_path,
                url,
                stars,
                forks,
                language,
                keywords,
                wasm_in_readme,
                compilation_target_wasm,
            )
        )
        # * Filter repo with more than 10 stars
        .filter_operator("stars > 10")
        # * Filter repo with more than 12 forks
        .filter_operator("forks > 12")
        # * Filter repo using C or C++
        .filter_operator("language in ['C', 'C++']")
        # * Filter repo that have wasm/webassembly/emscripten/web assembly as keyword
        .filter_operator(
            "any(kw in keywords for kw in ['wasm', 'webassembly', 'emscripten', 'web assembly'])"
        )
        .add_metadata(Loader(input_path, url, wasm_in_readme))
        # * Filter repo having webassembly as important keyword in readme
        .filter_operator("wasm_in_readme")
        .add_metadata(Loader(input_path, url, compilation_target_wasm))
        # * Filter repo having 'compilation_target_webassembly'
        .filter_operator("compilation_target_wasm")
    )

    workflow.execute_workflow()
