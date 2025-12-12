#!/usr/bin/env python3
"""
Script: cross_platform.py
Purpose: Shared utilities for cross-platform compatibility
Crucible Suite Plugin
"""

import sys
import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

# Ensure Python 3.8+
if sys.version_info < (3, 8):
    print("Error: Python 3.8+ required", file=sys.stderr)
    sys.exit(1)


def find_crucible_project(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    Find a Crucible project by looking for .crucible directory.

    Args:
        start_path: Directory to start searching from (default: cwd)

    Returns:
        Path to project root or None if not found
    """
    if start_path is None:
        current = Path.cwd()
    else:
        current = Path(start_path)

    # Check current directory and parents
    for directory in [current] + list(current.parents):
        crucible_dir = directory / ".crucible"
        if crucible_dir.exists() and crucible_dir.is_dir():
            return directory

    return None


# Alias for backward compatibility
def get_crucible_root() -> Optional[Path]:
    """Find the Crucible project root. Alias for find_crucible_project()."""
    return find_crucible_project()


def get_plugin_root() -> Optional[Path]:
    """Get the plugin root directory from environment or detection."""
    # Check environment variable first
    env_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env_root:
        return Path(env_root)

    # Try to detect from script location
    script_path = Path(__file__).resolve()
    # scripts/ is inside plugin root
    if script_path.parent.name == "scripts":
        return script_path.parent.parent

    return None


def ensure_directory(path: Path) -> bool:
    """Ensure a directory exists, creating it if necessary."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except OSError as e:
        print(f"Error creating directory {path}: {e}", file=sys.stderr)
        return False


def safe_read_json(path: Path) -> Optional[Dict[str, Any]]:
    """Safely read a JSON file, returning None on error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError) as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        return None


def safe_write_json(path: Path, data: Dict[str, Any]) -> bool:
    """Safely write a JSON file with proper error handling."""
    try:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write to temp file first, then rename (atomic on most systems)
        temp_path = path.with_suffix(".tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Rename temp to final
        temp_path.replace(path)
        return True
    except OSError as e:
        print(f"Error writing {path}: {e}", file=sys.stderr)
        return False


def get_timestamp() -> str:
    """Get a filesystem-safe timestamp string."""
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def get_iso_timestamp() -> str:
    """Get an ISO format timestamp."""
    return datetime.now().isoformat()


def count_words(text: str) -> int:
    """Count words in a text string."""
    return len(text.split())


def extract_title_from_claude_md(project_root: Path) -> Optional[str]:
    """
    Extract the book title from CLAUDE.md file.

    Args:
        project_root: Path to project root containing CLAUDE.md

    Returns:
        Title string or None if not found
    """
    claude_md = project_root / "CLAUDE.md"
    if not claude_md.exists():
        return None

    try:
        with open(claude_md, "r", encoding="utf-8") as f:
            for line in f:
                if "Book Title:" in line:
                    return line.split(":", 1)[1].strip()
    except (OSError, UnicodeDecodeError):
        pass

    return None


def count_words_in_file(path: Path) -> int:
    """Count words in a file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return count_words(f.read())
    except (FileNotFoundError, OSError):
        return 0


def find_files(directory: Path, pattern: str) -> List[Path]:
    """Find files matching a glob pattern."""
    if not directory.exists():
        return []
    return sorted(directory.glob(pattern))


def backup_file(source: Path, backup_dir: Path) -> Optional[Path]:
    """Create a timestamped backup of a file."""
    if not source.exists():
        return None

    ensure_directory(backup_dir)

    timestamp = get_timestamp()
    backup_name = f"{source.stem}-{timestamp}{source.suffix}"
    backup_path = backup_dir / backup_name

    try:
        shutil.copy2(source, backup_path)
        return backup_path
    except OSError as e:
        print(f"Error backing up {source}: {e}", file=sys.stderr)
        return None


def get_project_state(project_root: Path) -> Optional[Dict[str, Any]]:
    """Load the current project state from various state files."""
    state = {
        "root": str(project_root),
        "phase": "unknown",
        "planning": None,
        "outline": None,
        "draft": None,
        "edit": None
    }

    state_dir = project_root / ".crucible" / "state"

    # Check for planning state
    planning_state = state_dir / "planning-state.json"
    if planning_state.exists():
        state["planning"] = safe_read_json(planning_state)
        state["phase"] = "planning"

    # Check for outline state
    outline_state = state_dir / "outline-state.json"
    if outline_state.exists():
        state["outline"] = safe_read_json(outline_state)
        state["phase"] = "outlining"

    # Check for draft state
    draft_state = state_dir / "draft-state.json"
    if draft_state.exists():
        state["draft"] = safe_read_json(draft_state)
        state["phase"] = "writing"

    # Check for edit state
    edit_state = state_dir / "edit-state.json"
    if edit_state.exists():
        state["edit"] = safe_read_json(edit_state)
        state["phase"] = "editing"

    return state


def format_output(data: Dict[str, Any], for_hook: bool = False) -> str:
    """Format output data as JSON, optionally for hook consumption."""
    if for_hook:
        return json.dumps(data, indent=2)
    return json.dumps(data, indent=2, ensure_ascii=False)


# Module-level exports
__all__ = [
    "find_crucible_project",
    "get_crucible_root",
    "get_plugin_root",
    "ensure_directory",
    "safe_read_json",
    "safe_write_json",
    "get_timestamp",
    "get_iso_timestamp",
    "count_words",
    "count_words_in_file",
    "extract_title_from_claude_md",
    "find_files",
    "backup_file",
    "get_project_state",
    "format_output"
]
