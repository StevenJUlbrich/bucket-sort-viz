# Brick-by-Brick Progress Tracker

## Bucket Sort Visualizer — Lightning Labs

---

## Brick 1: UV Init + Data Model + Presets + Step Recording

**Status:** COMPLETE
**Date:** 2026-02-07

### What Was Built

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project config with ruff, pytest, hatchling build system |
| `src/bucket_sort_viz/__init__.py` | Package marker |
| `src/bucket_sort_viz/__main__.py` | Enables `python -m bucket_sort_viz` |
| `src/bucket_sort_viz/main.py` | Stub entry point (full impl in Brick 11) |
| `src/bucket_sort_viz/config.py` | Element count constants, pseudocode lines, step-to-code-line mapping |
| `src/bucket_sort_viz/presets.py` | `SortPreset` frozen dataclass, 3 presets (small/medium/large), validation |
| `src/bucket_sort_viz/model/__init__.py` | Model package marker |
| `src/bucket_sort_viz/model/step.py` | `Step` dataclass with `StepType` and `PhaseName` Literal types |
| `src/bucket_sort_viz/model/bucket_sort.py` | Algorithm engine: generates values, sorts, records all steps |
| `tests/__init__.py` | Test package marker |
| `tests/conftest.py` | `requires_display` marker for CI-safe test tiering |
| `tests/test_presets.py` | 12 tests: validation, ranges, gaps, coverage, frozen check |
| `tests/test_bucket_sort.py` | 24 tests: correctness, value gen, reproducibility, permutation |
| `tests/test_step_recording.py` | 30 tests: phase order, scatter/sort/gather/celebration steps, code lines, IDs |

### Key Design Decisions

- **Layout-agnostic steps:** Algorithm records logical moves only (element IDs, bucket/slot/output indices). No pixel coordinates in the model layer.
- **Stable element IDs:** Each element's ID is its index in the original unsorted list. Handles duplicate values without ambiguity.
- **Internal value generation:** `bucket_sort(preset, count, seed)` generates values internally — simpler API for the animator.
- **Hatchling build system:** Required for `src/` layout so tests can import `bucket_sort_viz` as an installed package.

### Validation Results

```
Ruff:   All checks passed!
Pytest: 66 passed in 0.08s
```

#### Test Breakdown

| Test File | Tests | Status |
|-----------|-------|--------|
| `test_presets.py` | 12 | 12 passed |
| `test_bucket_sort.py` | 24 | 24 passed |
| `test_step_recording.py` | 30 | 30 passed |
| **Total** | **66** | **66 passed** |

### Notes

- `uv init` created a default `main.py` at the project root — removed in favor of `src/bucket_sort_viz/main.py`
- Python pinned to 3.13.6 via UV
- `.python-version` file auto-created by `uv python pin 3.13`
- UV initialized a git repo automatically during `uv init`

---

## Brick 2: Static Layout Renderer

**Status:** COMPLETE
**Date:** 2026-02-07

### What Was Built

| File | Purpose |
|------|---------|
| `assets/fonts/JetBrainsMono-Regular.ttf` | Bundled code font (SIL Open Font License) |
| `assets/fonts/JetBrainsMono-Bold.ttf` | Bundled heading/branding font |
| `assets/fonts/OFL.txt` | JetBrains Mono license file |
| `src/bucket_sort_viz/config.py` | Extended with screen, colors, fonts, timing, layout constants |
| `src/bucket_sort_viz/view/__init__.py` | View package marker |
| `src/bucket_sort_viz/view/renderer.py` | `Renderer` class: Pygame window init, layout builder, READY state draw loop |
| `src/bucket_sort_viz/view/elements.py` | `CircleElement` (circle + value text) and `BucketRegion` (outlined rect + label) |
| `src/bucket_sort_viz/view/code_panel.py` | `CodePanel`: pseudocode display, active-line highlight, "LIGHTNING LABS" branding |
| `src/bucket_sort_viz/view/effects.py` | Stub for glow/particle effects (Brick 8) |

### What It Shows (READY State)

- **Input row:** Gray circles with numeric values, evenly spaced across the top
- **Bucket region:** Outlined rectangles with range labels (e.g., "0–24", "25–49") below each bucket
- **Code panel:** Dark bottom panel with "LIGHTNING LABS" branding (cyan), "ALGORITHM LOGIC" header, and 11 pseudocode lines with syntax-aware coloring
- **Layout:** Adapts to all 3 presets (4, 8, 10 buckets) and 10–15 elements

### Config Constants Added

| Section | Constants |
|---------|-----------|
| Paths | `PROJECT_ROOT`, `ASSETS_DIR`, `FONTS_DIR`, `OUTPUT_DIR` |
| Screen | `SCREEN_WIDTH=1694`, `SCREEN_HEIGHT=924`, `FPS=30`, `WINDOW_TITLE` |
| Colors | Full `COLORS` dict (17 named colors across backgrounds, text, phases, UI, elements) |
| Fonts | `FONTS` dict (8 font specs) + `load_font()` with system fallback |
| Timing | `TIMING` dict (12 animation timing values) + `timing_to_frames()` |
| Layout | `INPUT_ROW_Y`, `BUCKET_TOP_Y`, `BUCKET_HEIGHT`, `PANEL_TOP_Y`, `SIDE_MARGIN`, `BUCKET_GAP` |

### Validation Results

```
Ruff:   All checks passed!
Pytest: 66 passed in 0.06s (all Brick 1 tests still green)
Visual: Pygame window launches and displays READY state correctly
```

### How to Verify Visually

```powershell
cd d:\Visual_Learning_Sorting\bucket-sort-viz
uv run python -c "
from bucket_sort_viz.view.renderer import Renderer
from bucket_sort_viz.model.bucket_sort import bucket_sort
from bucket_sort_viz.presets import PRESETS
preset = PRESETS['small']  # Try 'medium' or 'large' too
original, _, _ = bucket_sort(preset, count=10, seed=42)
Renderer(preset, original).run_static()
"
```
Press ESC or close window to exit.

### Notes

- `config.py` now uses `from __future__ import annotations` + `TYPE_CHECKING` for the `pygame.font.Font` return type annotation (avoids ruff F821 with lazy pygame import)
- Font loading uses bundled JetBrains Mono with fallback to system Consolas/Courier New
- Brick 3 (drawable classes) is effectively merged into Brick 2 — `CircleElement` and `BucketRegion` are already functional

---

## Brick 3: Drawable Classes (CircleElement, BucketRegion)

**Status:** NOT STARTED

---

## Brick 4: Tween Engine + Easing Functions

**Status:** NOT STARTED

---

## Brick 5: Phase 1 — Scatter Animation

**Status:** NOT STARTED

---

## Brick 6: Phase 2 — Sort Buckets Animation

**Status:** NOT STARTED

---

## Brick 7: Phase 3 — Gather Animation

**Status:** NOT STARTED

---

## Brick 8: Celebration + Glow Effects

**Status:** NOT STARTED

---

## Brick 9: Code Panel + Branding + Line Sync

**Status:** NOT STARTED

---

## Brick 10: Pygame Menu Screen

**Status:** NOT STARTED

---

## Brick 11: CLI Argument Parsing + Dual Interface

**Status:** NOT STARTED

---

## Brick 12: Video Export (Piped ffmpeg)

**Status:** NOT STARTED

---

## Brick 13: GitHub Polish (README, Docs, CI, GIF)

**Status:** NOT STARTED

---

## Brick 14: Sound Effects (Optional)

**Status:** NOT STARTED
