"""Main Pygame drawing engine — initializes window and orchestrates rendering."""

import pygame

from bucket_sort_viz.config import (
    BUCKET_GAP,
    BUCKET_HEIGHT,
    BUCKET_TOP_Y,
    COLORS,
    FPS,
    INPUT_ROW_Y,
    PANEL_HEIGHT,
    PANEL_TOP_Y,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SIDE_MARGIN,
    WINDOW_TITLE,
)
from bucket_sort_viz.presets import SortPreset
from bucket_sort_viz.view.code_panel import CodePanel
from bucket_sort_viz.view.elements import BucketRegion, CircleElement


class Renderer:
    """Manages the Pygame window and draws the bucket sort visualization.

    Args:
        preset: The sort preset defining bucket count, ranges, circle radius.
        values: The unsorted values to display (one per element).
    """

    def __init__(self, preset: SortPreset, values: list[int]):
        self.preset = preset
        self.values = values

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        # Build layout
        self.elements = self._create_elements()
        self.buckets = self._create_buckets()
        self.code_panel = CodePanel(0, PANEL_TOP_Y, SCREEN_WIDTH, PANEL_HEIGHT)

    def _create_elements(self) -> list[CircleElement]:
        """Create CircleElement instances positioned in the input row."""
        count = len(self.values)
        usable_width = SCREEN_WIDTH - 2 * SIDE_MARGIN
        spacing = usable_width / (count + 1)

        elements = []
        for i, value in enumerate(self.values):
            x = SIDE_MARGIN + spacing * (i + 1)
            elements.append(CircleElement(
                element_id=i,
                value=value,
                x=x,
                y=INPUT_ROW_Y,
                radius=self.preset.circle_radius,
            ))
        return elements

    def _create_buckets(self) -> list[BucketRegion]:
        """Create BucketRegion instances positioned across the screen."""
        num = self.preset.num_buckets
        usable_width = SCREEN_WIDTH - 2 * SIDE_MARGIN
        gap_total = BUCKET_GAP * (num - 1)
        bucket_width = (usable_width - gap_total) / num
        bucket_ranges = self.preset.generate_bucket_ranges()

        buckets = []
        for i, (low, high) in enumerate(bucket_ranges):
            x = SIDE_MARGIN + i * (bucket_width + BUCKET_GAP)
            label = f"{low}\u2013{high}"
            buckets.append(BucketRegion(
                bucket_index=i,
                x=x,
                y=BUCKET_TOP_Y,
                width=bucket_width,
                height=BUCKET_HEIGHT,
                label=label,
            ))
        return buckets

    def draw_ready_state(self, active_line: int = -1) -> None:
        """Draw the complete READY state frame."""
        # Background
        self.screen.fill(COLORS["bg_dark"])

        # Bucket regions
        for bucket in self.buckets:
            bucket.draw(self.screen)

        # Input row elements
        for element in self.elements:
            element.draw(self.screen)

        # Code panel
        self.code_panel.draw(self.screen, active_line=active_line)

        pygame.display.flip()

    def run_static(self) -> None:
        """Run a static display loop showing the READY state. ESC or close to exit."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.draw_ready_state()
            self.clock.tick(FPS)

        pygame.quit()
