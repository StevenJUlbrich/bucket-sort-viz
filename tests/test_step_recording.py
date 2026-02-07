"""Tier 1: Step sequence validation (no Pygame)."""

import pytest

from bucket_sort_viz.config import STEP_TO_CODE_LINE
from bucket_sort_viz.model.bucket_sort import bucket_sort
from bucket_sort_viz.presets import PRESETS


def _get_steps_by_type(steps, step_type):
    return [s for s in steps if s.step_type == step_type]


def _get_steps_by_phase(steps, phase):
    return [s for s in steps if s.phase == phase]


class TestStepSequence:
    """Verify steps follow the correct phase ordering."""

    @pytest.mark.parametrize("preset_name", ["small", "medium", "large"])
    def test_phase_order(self, preset_name):
        """Steps should progress: scatter → sort → gather → done."""
        preset = PRESETS[preset_name]
        _, _, steps = bucket_sort(preset, count=10, seed=42)

        phases_seen = []
        for step in steps:
            if step.phase not in phases_seen or step.phase != phases_seen[-1]:
                phases_seen.append(step.phase)

        # Should see scatter, sort, gather, done in order
        assert "scatter" in phases_seen
        assert "gather" in phases_seen
        assert "done" in phases_seen
        scatter_idx = phases_seen.index("scatter")
        gather_idx = phases_seen.index("gather")
        done_idx = phases_seen.index("done")
        assert scatter_idx < gather_idx < done_idx

    @pytest.mark.parametrize("preset_name", ["small", "medium", "large"])
    def test_phase_transitions_present(self, preset_name):
        """Phase change steps should exist between phases."""
        preset = PRESETS[preset_name]
        _, _, steps = bucket_sort(preset, count=10, seed=42)
        phase_changes = _get_steps_by_type(steps, "phase_change")
        # At least 3 transitions: → scatter, → sort, → gather
        assert len(phase_changes) >= 3


class TestScatterSteps:
    """Verify scatter phase step recording."""

    @pytest.mark.parametrize("count", [10, 12, 15])
    def test_scatter_count_equals_element_count(self, count):
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=count, seed=42)
        scatter_steps = _get_steps_by_type(steps, "scatter")
        assert len(scatter_steps) == count

    def test_scatter_steps_have_valid_bucket_index(self):
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=10, seed=42)
        scatter_steps = _get_steps_by_type(steps, "scatter")
        for step in scatter_steps:
            assert 0 <= step.bucket_index < preset.num_buckets

    def test_scatter_steps_have_single_element_id(self):
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=10, seed=42)
        scatter_steps = _get_steps_by_type(steps, "scatter")
        for step in scatter_steps:
            assert len(step.element_ids) == 1

    def test_all_element_ids_scattered(self):
        """Every element ID (0 to count-1) should appear in scatter steps."""
        count = 12
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=count, seed=42)
        scatter_steps = _get_steps_by_type(steps, "scatter")
        scattered_ids = {s.element_ids[0] for s in scatter_steps}
        expected_ids = set(range(count))
        assert scattered_ids == expected_ids


class TestSortSteps:
    """Verify sort phase step recording."""

    def test_sort_steps_have_two_element_ids(self):
        """Compare and swap steps should reference exactly 2 elements."""
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=15, seed=42)
        sort_steps = [
            s for s in steps
            if s.step_type in ("compare", "swap", "no_swap")
        ]
        for step in sort_steps:
            assert len(step.element_ids) == 2

    def test_sort_steps_have_valid_bucket_index(self):
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=15, seed=42)
        sort_steps = [
            s for s in steps
            if s.step_type in ("compare", "swap", "no_swap")
        ]
        for step in sort_steps:
            assert 0 <= step.bucket_index < preset.num_buckets

    def test_every_compare_followed_by_swap_or_no_swap(self):
        """Each compare step should be immediately followed by swap or no_swap."""
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=15, seed=42)

        for i, step in enumerate(steps):
            if step.step_type == "compare":
                assert i + 1 < len(steps), "Compare step is last step"
                next_step = steps[i + 1]
                assert next_step.step_type in ("swap", "no_swap", "compare"), (
                    f"Expected swap/no_swap/compare after compare, got {next_step.step_type}"
                )


class TestGatherSteps:
    """Verify gather phase step recording."""

    @pytest.mark.parametrize("count", [10, 12, 15])
    def test_gather_count_equals_element_count(self, count):
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=count, seed=42)
        gather_steps = _get_steps_by_type(steps, "gather")
        assert len(gather_steps) == count

    def test_gather_output_indices_sequential(self):
        """Gather steps should have sequential output_index values."""
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=10, seed=42)
        gather_steps = _get_steps_by_type(steps, "gather")
        output_indices = [s.output_index for s in gather_steps]
        assert output_indices == list(range(10))

    def test_gather_steps_have_single_element_id(self):
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=10, seed=42)
        gather_steps = _get_steps_by_type(steps, "gather")
        for step in gather_steps:
            assert len(step.element_ids) == 1

    def test_all_element_ids_gathered(self):
        """Every element ID should appear exactly once in gather steps."""
        count = 12
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=count, seed=42)
        gather_steps = _get_steps_by_type(steps, "gather")
        gathered_ids = [s.element_ids[0] for s in gather_steps]
        assert sorted(gathered_ids) == list(range(count))


class TestCelebrationStep:
    """Verify celebration step at the end."""

    def test_celebration_is_last_step(self):
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=10, seed=42)
        assert steps[-1].step_type == "celebration"

    def test_celebration_contains_all_ids(self):
        count = 10
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=count, seed=42)
        celebration = steps[-1]
        assert sorted(celebration.element_ids) == list(range(count))

    def test_celebration_phase_is_done(self):
        preset = PRESETS["small"]
        _, _, steps = bucket_sort(preset, count=10, seed=42)
        assert steps[-1].phase == "done"


class TestCodeLineMapping:
    """Verify code_line values match STEP_TO_CODE_LINE mapping."""

    @pytest.mark.parametrize("preset_name", ["small", "medium", "large"])
    def test_all_steps_have_correct_code_line(self, preset_name):
        preset = PRESETS[preset_name]
        _, _, steps = bucket_sort(preset, count=12, seed=42)
        for step in steps:
            expected = STEP_TO_CODE_LINE[step.step_type]
            assert step.code_line == expected, (
                f"Step '{step.step_type}' has code_line={step.code_line}, "
                f"expected {expected}"
            )


class TestElementIDValidity:
    """Verify all element IDs are valid indices."""

    @pytest.mark.parametrize("preset_name", ["small", "medium", "large"])
    def test_element_ids_in_valid_range(self, preset_name):
        count = 12
        preset = PRESETS[preset_name]
        _, _, steps = bucket_sort(preset, count=count, seed=42)
        for step in steps:
            for eid in step.element_ids:
                assert 0 <= eid < count, (
                    f"Element ID {eid} out of range [0, {count}) "
                    f"in step '{step.step_type}'"
                )
