from pathlib import Path

from paper_extension.element.writter.CsvWriter import CsvWriter
from sampling_workflow.element.loader import JsonLoader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# How do Machine Learning Projects use Continuous Integration Practices? An Empirical Study on GitHub Actions.
# Step 1
# * Keep repos updated in 2023
# * Filter out repos with default branch different than ‘main’ or ‘master’
#
# Step 2
# * Filter out projects without at least one workflow config file (YAML file stored within the ‘.github/workflows/’ folder)
#
# Step 3
# * Keep projects with at least one active workflow (workflow name or filename should
# not contain any documentation-related words, workflow should be triggered by either a pull_request
# or push event, workflow configuration file must incorporate a CI-related word in either the job or step name)
# * Manually inspect 100 workflows
#
# Step 4
# * Keep repos with at least 100 runs for CI workflows
#
# Step 5
# * Keep repos with period between first and last run of the workflow being at least 6 months
#
# Step 6
# Sample to address the ML / non-ML imbalance
# * Sort by number of stars and take 150 first repos
# * Keep repos with more than 100 runs
# * Keep repos with more than 5 stars
# * Keep repos with forks
# * Keep repos with updates in 2023
# * Manually classify ML and non-ML repos
# * Apply steps 1 to 5
# * Mitigation of potential confounds with stratified sampling / -> not clear 'for example'
#
# * Combine with initial sample
# * Combine with Rzig et al dataset


def main():
    input_path_main = Path("github.json")

    default_branch = Metadata.of_string("default_branch")
    nb_workflow_config_files = Metadata.of_integer("nb_workflow_config_files")
    has_active_ci_workflow = Metadata.of_integer("has_active_ci_workflow")

    nb_runs_ci = Metadata.of_integer("nb_runs_ci")
    first_run_ci = Metadata.of_integer("first_run_ci")
    last_run_ci = Metadata.of_integer("last_run_ci")

    main_workflow = (
        WorkflowBuilder()
        .input(
            JsonLoader(
                input_path_main,
                default_branch,
                nb_workflow_config_files,
                has_active_ci_workflow,
                nb_runs_ci,
                first_run_ci,
                last_run_ci,
            )
        )
        .filter_operator("default_branch in ['main', 'master']")
        .filter_operator("nb_workflow_config_files > 0")
        .filter_operator("has_active_ci_workflow > 0")
        .manual_sampling_operator()
        .filter_operator("nb_runs_ci > 100")
        .filter_operator("last_run_ci - first_run_ci > 6")  # At least 6 months
        .output(CsvWriter("out_main.csv"))
    )

    input_path = Path("github.json")
    stars = Metadata.of_integer("stars")
    nb_runs = Metadata.of_integer("nb_runs")
    forks = Metadata.of_integer("forks")
    has_updates_in_2023 = Metadata.of_integer("has_updates_in_2023")
    url = Metadata.of_string("url")

    # Workflow for step 6
    w_step_6 = (
        WorkflowBuilder()
        .input(JsonLoader(input_path, url, stars, nb_runs, forks, has_updates_in_2023))
        .systematic_selection_operator(150, stars, 1)
        .filter_operator("nb_runs > 100")
        .filter_operator("stars > 5")
        .filter_operator("forks > 0")
        .filter_operator("has_updates_in_2023 > 2023")
        .manual_sampling_operator()
        # Steps 1 to 5
        .filter_operator("default_branch in ['main', 'master']")
        .filter_operator("nb_workflow_config_files > 0")
        .filter_operator("has_active_ci_workflow > 0")
        .manual_sampling_operator()
        .filter_operator("nb_runs_ci > 100")
        .filter_operator("last_run_ci - first_run_ci > 6")  # At least 6 months
        .output(CsvWriter("out.csv"))
    )

    main_workflow.execute_workflow()
    w_step_6.execute_workflow()

    # Combine with main workflow results
    # Combine with original dataset from Rzig et al.


if __name__ == "__main__":
    main()
