from src.analysis.WorkflowAnalysis import WorkflowAnalysis
from src.analysis.YamaneTest import YamaneTest


class YamaneWorkflowAnalysis(WorkflowAnalysis):
    def __init__(self, margin_of_error: float = 0.05):
        super().__init__()
        self.margin_of_error = margin_of_error

    def analyze(self, workflow):
        pop_size = workflow.get_workflow_input().size()
        yamane_test = YamaneTest(pop_size, self.margin_of_error)

        required_sample_size = yamane_test.calculate_required_sample_size()
        actual_sample_size = workflow.get_workflow_output().size()

        print("Yamane's Test Analysis:")
        print("Population Size (input size):", pop_size)
        print("Required Sample Size:", required_sample_size)
        print("Actual Sample Size:", actual_sample_size)

        if yamane_test.is_representative(actual_sample_size):
            print("The sample is representative based on Yamane's test.")
        else:
            print("The sample is not representative based on Yamane's test.")

        print("------------------------------------------")
