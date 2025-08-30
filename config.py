# config.py
# 
# Author: Adwait Godbole (adwait@berkeley.edu)

from pydantic import BaseModel, Field
from typing import Optional
import json

class FaultInjConfig(BaseModel):
    svm: bool = Field(default=False, description="Use SmartVerilog mutation module")
    flip_assigns: bool = Field(default=True, description="Flip signal assignments (e.g., assign x = y -> assign x = ~y)")
    invert_logic: bool = Field(default=True, description="Invert logic in always blocks (e.g., if (a) -> if (!a))")
    change_constants: bool = Field(default=True, description="Change constants (e.g., assign x = 1'b0 -> assign x = 1'b1)")
    randomize_assignments: bool = Field(default=False, description="Randomize assignment targets or values")
    seed: Optional[int] = Field(default=None, description="Random seed for reproducibility")

    @classmethod
    def from_json_file(cls, path: str):
        with open(path, "r") as f:
            data = json.load(f)
        return cls(**data)
