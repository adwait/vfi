def print_ast(node, indent=0, max_depth=5):
    """
    Recursively print the pyverilog AST structure for exploration.
    """
    if indent > max_depth:
        print(" " * (2 * indent) + "...")
        return
    node_type = type(node).__name__
    print(" " * (2 * indent) + f"{node_type}", end="")
    # Print key fields for leaf nodes
    if hasattr(node, 'name'):
        print(f" (name={getattr(node, 'name', None)})", end="")
    if hasattr(node, 'value'):
        print(f" (value={getattr(node, 'value', None)})", end="")
    print()
    # Recurse into children
    if hasattr(node, 'children'):
        for child in node.children():
            print_ast(child, indent + 1, max_depth)
