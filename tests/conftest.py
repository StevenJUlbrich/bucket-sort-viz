"""Shared fixtures and markers for test suite."""

import os

import pytest

requires_display = pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Requires display — skipped in CI",
)


def pytest_configure(config):
    """Register custom markers so pytest doesn't warn about unknown markers."""
    config.addinivalue_line(
        "markers",
        "requires_display: marks tests that need a display (skipped in CI)",
    )
