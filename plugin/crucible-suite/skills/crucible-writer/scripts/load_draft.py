#!/usr/bin/env python3
"""
Script: load_draft.py
Purpose: Load an existing Crucible draft project for resuming writing sessions
Crucible Writer Skill
"""

import json
import sys
from pathlib import Path

# Ensure Python 3.8+
if sys.version_info < (3, 8):
    print("Error: Python 3.8+ required", file=sys.stderr)
    sys.exit(1)


def find_draft_project(start_path: Path = None) -> Path:
    """Find a draft project by looking for story-bible.json or project-state.json."""
    if start_path is None:
        start_path = Path.cwd()

    current = Path(start_path)

    # Check if this is a draft project directory
    for directory in [current] + list(current.parents):
        if (directory / "story-bible.json").exists():
            return directory
        if (directory / "project-state.json").exists():
            return directory
        # Also check for .crucible structure
        crucible_draft = directory / ".crucible" / "draft"
        if crucible_draft.exists():
            return directory

    return None


def load_json_file(file_path: Path, default: dict = None) -> dict:
    """Safely load a JSON file."""
    if not file_path.exists():
        return default if default is not None else {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Could not load {file_path}: {e}", file=sys.stderr)
        return default if default is not None else {}


def load_draft(project_path: Path) -> dict:
    """
    Load an existing draft project.

    Args:
        project_path: Project directory path

    Returns:
        dict with loaded project data and status
    """
    if project_path is None:
        return {
            "success": False,
            "error": "No draft project found"
        }

    # Try multiple possible locations for state files
    possible_locations = [
        project_path,  # Direct project directory
        project_path / ".crucible",  # Inside .crucible
    ]

    story_bible = None
    style_profile = None
    project_state = None
    draft_state = None

    # Find and load story-bible.json
    for loc in possible_locations:
        bible_path = loc / "story-bible.json"
        if bible_path.exists():
            story_bible = load_json_file(bible_path)
            break

    # Find and load style-profile.json
    for loc in possible_locations:
        style_path = loc / "style-profile.json"
        if style_path.exists():
            style_profile = load_json_file(style_path)
            break
        # Also check style subdirectory
        style_path = loc / "style" / "style-profile.json"
        if style_path.exists():
            style_profile = load_json_file(style_path)
            break

    # Find and load project-state.json
    for loc in possible_locations:
        state_path = loc / "project-state.json"
        if state_path.exists():
            project_state = load_json_file(state_path)
            break

    # Find and load draft-state.json (for bi-chapter review tracking)
    for loc in possible_locations:
        draft_state_path = loc / "state" / "draft-state.json"
        if draft_state_path.exists():
            draft_state = load_json_file(draft_state_path)
            break
        draft_state_path = loc / "draft-state.json"
        if draft_state_path.exists():
            draft_state = load_json_file(draft_state_path)
            break

    # Check if we found essential files
    if story_bible is None and project_state is None:
        return {
            "success": False,
            "error": "No story-bible.json or project-state.json found",
            "searched_paths": [str(p) for p in possible_locations]
        }

    # Extract progress information
    progress = {}
    if story_bible and "progress" in story_bible:
        progress = story_bible["progress"]
    elif story_bible and "meta" in story_bible:
        # Fallback to meta if progress not found
        progress = {
            "current_chapter": 1,
            "current_scene": 1,
            "total_words": 0,
            "chapters_complete": 0,
            "status": "unknown"
        }

    # Extract metadata
    meta = {}
    if story_bible and "meta" in story_bible:
        meta = story_bible["meta"]
    elif project_state:
        meta = {
            "title": project_state.get("title", "Untitled"),
            "target_words": 150000,
            "target_chapters": 25
        }

    # Build comprehensive status
    status = {
        "success": True,
        "project_path": str(project_path),
        "title": meta.get("title", "Untitled"),
        "series": meta.get("series"),
        "book_number": meta.get("book_number", 1),
        "target_words": meta.get("target_words", 150000),
        "target_chapters": meta.get("target_chapters", 25),
        "words_per_chapter": meta.get("words_per_chapter", 6000),
        "progress": {
            "current_chapter": progress.get("current_chapter", 1),
            "current_scene": progress.get("current_scene", 1),
            "total_words": progress.get("total_words", 0),
            "chapters_complete": progress.get("chapters_complete", 0),
            "status": progress.get("status", "unknown")
        },
        "style_captured": False,
        "outline_loaded": False,
        "review_pending": False,
        "last_review_at_chapter": 0
    }

    # Check style profile status
    if style_profile:
        status["style_captured"] = style_profile.get("meta", {}).get("captured", False)

    # Check project state
    if project_state:
        status["outline_loaded"] = project_state.get("outline_loaded", False)
        status["last_updated"] = project_state.get("updated")
        status["phase"] = project_state.get("phase", "unknown")

    # Check draft state for bi-chapter reviews
    if draft_state:
        status["review_pending"] = draft_state.get("review_pending", False)
        status["last_review_at_chapter"] = draft_state.get("last_review_at_chapter", 0)
        status["chapters_complete"] = draft_state.get("chapters_complete", status["progress"]["chapters_complete"])

    # Calculate chapters until next review
    chapters_since_review = status["progress"]["chapters_complete"] - status["last_review_at_chapter"]
    status["chapters_until_review"] = max(0, 2 - chapters_since_review)

    # Include full data for detailed access
    status["data"] = {
        "story_bible": story_bible,
        "style_profile": style_profile,
        "project_state": project_state,
        "draft_state": draft_state
    }

    return status


def format_status_text(status: dict) -> str:
    """Format the status as readable text output."""
    if not status.get("success"):
        return f"Error: {status.get('error', 'Unknown error')}"

    prog = status["progress"]

    lines = [
        "═" * 50,
        f"DRAFT PROJECT LOADED",
        "═" * 50,
        "",
        f"📚 {status['title']}",
    ]

    if status.get("series"):
        lines.append(f"   Series: {status['series']}, Book {status['book_number']}")

    lines.extend([
        "",
        f"PROGRESS",
        "─" * 50,
        f"Current position: Chapter {prog['current_chapter']}, Scene {prog['current_scene']}",
        f"Chapters complete: {prog['chapters_complete']} / {status['target_chapters']}",
        f"Word count: {prog['total_words']:,} / {status['target_words']:,}",
        f"Status: {prog['status']}",
        "",
        f"SETUP STATUS",
        "─" * 50,
        f"Style captured: {'✓' if status['style_captured'] else '✗'}",
        f"Outline loaded: {'✓' if status['outline_loaded'] else '✗'}",
        "",
        f"BI-CHAPTER REVIEW",
        "─" * 50,
    ])

    if status["review_pending"]:
        lines.append("⚠️  REVIEW PENDING — Run /crucible-suite:crucible-review before continuing")
    else:
        lines.append(f"Chapters until next review: {status['chapters_until_review']}")
        lines.append(f"Last review at chapter: {status['last_review_at_chapter']}")

    lines.extend([
        "",
        "═" * 50,
        "",
        "Ready to continue. Next steps:",
    ])

    if not status["style_captured"]:
        lines.append("  1. Capture your writing style")
    if not status["outline_loaded"]:
        lines.append("  2. Load your chapter outline")
    if status["review_pending"]:
        lines.append("  → Run bi-chapter review first")
    else:
        lines.append(f"  → Continue writing Chapter {prog['current_chapter']}, Scene {prog['current_scene']}")

    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Load an existing Crucible draft project")
    parser.add_argument("project_path", nargs="?", default=".",
                        help="Path to the draft project directory")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of formatted text")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Minimal output (just success/failure)")

    args = parser.parse_args()

    # Find and load the project
    project_path = find_draft_project(Path(args.project_path))
    status = load_draft(project_path)

    if args.json:
        # Remove the full data from JSON output unless specifically needed
        output = {k: v for k, v in status.items() if k != "data"}
        print(json.dumps(output, indent=2))
    elif args.quiet:
        if status["success"]:
            prog = status["progress"]
            print(f"Loaded: {status['title']} — Ch {prog['current_chapter']}, Scene {prog['current_scene']}")
        else:
            print(f"Error: {status.get('error', 'Failed to load')}")
    else:
        print(format_status_text(status))

    sys.exit(0 if status["success"] else 1)


if __name__ == "__main__":
    main()
