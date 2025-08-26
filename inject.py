# inject.py
# Main entry point for the fault injection tool.
# 
# Author: Adwait Godbole (adwait@berkeley.edu)

import argparse
from pyverilog.vparser.parser import parse
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator

from config import FaultInjConfig
from perturbations import *
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
    args = parser.parse_args()

    # Load config
    config = FaultInjConfig.from_json_file(args.config)
    if args.seed is not None:
        config.seed = args.seed

    print("Loaded config:")
    print(config.model_dump_json(indent=2))

    ast, directives = parse([args.input])
    print("Parsed Verilog AST.")

    codegenerator = ASTCodeGenerator()
    original_verilog = codegenerator.visit(ast)
    with open(f"orig.{args.output}", "w") as f:
        f.write(original_verilog)

    # Apply perturbations
    if config.flip_signals:
        print("Applying signal flipping perturbation...")
        flipper = AssignmentFlipper(config=config)
        flipper.apply(ast)
    if config.invert_logic:
        print("Applying invert_logic perturbation...")
        inverter = LogicInverter(config=config)
        inverter.apply(ast)
    if config.change_constants:
        print("Applying change_constants perturbation...")
        changer = ConstChanger(config=config)
        changer.apply(ast)
    if config.randomize_assignments:
        print("Applying randomize_assignments perturbation...")
        randomizer = AssignmentRandomizer(config=config)
        randomizer.apply(ast)

    # Generate Verilog code from AST
    verilog_code = codegenerator.visit(ast)
    with open(args.output, "w") as f:
        f.write(verilog_code)
    print(f"Perturbed Verilog written to {args.output}")

if __name__ == "__main__":
    main()
