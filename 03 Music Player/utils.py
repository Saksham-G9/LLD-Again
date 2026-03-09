"""Small utility helpers for the music player."""
from __future__ import annotations

def format_time(seconds: int) -> str:
    """Return MM:SS formatted time for given seconds."""
    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"


def print_progress(elapsed: int, total: int, width: int = 40) -> None:
    """Print progress in-place, padded to avoid leftover characters.

    Prints a single-line progress like `Progress: 00:03/03:20` and
    keeps the cursor on the same line.
    """
    text = f"Progress: {format_time(elapsed)}/{format_time(total)}"
    print(text.ljust(width), end="\r", flush=True)
