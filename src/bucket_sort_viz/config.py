"""Central configuration for Bucket Sort Visualizer.

Brick 1 subset: element counts and pseudocode mapping.
Screen, color, font, and timing constants will be added in later bricks.
"""

from bucket_sort_viz.model.step import StepType

# ──────────────────────────────────────────────
# Element count
# ──────────────────────────────────────────────
ELEMENT_COUNT_MIN = 10
ELEMENT_COUNT_MAX = 15
ELEMENT_COUNT_DEFAULT = 10

# ──────────────────────────────────────────────
# Pseudocode lines displayed in the code panel
# ──────────────────────────────────────────────
PSEUDOCODE_LINES: list[str] = [
    "# 1. Scatter into Buckets",      # 0 — comment
    "for x in input:",                 # 1 — keyword
    "    idx = (x - min) // size",     # 2 — code
    "    buckets[idx].append(x)",      # 3 — code (scatter highlight)
    "# 2. Sort Buckets",              # 4 — comment
    "for b in buckets:",               # 5 — keyword
    "    insertionSort(b)",            # 6 — code (sort highlight)
    "# 3. Gather",                     # 7 — comment
    "output = []",                     # 8 — code
    "for b in buckets:",               # 9 — keyword
    "    output.extend(b)",            # 10 — code (gather highlight)
]

STEP_TO_CODE_LINE: dict[StepType, int] = {
    "scatter": 3,       # buckets[idx].append(x)
    "compare": 6,       # insertionSort(b)
    "swap": 6,          # insertionSort(b)
    "no_swap": 6,       # insertionSort(b)
    "gather": 10,       # output.extend(b)
    "phase_change": -1,  # No highlight during transitions
    "celebration": -1,   # No highlight during celebration
}
