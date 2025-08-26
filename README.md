# Verilog Fault Injection

A configurable fault-injection module for Verilog designs. It perturbs a given Verilog `.v` file using various (`pyverilog`) AST transformation strategies.

## Usage

To run the tool on an example Verilog file:
```bash
python inject.py -i examples/fifo.v -o examples/fifo_perturbed.v --config examples/config.json
```

## Operation

**Strategies:** The following strategies are implemented and can be enabled or disabled via the configuration file (`config.py`).

- Signal Flipping: Inverts the right-hand side of assignment statements.
- Logic Inversion: Inverts conditions in if-statements within always blocks.
- Constant Mutation: Flips or inverts constant values (binary, hex, decimal).
- Assignment Randomization: Randomly replaces assignment right-hand sides with random constants.

**Configuration:** The tool uses a Pydantic `BaseModel` config to enable/disable:
- `flip_signals`: Invert assignment right-hand sides.
- `invert_logic`: Invert if-statement conditions.
- `change_constants`: Flip/invert constants.
- `randomize_assignments`: Randomize assignment right-hand sides.
- `seed`: Random seed for reproducibility.

Example config (`examples/config.json`):
```json
{
  "flip_signals": true,
  "invert_logic": true,
  "change_constants": true,
  "randomize_assignments": false,
  "seed": 42
}
```


**Dependencies:**

- [pyverilog](https://github.com/PyHDI/Pyverilog)
- [pydantic](https://pydantic-docs.helpmanual.io/)


## License

See the source files for license and copyright.
