# perturbations.py
# This module will contain functions for different fault injection strategies.

import random
from pyverilog.vparser.ast import Node, Unot, Rvalue, IntConst, Assign
from pyverilog.dataflow.visit import NodeVisitor

class Perturber(NodeVisitor):
    def __init__(self, config=None):
        self.config = config

    def apply(self, ast):
        self.visit(ast)

class AssignmentFlipper(Perturber):
    """
    Flip the RHS of every Assign by applying Unot to the inner term of Rvalue,
    """
    def __init__(self, config=None):
        super().__init__(config)
        
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

class LogicInverter(Perturber):
    """
    Invert conditions in IfStatement nodes by wrapping them in Unot.
    """
    def __init__(self, config=None):
        super().__init__(config)

    def visit_IfStatement(self, node):
        cond = node.cond
        if not isinstance(cond, Unot):
            node.cond = Unot(cond)
        self.generic_visit(node)

class ConstChanger(Perturber):
    """
    Flip single-bit constants, invert all bits for multi-bit constants.
    """

    def __init__(self, config=None):
        super().__init__(config)

    def visit_IntConst(self, node):
        # Flip single-bit constants, invert all bits for multi-bit
        value_str = node.value
        # Handle binary, hex, decimal, etc.
        if "'" in value_str:
            width, baseval = value_str.split("'")
            base = baseval[0].lower()
            val = baseval[1:]
            if base == 'b':
                # Invert all bits
                flipped = ''.join('1' if c == '0' else '0' for c in val)
                node.value = f"{width}'b{flipped}"
            elif base == 'h':
                # Invert hex by flipping all bits
                nbits = int(width)
                intval = int(val, 16)
                mask = (1 << nbits) - 1
                flipped = hex(intval ^ mask)[2:]
                node.value = f"{width}'h{flipped}"
            elif base == 'd':
                nbits = int(width)
                intval = int(val, 10)
                mask = (1 << nbits) - 1
                flipped = str(intval ^ mask)
                node.value = f"{width}'d{flipped}"
            else:
                # Unknown base, skip
                pass
        else:
            # No width/base, treat as decimal and flip 0/1
            if value_str == "0":
                node.value = "1"
            elif value_str == "1":
                node.value = "0"
            else:
                # For other values, invert all bits
                intval = int(value_str)
                nbits = intval.bit_length()
                mask = (1 << nbits) - 1
                node.value = str(intval ^ mask)

class AssignmentRandomizer(Perturber):
    """
    Randomly change the RHS of assignments to random constants (0 or 1).
    """
    def __init__(self, config=None):
        super().__init__(config)

    def visit_Assign(self, node):
        # With 50% probability, replace RHS with a random constant (0 or 1)
        if random.random() < 0.5:
            rand_val = str(random.randint(0, 1))
            if isinstance(node.right, Rvalue):
                node.right.var = IntConst(rand_val)
            else:
                node.right = IntConst(rand_val)
        self.generic_visit(node)
