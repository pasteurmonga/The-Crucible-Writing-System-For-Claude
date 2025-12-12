#!/usr/bin/env python3
"""
Script: load_project_context.py
Purpose: Load project context on session start (SessionStart hook)
Crucible Suite Plugin

This script runs at the start of a Claude Code session and provides
context about the current Crucible project state.
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

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


def get_project_context(project_root: Path) -> str:
    """Generate context string for the session."""

    if project_root is None:
        return ""  # No project found, no context to inject

    crucible_dir = project_root / ".crucible"
    state_dir = crucible_dir / "state"

    context_parts = [
        "=== CRUCIBLE PROJECT DETECTED ===",
        ""
    ]

    # Get title from CLAUDE.md
    title = "Untitled Project"
    claude_md = project_root / "CLAUDE.md"
    if claude_md.exists():
        try:
            with open(claude_md, "r", encoding="utf-8") as f:
                content = f.read()
                for line in content.split("\n"):
                    if "Book Title:" in line:
                        title = line.split(":", 1)[1].strip()
                        break
        except (OSError, UnicodeDecodeError):
            pass

    context_parts.append(f"Project: {title}")
    context_parts.append(f"Location: {project_root}")
    context_parts.append("")

    # Determine phase and provide relevant context
    phase = "not_started"
    phase_context = []

    # Check for edit state (highest priority)
    edit_state_file = state_dir / "edit-state.json"
    if edit_state_file.exists():
        phase = "editing"
        try:
            with open(edit_state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
                phase_context.append(f"Currently in: EDITING phase")
                phase_context.append(f"Edit level: {state.get('current_phase', 'unknown')}")
                chapters_edited = len(state.get("chapters", {}))
                phase_context.append(f"Chapters edited: {chapters_edited}")
        except (json.JSONDecodeError, OSError):
            pass

    # Check for draft state
    draft_state_file = state_dir / "draft-state.json"
    if not phase_context and draft_state_file.exists():
        phase = "writing"
        try:
            with open(draft_state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
                phase_context.append(f"Currently in: WRITING phase")
                phase_context.append(f"Current chapter: {state.get('current_chapter', '?')}")
                phase_context.append(f"Current scene: {state.get('current_scene', '?')}")
                phase_context.append(f"Word count: {state.get('word_count', 0):,}")
                phase_context.append(f"Target: {state.get('target_words', 150000):,}")

                # Check if bi-chapter review is due
                current_ch = state.get('chapters_complete', 0)
                if current_ch > 0 and current_ch % 2 == 0:
                    last_review = state.get('last_review_chapter', 0)
                    if last_review < current_ch:
                        phase_context.append("")
                        phase_context.append("⚠️ BI-CHAPTER REVIEW DUE")
                        phase_context.append(f"Review chapters {current_ch - 1}-{current_ch} before continuing")
        except (json.JSONDecodeError, OSError):
            pass

    # Check for outline state
    outline_state_file = state_dir / "outline-state.json"
    if not phase_context and outline_state_file.exists():
        phase = "outlining"
        try:
            with open(outline_state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
                phase_context.append(f"Currently in: OUTLINING phase")
                phase_context.append(f"Current chapter: {state.get('current_chapter', '?')}")
                phase_context.append(f"Chapters complete: {state.get('chapters_complete', 0)}/{state.get('total_chapters', '?')}")
        except (json.JSONDecodeError, OSError):
            pass

    # Check for planning state
    planning_state_file = state_dir / "planning-state.json"
    if not phase_context and planning_state_file.exists():
        phase = "planning"
        try:
            with open(planning_state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
                phase_context.append(f"Currently in: PLANNING phase")
                phase_context.append(f"Current document: {state.get('current_document', '?')}")
                phase_context.append(f"Documents complete: {state.get('documents_complete', 0)}/9")
        except (json.JSONDecodeError, OSError):
            pass

    # Check if we have planning docs but no state file
    planning_dir = crucible_dir / "planning"
    if not phase_context and planning_dir.exists():
        docs = list(planning_dir.glob("*.md")) + list(planning_dir.glob("**/*.md"))
        if docs:
            phase_context.append("Planning documents found")
            phase_context.append(f"Planning status: Complete ({len(docs)} documents)")

    if phase_context:
        context_parts.extend(phase_context)
    else:
        context_parts.append("No active session state found.")
        context_parts.append("Use /crucible-suite:crucible-plan to start a new project")
        context_parts.append("or /crucible-suite:crucible-continue to resume an existing one.")

    context_parts.append("")
    context_parts.append("Available commands:")
    context_parts.append("  /crucible-suite:crucible-status   - Show full project status")
    context_parts.append("  /crucible-suite:crucible-continue - Resume from current point")
    context_parts.append("")
    context_parts.append("=== END CRUCIBLE CONTEXT ===")

    return "\n".join(context_parts)


def main():
    # Read hook input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    # Find project
    project_root = find_crucible_project()

    # Generate context
    context = get_project_context(project_root)

    # Output for SessionStart hook
    # This format allows the context to be injected into the session
    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context
        }
    }

    print(json.dumps(output, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
