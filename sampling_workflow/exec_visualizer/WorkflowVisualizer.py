import os
from graphviz import Digraph

class WorkflowVisualizer:
    def __init__(self, workflow):
        self.workflow = workflow
        self.output_dir = os.path.dirname(__file__)  # Path to the exec_visualizer directory

    def generate_graph(self, output_file: str = "workflow_graph"):
        # Full path for the SVG file
        svg_path = os.path.join(self.output_dir, f"{output_file}")

        dot = Digraph(format="svg")
        dot.attr(rankdir="LR")  # Left-to-right layout

        # Traverse the workflow and add nodes/edges
        self._add_nodes_and_edges(dot, self.workflow, "Root")

        # Save the graph to an SVG file
        dot.render(svg_path, format="svg", cleanup=True)
        print(f"Workflow graph saved to {svg_path}")

        # Create the HTML page in the same directory
        self.create_html_page(svg_path)

    def _add_nodes_and_edges(self, dot, workflow, parent_name=None):
        op = workflow.get_root()
        parent_name = None  # No "Root" node

        while op is not None:
            output_set = op.get_output()

            # Add the current operator as a node
            node_name = f"{op.__class__.__name__}"
            dot.node(node_name, label=f"{op.__class__.__name__}\nSize: {output_set.size()}", shape="box")

            # Add an edge from the previous node to the current node
            if parent_name:
                dot.edge(parent_name, node_name)

            # Move to the next operator
            parent_name = node_name
            op = op.get_next_operator()

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