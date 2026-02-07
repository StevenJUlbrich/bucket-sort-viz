"""Tier 1: Preset configuration and bucket range validation (no Pygame)."""

from bucket_sort_viz.presets import DEFAULT_PRESET, PRESETS


class TestPresetValidation:
    """Verify all presets have correct bucket coverage."""

    def test_all_presets_validate(self):
        for name, preset in PRESETS.items():
            assert preset.validate(), f"Preset '{name}' failed validation"

    def test_small_preset_coverage(self):
        preset = PRESETS["small"]
        assert preset.value_range == (0, 99)
        assert preset.num_buckets == 4
        assert preset.bucket_size == 25
        assert preset.num_buckets * preset.bucket_size == 100

    def test_medium_preset_coverage(self):
        preset = PRESETS["medium"]
        assert preset.value_range == (0, 199)
        assert preset.num_buckets == 8
        assert preset.bucket_size == 25
        assert preset.num_buckets * preset.bucket_size == 200

    def test_large_preset_coverage(self):
        preset = PRESETS["large"]
        assert preset.value_range == (0, 999)
        assert preset.num_buckets == 10
        assert preset.bucket_size == 100
        assert preset.num_buckets * preset.bucket_size == 1000


class TestBucketRanges:
    """Verify generate_bucket_ranges produces correct, gapless ranges."""

    def test_small_ranges(self):
        ranges = PRESETS["small"].generate_bucket_ranges()
        assert len(ranges) == 4
        assert ranges[0] == (0, 24)
        assert ranges[1] == (25, 49)
        assert ranges[2] == (50, 74)
        assert ranges[3] == (75, 99)

    def test_medium_ranges(self):
        ranges = PRESETS["medium"].generate_bucket_ranges()
        assert len(ranges) == 8
        assert ranges[0] == (0, 24)
        assert ranges[-1] == (175, 199)

    def test_large_ranges(self):
        ranges = PRESETS["large"].generate_bucket_ranges()
        assert len(ranges) == 10
        assert ranges[0] == (0, 99)
        assert ranges[-1] == (900, 999)

    def test_no_gaps_in_ranges(self):
        """Each range's high + 1 should equal the next range's low."""
        for name, preset in PRESETS.items():
            ranges = preset.generate_bucket_ranges()
            for i in range(len(ranges) - 1):
                assert ranges[i][1] + 1 == ranges[i + 1][0], (
                    f"Gap between range {i} and {i + 1} in preset '{name}'"
                )

    def test_ranges_cover_full_value_range(self):
        """First range starts at value_range[0], last ends at value_range[1]."""
        for name, preset in PRESETS.items():
            ranges = preset.generate_bucket_ranges()
            assert ranges[0][0] == preset.value_range[0], (
                f"Preset '{name}' ranges don't start at {preset.value_range[0]}"
            )
            assert ranges[-1][1] == preset.value_range[1], (
                f"Preset '{name}' ranges don't end at {preset.value_range[1]}"
            )


class TestPresetDefaults:
    """Verify default preset configuration."""

    def test_default_preset_exists(self):
        assert DEFAULT_PRESET in PRESETS

    def test_all_presets_have_required_fields(self):
        for name, preset in PRESETS.items():
            assert preset.name == name
            assert len(preset.label) > 0
            assert preset.value_range[0] < preset.value_range[1]
            assert preset.num_buckets > 0
            assert preset.bucket_size > 0
            assert preset.circle_radius > 0
            assert len(preset.description) > 0

    def test_presets_are_frozen(self):
        """Presets should be immutable."""
        preset = PRESETS["small"]
        try:
            preset.name = "modified"
            assert False, "Should have raised FrozenInstanceError"
        except AttributeError:
            pass  # Expected — frozen dataclass
