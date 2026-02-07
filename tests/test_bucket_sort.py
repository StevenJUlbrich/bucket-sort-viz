"""Tier 1: Algorithm correctness tests (no Pygame)."""

import pytest

from bucket_sort_viz.model.bucket_sort import bucket_sort
from bucket_sort_viz.presets import PRESETS


class TestSortingCorrectness:
    """Verify the algorithm produces correctly sorted output."""

    @pytest.mark.parametrize("preset_name", ["small", "medium", "large"])
    def test_sorted_output_matches_builtin(self, preset_name):
        """Sorted values should match Python's sorted()."""
        preset = PRESETS[preset_name]
        original, sorted_vals, _ = bucket_sort(preset, count=10, seed=42)
        assert sorted_vals == sorted(original)

    @pytest.mark.parametrize("preset_name", ["small", "medium", "large"])
    def test_sorted_output_with_max_elements(self, preset_name):
        """Works with maximum element count (15)."""
        preset = PRESETS[preset_name]
        original, sorted_vals, _ = bucket_sort(preset, count=15, seed=123)
        assert sorted_vals == sorted(original)

    @pytest.mark.parametrize("seed", [0, 1, 42, 100, 999])
    def test_sorted_with_various_seeds(self, seed):
        """Sorting is correct across different random seeds."""
        preset = PRESETS["small"]
        original, sorted_vals, _ = bucket_sort(preset, count=12, seed=seed)
        assert sorted_vals == sorted(original)


class TestValueGeneration:
    """Verify generated values match preset constraints."""

    @pytest.mark.parametrize("preset_name", ["small", "medium", "large"])
    def test_element_count(self, preset_name):
        """Generated value count matches requested count."""
        preset = PRESETS[preset_name]
        for count in [10, 12, 15]:
            original, sorted_vals, _ = bucket_sort(preset, count=count, seed=42)
            assert len(original) == count
            assert len(sorted_vals) == count

    @pytest.mark.parametrize("preset_name", ["small", "medium", "large"])
    def test_values_within_range(self, preset_name):
        """All generated values fall within the preset's value range."""
        preset = PRESETS[preset_name]
        original, _, _ = bucket_sort(preset, count=15, seed=42)
        for val in original:
            assert preset.value_range[0] <= val <= preset.value_range[1], (
                f"Value {val} outside range {preset.value_range}"
            )

    def test_values_are_integers(self):
        preset = PRESETS["small"]
        original, sorted_vals, _ = bucket_sort(preset, count=10, seed=42)
        for val in original:
            assert isinstance(val, int)
        for val in sorted_vals:
            assert isinstance(val, int)


class TestReproducibility:
    """Verify seed-based reproducibility."""

    def test_same_seed_produces_same_values(self):
        preset = PRESETS["small"]
        orig1, sorted1, steps1 = bucket_sort(preset, count=10, seed=42)
        orig2, sorted2, steps2 = bucket_sort(preset, count=10, seed=42)
        assert orig1 == orig2
        assert sorted1 == sorted2
        assert len(steps1) == len(steps2)

    def test_different_seeds_produce_different_values(self):
        preset = PRESETS["small"]
        orig1, _, _ = bucket_sort(preset, count=10, seed=42)
        orig2, _, _ = bucket_sort(preset, count=10, seed=99)
        assert orig1 != orig2

    def test_none_seed_still_sorts_correctly(self):
        preset = PRESETS["small"]
        original, sorted_vals, _ = bucket_sort(preset, count=10, seed=None)
        assert sorted_vals == sorted(original)


class TestSortedOutputPreservesAllValues:
    """Ensure no values are lost or duplicated during sorting."""

    @pytest.mark.parametrize("preset_name", ["small", "medium", "large"])
    def test_sorted_is_permutation_of_original(self, preset_name):
        preset = PRESETS[preset_name]
        original, sorted_vals, _ = bucket_sort(preset, count=15, seed=42)
        assert sorted(original) == sorted(sorted_vals)
