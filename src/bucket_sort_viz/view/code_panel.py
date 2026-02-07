"""Pseudocode panel with line highlighting and Lightning Labs branding."""

import pygame

from bucket_sort_viz.config import COLORS, PSEUDOCODE_LINES, load_font


class CodePanel:
    """Bottom panel displaying pseudocode with an active-line highlight bar.

    Attributes:
        x, y: Top-left corner of the panel.
        width, height: Dimensions.
    """

    CODE_LEFT_MARGIN = 30
    CODE_TOP_OFFSET = 90       # Below branding + header
    LINE_HEIGHT = 24
    HIGHLIGHT_PAD_X = 10
    HIGHLIGHT_PAD_Y = 2

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._branding_font: pygame.font.Font | None = None
        self._header_font: pygame.font.Font | None = None
        self._code_font: pygame.font.Font | None = None

    def _ensure_fonts(self) -> None:
        if self._branding_font is None:
            self._branding_font = load_font("branding")
            self._header_font = load_font("subtitle")
            self._code_font = load_font("code")

    def draw(self, surface: pygame.Surface, active_line: int = -1) -> None:
        """Draw the full code panel.

        Args:
            surface: Pygame surface to draw on.
            active_line: Index of the pseudocode line to highlight (-1 for none).
        """
        self._ensure_fonts()

        # Panel background
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, COLORS["bg_panel"], panel_rect)

        # Top separator line
        pygame.draw.line(
            surface,
            COLORS["bucket_outline"],
            (self.x, self.y),
            (self.x + self.width, self.y),
            1,
        )

        # Branding: "LIGHTNING LABS"
        branding_surf = self._branding_font.render(
            "LIGHTNING LABS", True, COLORS["branding_cyan"],
        )
        surface.blit(branding_surf, (self.x + self.CODE_LEFT_MARGIN, self.y + 15))

        # Header: "ALGORITHM LOGIC"
        header_surf = self._header_font.render(
            "ALGORITHM LOGIC", True, COLORS["text_muted"],
        )
        surface.blit(header_surf, (self.x + self.CODE_LEFT_MARGIN, self.y + 55))

        # Pseudocode lines
        code_x = self.x + self.CODE_LEFT_MARGIN
        code_start_y = self.y + self.CODE_TOP_OFFSET

        for i, line in enumerate(PSEUDOCODE_LINES):
            line_y = code_start_y + i * self.LINE_HEIGHT

            # Highlight bar for active line
            if i == active_line:
                highlight_rect = pygame.Rect(
                    self.x + self.HIGHLIGHT_PAD_X,
                    line_y - self.HIGHLIGHT_PAD_Y,
                    self.width - 2 * self.HIGHLIGHT_PAD_X,
                    self.LINE_HEIGHT,
                )
                highlight_color = (*COLORS["cyan_scatter"][:3], 40)
                highlight_surface = pygame.Surface(
                    (highlight_rect.width, highlight_rect.height), pygame.SRCALPHA,
                )
                highlight_surface.fill(highlight_color)
                surface.blit(highlight_surface, highlight_rect.topleft)

            # Determine text color based on line content
            if line.startswith("#"):
                color = COLORS["text_muted"]
            elif line.strip().startswith("for ") or line.strip().startswith("output = "):
                color = COLORS["cyan_scatter"]
            else:
                color = COLORS["text_primary"]

            # Brighten active line text
            if i == active_line:
                color = COLORS["text_bright"]

            text_surf = self._code_font.render(line, True, color)
            surface.blit(text_surf, (code_x, line_y))
