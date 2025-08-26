# perturbations.py
# This module will contain functions for different fault injection strategies.

from pyverilog.vparser.ast import Node, Unot, Rvalue
from pyverilog.dataflow.visit import NodeVisitor

class FaultInjector(NodeVisitor):
    def __init__(self, config=None):
        self.config = config

    def visit_Assign(self, node):
        """
        Flip the RHS of every Assign by applying Unot to the inner term of Rvalue, unless already Unot.
        """
        rhs = node.right
        # If right is an Rvalue, apply Unot to its .var field
        if isinstance(rhs, Rvalue):
            expr = rhs.var
            if not isinstance(expr, Unot):
                rhs.var = Unot(expr)
        # If right is not an Rvalue, fallback to previous logic
        elif not isinstance(rhs, Unot):
            node.right = Unot(rhs)
        # Continue walking into the left‐hand side (and any other children)
        self.visit(node.left)
        self.generic_visit(node)

    def generic_visit(self, node):
        """
        Override the base generic_visit to:
         - skip non-Node objects
         - descend into both single Node children and lists of Nodes
        """
        if not isinstance(node, Node):
            return

        for c in node.children():
            if isinstance(c, Node):
                self.visit(c)
            elif isinstance(c, list):
                for elem in c:
                    if isinstance(elem, Node):
                        self.visit(elem)

def invert_logic(ast, config):
    """Invert logic in always blocks in the AST."""
    pass  # To be implemented

def change_constants(ast, config):
    """Change constants in the AST."""
    pass  # To be implemented

def randomize_assignments(ast, config):
    """Randomize assignment targets or values in the AST."""
    pass  # To be implemented
