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

**Status:** NOT STARTED

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
