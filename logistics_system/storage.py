"""Load and save logistics system state as JSON."""

import json
from pathlib import Path
from typing import Any


def load_state(path: str | Path) -> dict[str, Any]:
    """Load state from a JSON file."""
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_state(path: str | Path, state: dict[str, Any]) -> None:
    """Save state to a JSON file."""
    file_path = Path(path)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(state, file, ensure_ascii=False, indent=2)
