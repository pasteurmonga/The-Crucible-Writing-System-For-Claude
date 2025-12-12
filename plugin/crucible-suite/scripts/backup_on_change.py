#!/usr/bin/env python3
"""
Script: backup_on_change.py
Purpose: Incremental backup triggered by PostToolUse hook on Write|Edit
Crucible Suite Plugin
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# Ensure Python 3.8+
if sys.version_info < (3, 8):
    print("Error: Python 3.8+ required", file=sys.stderr)
    sys.exit(1)


def get_timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def should_backup_file(file_path: str) -> bool:
    """Determine if a file change should trigger a backup."""
    if not file_path:
        return False

    path = Path(file_path)
    path_str = str(path).lower()

    # Never backup backup files
    if "backup" in path_str:
        return False

    # Backup if it's in .crucible directory
    if ".crucible" in path.parts:
        return True

    # Backup CLAUDE.md
    if path.name == "CLAUDE.md":
        return True

    # Backup markdown files in common Crucible directories
    crucible_dirs = ["draft", "chapter", "planning", "outline", "story-bible", "style"]
    if path.suffix == ".md":
        for dir_name in crucible_dirs:
            if dir_name in path.parts:
                return True

    # Backup JSON state files
    if path.suffix == ".json" and "state" in path.parts:
        return True

    # Backup any file in a crucible-project directory structure
    # Check if any parent directory contains .crucible
    try:
        for parent in path.parents:
            if (parent / ".crucible").exists():
                # This file is in a Crucible project
                # Backup markdown and JSON files
                if path.suffix in [".md", ".json"]:
                    return True
                break
    except (OSError, PermissionError):
        pass

    return False


def incremental_backup(file_path: str, project_root: Path = None) -> dict:
    """Create an incremental backup of a changed file."""

    if not should_backup_file(file_path):
        return {
            "success": True,
            "action": "skipped",
            "reason": "File not in backup scope"
        }

    source = Path(file_path)
    if not source.exists():
        return {
            "success": True,
            "action": "skipped",
            "reason": "File does not exist (may be new)"
        }

    # Find project root
    if project_root is None:
        current = source.parent
        for directory in [current] + list(current.parents):
            if (directory / ".crucible").exists():
                project_root = directory
                break

    if project_root is None:
        return {
            "success": False,
            "error": "Could not find Crucible project root"
        }

    # Set up incremental backup directory
    backup_dir = project_root / ".crucible" / "backups" / "incremental"
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Create backup with timestamp
    timestamp = get_timestamp()
    # Use try/except for Python 3.8 compatibility (is_relative_to added in 3.9)
    try:
        relative_path = source.relative_to(project_root)
    except ValueError:
        relative_path = Path(source.name)
    safe_name = str(relative_path).replace("/", "_").replace("\\", "_")
    backup_name = f"{timestamp}-{safe_name}"
    backup_path = backup_dir / backup_name

    try:
        shutil.copy2(source, backup_path)

        # Clean up old incremental backups (keep last 100)
        all_backups = sorted(backup_dir.glob("*"), key=lambda x: x.stat().st_mtime)
        if len(all_backups) > 100:
            for old_backup in all_backups[:-100]:
                old_backup.unlink()

        return {
            "success": True,
            "action": "backed_up",
            "source": str(source),
            "backup": str(backup_path),
            "timestamp": timestamp
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Backup failed: {str(e)}"
        }


def main():
    # Read hook input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    # Extract file path from hook data
    # PostToolUse hook provides tool_input which may contain file_path
    file_path = None

    tool_input = input_data.get("tool_input", {})
    if isinstance(tool_input, dict):
        file_path = tool_input.get("file_path") or tool_input.get("path")

    # Also check direct input
    if not file_path:
        file_path = input_data.get("file_path")

    if not file_path:
        print(json.dumps({
            "success": True,
            "action": "skipped",
            "reason": "No file path in hook input"
        }))
        sys.exit(0)

    result = incremental_backup(file_path)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
