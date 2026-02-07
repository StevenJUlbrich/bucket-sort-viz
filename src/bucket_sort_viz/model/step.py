"""Step dataclass — layout-agnostic with stable element IDs.

The algorithm engine records logical moves only. No pixel coordinates.
The Animator computes pixel positions at tween creation time based on
current layout state. This preserves clean MVC separation.

Element IDs are the index in the original unsorted list (stable, unique).
This avoids ambiguity when duplicate values exist (e.g., two 42s).
"""

from dataclasses import dataclass
from typing import Literal

StepType = Literal[
    "scatter",       # Element moves from input row to bucket
    "compare",       # Two elements highlighted for comparison (sort phase)
    "swap",          # Two elements swap positions within a bucket
    "no_swap",       # Comparison made, no swap needed (element stays)
    "gather",        # Element moves from bucket to output row
    "phase_change",  # Transition marker between phases
    "celebration",   # Final sorted state trigger
]

PhaseName = Literal["ready", "scatter", "sort", "gather", "done"]


@dataclass
class Step:
    step_type: StepType
    phase: PhaseName
    element_ids: list[int]            # Stable IDs (index in original unsorted list)
    bucket_index: int = -1            # Target bucket (-1 if N/A)
    slot_index: int = -1              # Position within bucket stack (-1 if N/A)
    output_index: int = -1            # Position in final output row (-1 if N/A)
    code_line: int = -1               # Pseudocode line to highlight
    description: str = ""             # Human-readable debug note
