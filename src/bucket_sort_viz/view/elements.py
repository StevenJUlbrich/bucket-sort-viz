"""Drawable element classes: CircleElement and BucketRegion."""

import pygame

from bucket_sort_viz.config import COLORS, load_font


class CircleElement:
    """A single sortable element rendered as a circle with its value inside.

    Attributes:
        element_id: Stable ID (index in original unsorted list).
        value: The numeric value to display.
        x, y: Center position (mutable for animation).
        radius: Circle radius (from preset).
        color: Current fill color (RGB tuple).
    """

    def __init__(
        self,
        element_id: int,
        value: int,
        x: float,
        y: float,
        radius: int,
        color: tuple[int, int, int] | None = None,
    ):
        self.element_id = element_id
        self.value = value
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color or COLORS["element_default"]
        self._font: pygame.font.Font | None = None

    def _get_font(self) -> pygame.font.Font:
        if self._font is None:
            self._font = load_font("value")
        return self._font

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the circle and value text."""
        center = (int(self.x), int(self.y))

        # Filled circle
        pygame.draw.circle(surface, self.color, center, self.radius)

        # Value text centered inside
        font = self._get_font()
        text_surf = font.render(str(self.value), True, COLORS["text_bright"])
        text_rect = text_surf.get_rect(center=center)
        surface.blit(text_surf, text_rect)


class BucketRegion:
    """A bucket container rendered as an outlined rectangle with a range label.

    Attributes:
        bucket_index: Which bucket this is (0-based).
        x, y: Top-left corner position.
        width, height: Dimensions.
        label: Range label string (e.g., "0-24").
    """

    def __init__(
        self,
        bucket_index: int,
        x: float,
        y: float,
        width: float,
        height: float,
        label: str,
    ):
        self.bucket_index = bucket_index
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self._font: pygame.font.Font | None = None

    def _get_font(self) -> pygame.font.Font:
        if self._font is None:
            self._font = load_font("label")
        return self._font

    @property
    def center_x(self) -> float:
        """Horizontal center of the bucket."""
        return self.x + self.width / 2

    def draw(self, surface: pygame.Surface) -> None:
        """Draw bucket outline, fill, and range label."""
        rect = pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))

        # Filled background
        pygame.draw.rect(surface, COLORS["bucket_fill"], rect)
        # Outline
        pygame.draw.rect(surface, COLORS["bucket_outline"], rect, 2)

        # Range label below the bucket
        font = self._get_font()
        label_surf = font.render(self.label, True, COLORS["text_muted"])
        label_rect = label_surf.get_rect(centerx=int(self.center_x), top=rect.bottom + 8)
        surface.blit(label_surf, label_rect)
