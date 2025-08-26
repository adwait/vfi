# Fault Injection Module for Verilog

This Python package provides a configurable fault-injection tool for Verilog designs. It can perturb a given Verilog `.v` file using various strategies, controlled by a Pydantic-based configuration.

## Structure

- `inject.py`: Main entry point (CLI/API) for running fault injection.
- `config.py`: Defines the Pydantic `FaultInjConfig` for enabling/disabling perturbations and setting the random seed.
- `perturbations.py`: Contains functions for different fault injection strategies.
- `__init__.py`: Package initialization.

## Configuration

The tool uses a Pydantic `BaseModel` config to enable/disable:
- Signal flipping
- Logic inversion
- Constant changes
- Assignment randomization
- Random seed for reproducibility

## Usage

To be implemented: CLI and API usage instructions.

## Dependencies

- [pydantic](https://pydantic-docs.helpmanual.io/)
- [pyverilog](https://github.com/PyHDI/Pyverilog) (planned for AST manipulation)
