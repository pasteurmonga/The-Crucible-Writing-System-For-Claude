#!/usr/bin/env python3
"""
Script: backup_on_change.py
Purpose: Incremental backup triggered by PostToolUse hook on Write|Edit
         Also checks for chapter completion and reminds about bi-chapter reviews
Crucible Suite Plugin
"""

import sys
import json
import shutil
import re
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


def is_chapter_file(file_path: str) -> tuple:
    """
    Check if a file is a chapter file and extract chapter number.

    Returns:
        tuple: (is_chapter: bool, chapter_number: int or None)
    """
    if not file_path:
        return False, None

    path = Path(file_path)
    name = path.name.lower()

    # Common chapter file patterns
    patterns = [
        r'chapter[_-]?(\d+)',
        r'ch[_-]?(\d+)',
        r'(\d+)[_-]?chapter',
    ]

    for pattern in patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            return True, int(match.group(1))

    # Check if in a chapters/draft directory
    if any(part in ['chapters', 'draft', 'manuscript'] for part in path.parts):
        # Try to find a number in the filename
        numbers = re.findall(r'\d+', name)
        if numbers:
            return True, int(numbers[0])

    return False, None


def check_review_status(project_root: Path) -> dict:
    """
    Check if a bi-chapter review is due.

    Returns:
        dict with review status information
    """
    if project_root is None:
        return {"review_due": False}

    state_dir = project_root / ".crucible" / "state"
    draft_state_file = state_dir / "draft-state.json"

    if not draft_state_file.exists():
        return {"review_due": False}

    try:
        with open(draft_state_file, "r", encoding="utf-8") as f:
            state = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"review_due": False}

    chapters_complete = state.get("chapters_complete", 0)
    last_review_chapter = state.get("last_review_chapter", 0)

    # Check if review is due
    if chapters_complete >= 2 and chapters_complete % 2 == 0:
        if last_review_chapter < chapters_complete:
            return {
                "review_due": True,
                "chapters_complete": chapters_complete,
                "review_start": chapters_complete - 1,
                "review_end": chapters_complete
            }

    return {
        "review_due": False,
        "chapters_complete": chapters_complete
    }


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


def find_project_root(file_path: str) -> Path:
    """Find Crucible project root from a file path."""
    if not file_path:
        return None

    path = Path(file_path)
    for directory in [path.parent] + list(path.parent.parents):
        if (directory / ".crucible").exists():
            return directory
    return None


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

    # Perform backup
    result = incremental_backup(file_path)

    # Check if this was a chapter file and if review is now due
    is_chapter, chapter_num = is_chapter_file(file_path)
    project_root = find_project_root(file_path)
    review_status = check_review_status(project_root)

    # Build output with optional review reminder
    output = {
        "success": result["success"],
        "action": result.get("action", "unknown"),
        "backup_result": result
    }

    # If a chapter file was modified and review is due, add context for Claude
    if is_chapter and review_status.get("review_due"):
        review_start = review_status["review_start"]
        review_end = review_status["review_end"]

        output["hookSpecificOutput"] = {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"[CRUCIBLE REMINDER] Chapter {chapter_num} was just modified. "
                f"You have now completed {review_status['chapters_complete']} chapters. "
                f"A bi-chapter review is due for chapters {review_start}-{review_end}. "
                f"Please run /crucible-suite:crucible-review {review_start}-{review_end} "
                f"before continuing to the next chapter."
            )
        }
        output["review_reminder"] = {
            "review_due": True,
            "chapters": f"{review_start}-{review_end}"
        }

    print(json.dumps(output, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
