# inject.py
# Main entry point for the fault injection tool.
# 
# Author: Adwait Godbole (adwait@berkeley.edu)

import argparse
from pyverilog.vparser.parser import parse
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator

from config import FaultInjConfig
from perturbations import *

def fault_inject(input_files, config: FaultInjConfig) -> str:
    """
    Main fault injection function.
    Parses the input Verilog file, applies perturbations based on the config,
    and writes the perturbed Verilog to the output file.
    """
    ast, _ = parse(input_files)
    
    # Apply perturbations based on config
    if config.flip_assigns:
        print("Applying assignment_flipping perturbation...")
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

    codegenerator = ASTCodeGenerator()
    # Generate Verilog code from AST
    return codegenerator.visit(ast)


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
    parser.add_argument("--show-diff", "-s", action="store_true", help="Show diff between original and perturbed Verilog")
    args = parser.parse_args()

    # Load config
    config = FaultInjConfig.from_json_file(args.config)
    if args.seed is not None:
        config.seed = args.seed

    print("Loaded config:")
    print(config.model_dump_json(indent=2))

    codegenerator = ASTCodeGenerator()
    original_verilog = None
    if args.show_diff:
        ast, _ = parse([args.input])
        original_verilog = codegenerator.visit(ast)

    # Apply perturbations
    perturbed_verilog = fault_inject([args.input], config)

    with open(args.output, "w") as f:
        f.write(perturbed_verilog)

    if args.show_diff and original_verilog is not None:
        import difflib
        diff = difflib.unified_diff(
            original_verilog.splitlines(keepends=True),
            perturbed_verilog.splitlines(keepends=True),
            fromfile='original.v',
            tofile='perturbed.v'
        )
        with open("diff.txt", "w") as df:
            df.writelines(diff)
        print("Diff written to diff.txt")

    print(f"Perturbed Verilog written to {args.output}")

if __name__ == "__main__":
    main()
