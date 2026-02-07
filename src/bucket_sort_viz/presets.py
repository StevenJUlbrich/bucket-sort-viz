"""Preset definitions for Small, Medium, and Large bucket sort configurations."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SortPreset:
    name: str
    label: str
    value_range: tuple[int, int]     # (min, max) inclusive
    num_buckets: int
    bucket_size: int                  # range width per bucket
    circle_radius: int
    description: str

    def generate_bucket_ranges(self) -> list[tuple[int, int]]:
        """Generate (low, high) range tuples for each bucket."""
        ranges = []
        for i in range(self.num_buckets):
            low = self.value_range[0] + i * self.bucket_size
            high = low + self.bucket_size - 1
            ranges.append((low, high))
        return ranges

    def validate(self) -> bool:
        """Verify bucket ranges fully cover the value range with no gaps."""
        total_coverage = self.num_buckets * self.bucket_size
        value_span = self.value_range[1] - self.value_range[0] + 1
        return total_coverage == value_span


PRESETS: dict[str, SortPreset] = {
    "small": SortPreset(
        name="small",
        label="Small (0\u201399)",
        value_range=(0, 99),
        num_buckets=4,
        bucket_size=25,               # 0-24, 25-49, 50-74, 75-99
        circle_radius=22,
        description="Classic 4-bucket sort. Great for understanding the basics.",
    ),
    "medium": SortPreset(
        name="medium",
        label="Medium (0\u2013199)",
        value_range=(0, 199),
        num_buckets=8,
        bucket_size=25,               # 0-24, 25-49, ... 175-199
        circle_radius=18,
        description="Wider range with 8 buckets. Shows how bucket count scales.",
    ),
    "large": SortPreset(
        name="large",
        label="Large (0\u2013999)",
        value_range=(0, 999),
        num_buckets=10,
        bucket_size=100,              # 0-99, 100-199, ... 900-999
        circle_radius=15,
        description="Big range, 10 buckets. Demonstrates real-world distribution.",
    ),
}

DEFAULT_PRESET = "small"
