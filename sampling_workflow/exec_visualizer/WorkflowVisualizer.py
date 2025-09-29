import os
from typing import cast

from graphviz import Digraph

from sampling_workflow.constraint.BoolConstraintString import BoolConstraintString
from sampling_workflow.operator.clustering.GroupingOperator import GroupingOperator
from sampling_workflow.operator.selection.filter.FilterOperator import FilterOperator


class WorkflowVisualizer:
    def __init__(self, workflow):
        self.workflow = workflow
        self.output_dir = os.path.dirname(__file__)

    def generate_graph(self, output_file: str = "workflow_graph"):
        svg_path = os.path.join(self.output_dir, output_file)
        dot = Digraph(format="svg")
        dot.attr(rankdir="LR")

        # Add input node
        dot.node(
            "InputSet",
            label=f"INPUT SET\nSize : {self.workflow.get_workflow_input().flatten_set().size()}",
            shape="box",
        )

        # Traverse and draw the workflow
        last_nodes = self._add_nodes_and_edges(
            dot, self.workflow, parent_names=["InputSet"]
        )

        # Add output node
        output_set = self.workflow.get_workflow_output().flatten_set()
        output_size = output_set.size()
        dot.node("OutputSet", label=f"SAMPLE\nSize : {output_size}", shape="box")

        # Link last operator(s) to output
        for node in last_nodes:
            dot.edge(node, "OutputSet")

        # Render
        dot.render(svg_path, format="svg", cleanup=True)
        print(f"Workflow graph saved to {svg_path}")

        # HTML wrapper
        self.create_html_page(svg_path)

    def _add_nodes_and_edges(
        self,
        dot,
        workflow,
        level: int = 0,
        workflow_number: int = 0,
        op_number: int = 0,
        parent_names=None,
    ) -> list[str]:
        if parent_names is None:
            parent_names = []

        op = workflow.get_root()
        last_nodes = []

        while op is not None:
            output_set = op.get_output()
            node_name = f"{op.__class__.__name__}_{level}_{workflow_number}_{op_number}"

            # Label formatting
            if isinstance(op, FilterOperator) and isinstance(
                op.get_constraint(), BoolConstraintString
            ):
                constraint = cast(
                    "BoolConstraintString", op.get_constraint()
                ).get_string_constraint()
                label = f"Filter Operator\n{constraint}\nSize : {output_set.flatten_set().size()}"
            elif isinstance(op, GroupingOperator):
                label = "Grouping\nOperator"
            else:
                label = f"{op.__class__.__name__.replace('Operator', '')}\nOperator\nSize : {output_set.flatten_set().size()}"

            dot.node(node_name, label=label, shape="box")

            # Link all incoming parent nodes
            for parent in parent_names:
                dot.edge(parent, node_name)

            # Handle grouping
            if isinstance(op, GroupingOperator):
                sub_last_nodes = []
                for i, sub_workflow in enumerate(op.get_workflows()):
                    sub_nodes = self._add_nodes_and_edges(
                        dot,
                        sub_workflow,
                        level=level + 1,
                        workflow_number=i,
                        op_number=0,
                        parent_names=[node_name],
                    )
                    sub_last_nodes.extend(sub_nodes)

                parent_names = (
                    sub_last_nodes  # They become the parents of the next operator
                )
                last_nodes = sub_last_nodes
            else:
                parent_names = [node_name]
                last_nodes = [node_name]

            op = op.get_next_operator()
            op_number += 1

        return last_nodes

    def create_html_page(self, svg_file: str, output_html: str = "workflow.html"):
        html_path = os.path.join(self.output_dir, output_html)

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Workflow Visualization</title>
        </head>
        <body>
            <h1>Workflow Visualization</h1>
            <div>
                <embed src="{os.path.basename(svg_file)}.svg" type="image/svg+xml" style="width:100%; height:90vh;"></embed>
            </div>
        </body>
        </html>
        """
        with open(html_path, "w") as f:
            f.write(html_content)
        print(f"HTML page saved to {html_path}")
