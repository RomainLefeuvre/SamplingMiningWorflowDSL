import ast


def get_variable_names(code_str):
    tree = ast.parse(code_str)
    variable_names = set()

    class VariableVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):  # Variable being assigned
                variable_names.add(node.id)
            self.generic_visit(node)

        def visit_arg(self, node):  # Function arguments
            variable_names.add(node.arg)

        def visit_FunctionDef(self, node):  # Also visit function arguments
            for arg in node.args.args:
                variable_names.add(arg.arg)
            self.generic_visit(node)

        def visit_For(self, node):  # For loop target
            self.visit(node.target)
            self.generic_visit(node)

    VariableVisitor().visit(tree)
    return variable_names


def setup_logging(log_file="app.log", level="DEBUG"):
    import logging

    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename=log_file,
        filemode="a",  # Append to file (use "w" to overwrite each run)
    )