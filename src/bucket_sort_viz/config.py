"""Central configuration for Bucket Sort Visualizer."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from bucket_sort_viz.model.step import StepType

if TYPE_CHECKING:
    import pygame

# ──────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
OUTPUT_DIR = PROJECT_ROOT / "output"

# ──────────────────────────────────────────────
# Screen
# Dimensions fit cleanly on a 1920×1080 display
# with Windows taskbar visible and window chrome.
# ──────────────────────────────────────────────
SCREEN_WIDTH = 1694
SCREEN_HEIGHT = 924
FPS = 30
WINDOW_TITLE = "Bucket Sort \u2014 Lightning Labs"

# ──────────────────────────────────────────────
# Colors (RGB tuples)
# ──────────────────────────────────────────────
COLORS = {
    # Backgrounds
    "bg_dark": (15, 20, 30),
    "bg_panel": (20, 28, 40),
    "bg_menu": (12, 16, 24),
    # Text
    "text_primary": (200, 210, 220),
    "text_muted": (80, 100, 120),
    "text_bright": (240, 245, 250),
    # Phase colors
    "cyan_scatter": (0, 255, 208),
    "yellow_sort": (255, 215, 0),
    "magenta_gather": (255, 51, 102),
    "green_sorted": (0, 255, 136),
    # UI elements
    "bucket_outline": (40, 55, 75),
    "bucket_fill": (25, 35, 50),
    "branding_cyan": (0, 200, 180),
    "menu_highlight": (0, 180, 160),
    "menu_inactive": (60, 75, 95),
    # Element states
    "element_default": (100, 115, 135),
    "element_active": (255, 255, 255),
}

# ──────────────────────────────────────────────
# Fonts (bundled + system fallbacks)
# ──────────────────────────────────────────────
FONTS = {
    "title": {
        "path": FONTS_DIR / "JetBrainsMono-Bold.ttf",
        "fallback": "Consolas",
        "size": 36,
    },
    "subtitle": {
        "path": FONTS_DIR / "JetBrainsMono-Regular.ttf",
        "fallback": "Consolas",
        "size": 18,
    },
    "code": {
        "path": FONTS_DIR / "JetBrainsMono-Regular.ttf",
        "fallback": "Consolas",
        "size": 16,
    },
    "branding": {
        "path": FONTS_DIR / "JetBrainsMono-Bold.ttf",
        "fallback": "Courier New",
        "size": 28,
    },
    "label": {
        "path": FONTS_DIR / "JetBrainsMono-Regular.ttf",
        "fallback": "Consolas",
        "size": 14,
    },
    "value": {
        "path": FONTS_DIR / "JetBrainsMono-Bold.ttf",
        "fallback": "Consolas",
        "size": 14,
    },
    "menu_title": {
        "path": FONTS_DIR / "JetBrainsMono-Bold.ttf",
        "fallback": "Consolas",
        "size": 48,
    },
    "menu_item": {
        "path": FONTS_DIR / "JetBrainsMono-Regular.ttf",
        "fallback": "Consolas",
        "size": 22,
    },
}


def load_font(font_key: str) -> pygame.font.Font:
    """Load bundled font with system fallback for Windows compatibility."""
    import pygame

    spec = FONTS[font_key]
    try:
        return pygame.font.Font(str(spec["path"]), spec["size"])
    except FileNotFoundError:
        return pygame.font.SysFont(spec["fallback"], spec["size"])


# ──────────────────────────────────────────────
# Animation Timing (in seconds)
# ──────────────────────────────────────────────
TIMING = {
    "ready_hold": 1.5,
    "scatter_per_element": 0.6,
    "scatter_stagger": 0.15,
    "scatter_glow_warmup": 0.3,
    "phase_transition_pause": 1.0,
    "sort_swap": 0.4,
    "sort_compare_hold": 0.2,
    "sort_bucket_pause": 0.3,
    "gather_per_element": 0.5,
    "gather_stagger": 0.12,
    "celebration_hold": 2.5,
    "celebration_pulse_rate": 0.4,
}


def timing_to_frames(seconds: float) -> int:
    """Convert seconds to frame count based on FPS."""
    return max(1, round(seconds * FPS))


# ──────────────────────────────────────────────
# Element count
# ──────────────────────────────────────────────
ELEMENT_COUNT_MIN = 10
ELEMENT_COUNT_MAX = 15
ELEMENT_COUNT_DEFAULT = 10

# ──────────────────────────────────────────────
# Layout regions (y-coordinates and margins)
# ──────────────────────────────────────────────
INPUT_ROW_Y = 80
BUCKET_TOP_Y = 200
BUCKET_HEIGHT = 300
BUCKET_BOTTOM_Y = BUCKET_TOP_Y + BUCKET_HEIGHT
BUCKET_LABEL_Y = BUCKET_BOTTOM_Y + 20
OUTPUT_ROW_Y = INPUT_ROW_Y
PANEL_TOP_Y = 600
PANEL_HEIGHT = SCREEN_HEIGHT - PANEL_TOP_Y
SIDE_MARGIN = 40
BUCKET_GAP = 6

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
