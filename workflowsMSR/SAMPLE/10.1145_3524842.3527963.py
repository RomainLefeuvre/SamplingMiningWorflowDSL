from sampling_workflow.element.Loader import Loader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# Do Customized Android Frameworks Keep Pace with Android?
# start from wikipedia list
# add metadata manually ==> customized_android_framework
# filter project that customized the android framework base
# add metadata manually ==> source_code_available
# filter project that offer access to the source code of their customization
# add metadata manually ==> use a VCS
# filter project project that use a version control system
# add metadata manually ==> is_discontinued
# filter out project that are discontinued
# add metadata manually ==> number_of_merge_change_android
# filter repo with more than one number_of_merge_change_android


def main():
    # --- Workflow ---
    url = Metadata.of_string("id")  # GitHub repo id / URL
    customized_android_framework = Metadata.of_boolean("customized_android_framework")
    source_code_available = Metadata.of_boolean("source_code_available")
    use_vcs = Metadata.of_boolean("use_vcs")
    is_discontinued = Metadata.of_boolean("is_discontinued")
    number_of_merge_change_android = Metadata.of_long("number_of_merge_change_android")

    (
        WorkflowBuilder()
        # Input: Wikipedia-based dataset of Android forks on GitHub
        .input(
            Loader(
                Metadata.of_string("id")  # GitHub repo id / URL
            )
        )
        # --- Add & filter: customized Android framework ---
        .add_metadata(Loader(url, customized_android_framework))
        .filter_operator("customized_android_framework ")
        # --- Add & filter: source code availability ---
        .add_metadata(Loader(url, source_code_available))
        .filter_operator("source_code_available")
        # --- Add & filter: version control system ---
        .add_metadata(Loader(url, use_vcs))
        .filter_operator("use_vcs")
        # --- Add & filter: discontinued projects ---
        .add_metadata(Loader(url, is_discontinued))
        .filter_operator("is_discontinued")
        # --- Add & filter: number of Android merge changes ---
        .add_metadata(Loader(url, number_of_merge_change_android))
        .filter_operator("number_of_merge_change_android > 1")
    )
