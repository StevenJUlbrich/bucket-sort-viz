"""Bucket Sort algorithm engine with step recording.

Generates random values within a preset's range, sorts them using
bucket sort with insertion sort per bucket, and records every logical
step for the animator to replay.
"""

import random

from bucket_sort_viz.config import STEP_TO_CODE_LINE
from bucket_sort_viz.model.step import Step
from bucket_sort_viz.presets import SortPreset


def bucket_sort(
    preset: SortPreset,
    count: int,
    seed: int | None = None,
) -> tuple[list[int], list[int], list[Step]]:
    """Run bucket sort and record all steps.

    Args:
        preset: The sort preset defining range, bucket count, etc.
        count: Number of elements to generate and sort.
        seed: Optional random seed for reproducibility.

    Returns:
        A tuple of (original_values, sorted_values, steps).
    """
    rng = random.Random(seed)
    values = [rng.randint(preset.value_range[0], preset.value_range[1]) for _ in range(count)]
    original_values = list(values)

    steps: list[Step] = []
    bucket_ranges = preset.generate_bucket_ranges()

    # Build element_id -> value mapping (stable IDs = original list indices)
    # Each element_id is its index in the original unsorted list.
    buckets: list[list[int]] = [[] for _ in range(preset.num_buckets)]

    # ── Phase: Scatter ──────────────────────────────────
    steps.append(Step(
        step_type="phase_change",
        phase="scatter",
        element_ids=[],
        code_line=STEP_TO_CODE_LINE["phase_change"],
        description="Begin scatter phase",
    ))

    for element_id in range(count):
        value = original_values[element_id]
        bucket_idx = _find_bucket(value, bucket_ranges)
        slot = len(buckets[bucket_idx])
        buckets[bucket_idx].append(element_id)

        steps.append(Step(
            step_type="scatter",
            phase="scatter",
            element_ids=[element_id],
            bucket_index=bucket_idx,
            slot_index=slot,
            code_line=STEP_TO_CODE_LINE["scatter"],
            description=f"Scatter element {element_id} (value={value}) into bucket {bucket_idx}",
        ))

    # ── Phase: Sort Buckets (insertion sort) ────────────
    steps.append(Step(
        step_type="phase_change",
        phase="sort",
        element_ids=[],
        code_line=STEP_TO_CODE_LINE["phase_change"],
        description="Begin sort phase",
    ))

    for bucket_idx, bucket in enumerate(buckets):
        if len(bucket) <= 1:
            continue
        _insertion_sort_bucket(
            bucket, bucket_idx, original_values, steps,
        )

    # ── Phase: Gather ───────────────────────────────────
    steps.append(Step(
        step_type="phase_change",
        phase="gather",
        element_ids=[],
        code_line=STEP_TO_CODE_LINE["phase_change"],
        description="Begin gather phase",
    ))

    output_idx = 0
    for bucket_idx, bucket in enumerate(buckets):
        for element_id in bucket:
            steps.append(Step(
                step_type="gather",
                phase="gather",
                element_ids=[element_id],
                bucket_index=bucket_idx,
                output_index=output_idx,
                code_line=STEP_TO_CODE_LINE["gather"],
                description=(
                    f"Gather element {element_id} "
                    f"(value={original_values[element_id]}) to output[{output_idx}]"
                ),
            ))
            output_idx += 1

    # ── Celebration ─────────────────────────────────────
    all_ids = []
    for bucket in buckets:
        all_ids.extend(bucket)

    steps.append(Step(
        step_type="celebration",
        phase="done",
        element_ids=all_ids,
        code_line=STEP_TO_CODE_LINE["celebration"],
        description="Sorting complete!",
    ))

    sorted_values = [original_values[eid] for eid in all_ids]
    return original_values, sorted_values, steps


def _find_bucket(value: int, bucket_ranges: list[tuple[int, int]]) -> int:
    """Find which bucket a value belongs to."""
    for i, (low, high) in enumerate(bucket_ranges):
        if low <= value <= high:
            return i
    raise ValueError(f"Value {value} does not fit in any bucket range: {bucket_ranges}")


def _insertion_sort_bucket(
    bucket: list[int],
    bucket_idx: int,
    original_values: list[int],
    steps: list[Step],
) -> None:
    """Sort a bucket in-place using insertion sort, recording steps."""
    for i in range(1, len(bucket)):
        j = i
        while j > 0:
            eid_j = bucket[j]
            eid_j_minus_1 = bucket[j - 1]
            val_j = original_values[eid_j]
            val_j_minus_1 = original_values[eid_j_minus_1]

            # Record comparison
            steps.append(Step(
                step_type="compare",
                phase="sort",
                element_ids=[eid_j_minus_1, eid_j],
                bucket_index=bucket_idx,
                code_line=STEP_TO_CODE_LINE["compare"],
                description=(
                    f"Compare elements {eid_j_minus_1} (val={val_j_minus_1}) "
                    f"and {eid_j} (val={val_j}) in bucket {bucket_idx}"
                ),
            ))

            if val_j_minus_1 > val_j:
                # Swap needed
                bucket[j], bucket[j - 1] = bucket[j - 1], bucket[j]
                steps.append(Step(
                    step_type="swap",
                    phase="sort",
                    element_ids=[eid_j_minus_1, eid_j],
                    bucket_index=bucket_idx,
                    slot_index=j - 1,
                    code_line=STEP_TO_CODE_LINE["swap"],
                    description=(
                        f"Swap elements {eid_j_minus_1} (val={val_j_minus_1}) "
                        f"and {eid_j} (val={val_j}) in bucket {bucket_idx}"
                    ),
                ))
                j -= 1
            else:
                # No swap needed — element is in correct position
                steps.append(Step(
                    step_type="no_swap",
                    phase="sort",
                    element_ids=[eid_j_minus_1, eid_j],
                    bucket_index=bucket_idx,
                    slot_index=j,
                    code_line=STEP_TO_CODE_LINE["no_swap"],
                    description=(
                        f"No swap needed: {eid_j_minus_1} (val={val_j_minus_1}) "
                        f"<= {eid_j} (val={val_j}) in bucket {bucket_idx}"
                    ),
                ))
                break
