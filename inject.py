# inject.py
# Main entry point for the fault injection tool.

import argparse
from config import FaultInjConfig
from perturbations import *
from pyverilog.vparser.parser import parse
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
from utils import print_ast

def main():
    """
    Main function for CLI/API.
    Handles argument parsing, config loading, and (future) perturbation orchestration.
    """
    parser = argparse.ArgumentParser(description="Fault Injection Tool for Verilog")
    parser.add_argument("--input", "-i", required=True, help="Input Verilog .v file")
    parser.add_argument("--output", "-o", required=False, help="Output perturbed Verilog .v file")
    parser.add_argument("--config", "-c", required=True, help="Path to config JSON file")
    parser.add_argument("--seed", type=int, default=None, help="Random seed (overrides config)")
    parser.add_argument("--print-ast", action="store_true", help="Print the AST structure of the input Verilog file and exit")
    args = parser.parse_args()

    # Load config
    config = FaultInjConfig.from_json_file(args.config)
    if args.seed is not None:
        config.seed = args.seed

    print("Loaded config:")
    print(config.model_dump_json(indent=2))

    ast, directives = parse([args.input])
    print("Parsed Verilog AST.")

    if args.print_ast:
        print("Printing AST structure (first 5 levels):")
        print_ast(ast)
        return

    # Apply perturbations
    if config.flip_signals:
        injector = FaultInjector(config=config)
        print("Applying signal flipping perturbation...")
        injector.visit(ast)

    # Generate Verilog code from AST
    codegen = ASTCodeGenerator()
    verilog_code = codegen.visit(ast)
    with open(args.output, "w") as f:
        f.write(verilog_code)
    print(f"Perturbed Verilog written to {args.output}")

if __name__ == "__main__":
    main()
