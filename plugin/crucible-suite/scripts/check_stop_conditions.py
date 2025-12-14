#!/usr/bin/env python3
"""
Script: check_stop_conditions.py
Purpose: Stop hook to enforce bi-chapter reviews before session end
Crucible Suite Plugin

This script runs when Claude tries to stop and blocks if a bi-chapter
review is due but hasn't been performed.
"""

import sys
import json
from pathlib import Path

# Ensure Python 3.8+
if sys.version_info < (3, 8):
    print("Error: Python 3.8+ required", file=sys.stderr)
    sys.exit(1)


def find_crucible_project(start_path: Path = None) -> Path:
    """Find a Crucible project by looking for .crucible directory."""
    if start_path is None:
        start_path = Path.cwd()

    current = Path(start_path)
    for directory in [current] + list(current.parents):
        crucible_dir = directory / ".crucible"
        if crucible_dir.exists() and crucible_dir.is_dir():
            return directory

    return None


def check_review_needed(project_root: Path) -> dict:
    """
    Check if a bi-chapter review is needed.

    Returns:
        dict with keys:
        - review_needed: bool
        - chapters_to_review: tuple (start, end) or None
        - reason: str
    """
    if project_root is None:
        return {
            "review_needed": False,
            "chapters_to_review": None,
            "reason": "No Crucible project found"
        }

    state_dir = project_root / ".crucible" / "state"
    draft_state_file = state_dir / "draft-state.json"

    if not draft_state_file.exists():
        return {
            "review_needed": False,
            "chapters_to_review": None,
            "reason": "No draft state found (not in writing phase)"
        }

    try:
        with open(draft_state_file, "r", encoding="utf-8") as f:
            state = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return {
            "review_needed": False,
            "chapters_to_review": None,
            "reason": f"Could not read draft state: {e}"
        }

    chapters_complete = state.get("chapters_complete", 0)
    last_review_chapter = state.get("last_review_chapter", 0)

    # Bi-chapter review is due when:
    # 1. At least 2 chapters are complete
    # 2. chapters_complete is even (2, 4, 6, etc.)
    # 3. The last review didn't cover the current chapter pair
    if chapters_complete >= 2 and chapters_complete % 2 == 0:
        if last_review_chapter < chapters_complete:
            review_start = chapters_complete - 1
            review_end = chapters_complete
            return {
                "review_needed": True,
                "chapters_to_review": (review_start, review_end),
                "chapters_complete": chapters_complete,
                "last_review_chapter": last_review_chapter,
                "reason": f"Bi-chapter review required for chapters {review_start}-{review_end}"
            }

    return {
        "review_needed": False,
        "chapters_to_review": None,
        "chapters_complete": chapters_complete,
        "last_review_chapter": last_review_chapter,
        "reason": "No review currently due"
    }


def main():
    # Read hook input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    # Check if stop hook is already active (prevent infinite loops)
    stop_hook_active = input_data.get("stop_hook_active", False)
    if stop_hook_active:
        # Don't block if we're already in a stop hook continuation
        # This prevents infinite loops
        sys.exit(0)

    # Find project and check conditions
    project_root = find_crucible_project()
    result = check_review_needed(project_root)

    if result["review_needed"]:
        start, end = result["chapters_to_review"]
        # Exit code 2 blocks the stop and sends stderr to Claude
        error_message = (
            f"STOP BLOCKED: Bi-chapter review required.\n\n"
            f"You have completed {result['chapters_complete']} chapters but the last review "
            f"only covered up to chapter {result['last_review_chapter']}.\n\n"
            f"ACTION REQUIRED: Run the bi-chapter review for chapters {start}-{end} using:\n"
            f"  /crucible-suite:crucible-review {start}-{end}\n\n"
            f"After completing the review, you may stop the session."
        )
        print(error_message, file=sys.stderr)
        sys.exit(2)
    else:
        # Exit code 0 allows the stop
        # Optionally output success info (shown in verbose mode)
        output = {
            "decision": "approve",
            "reason": result["reason"]
        }
        print(json.dumps(output))
        sys.exit(0)


if __name__ == "__main__":
    main()
