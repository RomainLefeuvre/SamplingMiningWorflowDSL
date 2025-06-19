from bidouille.test.Workflow import Workflow

if __name__ == "__main__":
    workflow = Workflow().filterOperator().filterOperator().sampleOperator(cardinality = 2)
    workflow.display()