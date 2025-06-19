from bidouille.test.Workflow import Workflow

if __name__ == "__main__":
    workflow = Workflow().sample_operator(cardinality = 2).filter_operator().filter_operator()
    workflow.display()