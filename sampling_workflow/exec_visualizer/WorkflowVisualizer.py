import os
from typing import cast

from graphviz import Digraph

from sampling_workflow.constraint.BoolConstraintString import BoolConstraintString
from sampling_workflow.operator.clustering.GroupingOperator import GroupingOperator
from sampling_workflow.operator.selection.filter.FilterOperator import FilterOperator


class WorkflowVisualizer:
    def __init__(self, workflow):
        self.workflow = workflow
        self.output_dir = os.path.dirname(__file__)  # Path to the exec_visualizer directory
        self.last_nodes = []

    def generate_graph(self, output_file: str = "workflow_graph"):
        # Full path for the SVG file
        svg_path = os.path.join(self.output_dir, f"{output_file}")

        dot = Digraph(format="svg")
        dot.attr(rankdir="LR")  # Left-to-right layout

        # Traverse the workflow and add nodes/edges
        self._add_nodes_and_edges(dot, self.workflow)

        # Save the graph to an SVG file
        dot.render(svg_path, format="svg", cleanup=True)
        print(f"Workflow graph saved to {svg_path}")

        # Create the HTML page in the same directory
        self.create_html_page(svg_path)

    def _add_nodes_and_edges(self, dot, workflow, level:int=0, workflow_number:int=0, op_number:int=0, parent_name=None):
        op = workflow.get_root()

        if(not parent_name):
            dot.node("InputSet", label=f"INPUT SET\nSize: {workflow.get_workflow_input().size()}", shape="box")
            parent_name = "InputSet"


        dot.node("OutputSet", label=f"OUTPUT SET\nSize: {workflow.get_workflow_output().size()}", shape="box")

        to_attach = []
        while op is not None:
            output_set = op.get_output()

            # Add the current operator as a node
            node_name = f"{op.__class__.__name__}_{level}_{workflow_number}_{op_number}"
            label = f"{op.__class__.__name__}\nSize: {output_set.size()}"

            if isinstance(op, FilterOperator) and isinstance(op.get_constraint(), BoolConstraintString):
                constraint = cast(BoolConstraintString, op.get_constraint()).get_string_constraint()
                label = f"{constraint}\nSize: {output_set.size()}"

            dot.node(node_name, label=label, shape="box")

            for node in self.last_nodes:
                dot.edge(node, node_name)

            # Add an edge from the previous node to the current node
            if parent_name:
                dot.edge(parent_name, node_name)

            if isinstance(op, GroupingOperator):
                # If it's a GroupingOperator, recursively add its sub-workflows
                workflow_number = 0
                for sub_workflow in op.get_workflows():
                    self._add_nodes_and_edges(dot, sub_workflow, level+1, workflow_number, op_number, node_name)
                    workflow_number += 1

            op_number += 1
            # Move to the next operator
            parent_name = node_name
            op = op.get_next_operator()

        last_op_name = f"{workflow.get_last_operator().__class__.__name__}_{level}_{workflow_number}_{op_number-1}"
        self.last_nodes.append(last_op_name)

        for end in self.last_nodes:
            dot.edge(end, "OutputSet")


    def create_html_page(self, svg_file: str, output_html: str = "workflow.html"):
        # Full path for the HTML file
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