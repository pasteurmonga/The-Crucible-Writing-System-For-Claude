#!/usr/bin/env python3
"""
Script: status_reporter.py
Purpose: Generate comprehensive project status report for /crucible-suite:crucible-status
Crucible Suite Plugin
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


def find_crucible_project(start_path: Path = None) -> tuple[Path, str]:
    """Find a Crucible project by looking for project markers.

    Returns:
        Tuple of (project_root, structure_type) where structure_type is:
        - "dotcrucible": .crucible/ directory structure
        - "rootlevel": state.json at project root (planner-created)
        - None if no project found
    """
    if start_path is None:
        start_path = Path.cwd()

    current = Path(start_path)
    for directory in [current] + list(current.parents):
        # Check for .crucible directory (legacy/future structure)
        crucible_dir = directory / ".crucible"
        if crucible_dir.exists() and crucible_dir.is_dir():
            return directory, "dotcrucible"

        # Check for state.json at root (planner-created structure)
        state_file = directory / "state.json"
        if state_file.exists():
            return directory, "rootlevel"

    return None, None


def count_words_in_file(file_path: Path) -> int:
    """Count words in a single file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return len(f.read().split())
    except (OSError, UnicodeDecodeError):
        return 0


def get_last_modified(directory: Path) -> str:
    """Get the most recent modification time from files in a directory."""
    latest = None
    if directory.exists():
        for file_path in directory.rglob("*"):
            if file_path.is_file():
                mtime = file_path.stat().st_mtime
                if latest is None or mtime > latest:
                    latest = mtime

    if latest:
        return datetime.fromtimestamp(latest).strftime("%Y-%m-%d %H:%M")
    return "Unknown"


def generate_status_report(project_root: Path, structure_type: str = None) -> dict:
    """Generate a comprehensive status report."""

    if project_root is None:
        return {
            "success": False,
            "error": "No Crucible project found"
        }

    # Determine paths based on structure type
    if structure_type == "dotcrucible":
        crucible_dir = project_root / ".crucible"
        planning_dir = crucible_dir / "planning"
        outline_dir = crucible_dir / "outline"
        draft_dir = crucible_dir / "draft"
        state_dir = crucible_dir / "state"
        backup_dir = crucible_dir / "backups"
        state_file = None  # Uses individual state files in state_dir
    else:
        # rootlevel structure (planner-created)
        crucible_dir = project_root
        planning_dir = project_root / "planning"
        outline_dir = project_root / "outline"
        draft_dir = project_root / "draft"
        state_dir = project_root  # state.json at root
        backup_dir = project_root / "backups"
        state_file = project_root / "state.json"

    report = {
        "success": True,
        "project_root": str(project_root),
        "structure_type": structure_type,
        "title": "Untitled",
        "phase": "not_started",
        "overall_progress": 0,
        "planning": {},
        "outline": {},
        "writing": {},
        "editing": {},
        "backups": {},
        "recent_files": []
    }

    # Load state.json for rootlevel structure
    project_state = {}
    if state_file and state_file.exists():
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                project_state = json.load(f)
                # Get title from state
                if "project" in project_state and "title" in project_state["project"]:
                    report["title"] = project_state["project"]["title"]
        except (json.JSONDecodeError, OSError):
            pass

    # Get title from CLAUDE.md (fallback or override)
    claude_md = project_root / "CLAUDE.md"
    if claude_md.exists():
        try:
            with open(claude_md, "r", encoding="utf-8") as f:
                content = f.read()
                for line in content.split("\n"):
                    if "Book Title:" in line:
                        report["title"] = line.split(":", 1)[1].strip()
                        break
        except (OSError, UnicodeDecodeError):
            pass

    # Planning status
    # Map document numbers to display names (9 documents total)
    planning_doc_map = {
        1: "Thesis",
        2: "Quest Strand",
        3: "Fire Strand",
        4: "Constellation Strand",
        5: "Forge Points",
        6: "Dark Mirror",
        7: "Constellation Bible",
        8: "Mercy Ledger",
        9: "World Forge"
    }

    # File-based detection (for compiled documents)
    file_docs = {
        "crucible-thesis.md": "Thesis",
        "strand-maps": "Strand Maps",
        "forge-points": "Forge Points",
        "dark-mirror-profile.md": "Dark Mirror",
        "constellation-bible.md": "Constellation Bible",
        "mercy-ledger.md": "Mercy Ledger",
        "world-forge.md": "World Forge"
    }

    planning_complete = 0
    planning_total = 9  # Total planning documents
    planning_status = {}

    # Check for rootlevel state.json progress
    if structure_type == "rootlevel" and project_state:
        progress = project_state.get("progress", {})
        documents_complete = progress.get("documents_complete", [])
        current_doc = progress.get("current_document", 1)

        # Map document numbers to state.json document keys
        doc_num_to_key = {
            1: "doc1_crucible_thesis",
            2: "doc2_quest_strand",
            3: "doc3_fire_strand",
            4: "doc4_constellation_strand",
            5: "doc5_forge_points",
            6: "doc6_dark_mirror",
            7: "doc7_constellation_bible",
            8: "doc8_mercy_ledger",
            9: "doc9_world_forge"
        }

        for doc_num, name in planning_doc_map.items():
            doc_key = doc_num_to_key.get(doc_num)
            if doc_key and doc_key in documents_complete:
                planning_status[name] = "complete"
                planning_complete += 1
            elif doc_num == current_doc:
                planning_status[name] = "in_progress"
            else:
                planning_status[name] = "pending"
    else:
        # File-based detection
        for doc, name in file_docs.items():
            doc_path = planning_dir / doc
            if doc_path.exists():
                planning_status[name] = "complete"
                planning_complete += 1
            else:
                planning_status[name] = "pending"
        planning_total = len(file_docs)

    report["planning"] = {
        "complete": planning_complete,
        "total": planning_total,
        "percentage": int((planning_complete / planning_total) * 100) if planning_total > 0 else 0,
        "documents": planning_status,
        "last_modified": get_last_modified(planning_dir),
        "current_document": project_state.get("progress", {}).get("current_document") if structure_type == "rootlevel" else None
    }

    # Outline status
    by_chapter_dir = outline_dir / "by-chapter"

    outline_chapters = []
    if by_chapter_dir.exists():
        outline_chapters = sorted(by_chapter_dir.glob("ch*.md"))

    # Try to get total from state or default
    total_chapters = 25  # Default
    if structure_type == "rootlevel":
        # Get from project_state scope
        total_chapters = project_state.get("scope", {}).get("chapters", 25) or 25
    else:
        outline_state_file = state_dir / "outline-state.json"
        if outline_state_file.exists():
            try:
                with open(outline_state_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    total_chapters = state.get("total_chapters", 25)
            except (json.JSONDecodeError, OSError):
                pass

    report["outline"] = {
        "complete": len(outline_chapters),
        "total": total_chapters,
        "percentage": int((len(outline_chapters) / total_chapters) * 100) if total_chapters > 0 else 0,
        "last_modified": get_last_modified(outline_dir)
    }

    # Writing status
    chapters_dir = draft_dir / "chapters"

    draft_chapters = []
    if chapters_dir.exists():
        draft_chapters = sorted(chapters_dir.glob("chapter-*.md"))
    elif draft_dir.exists():
        draft_chapters = sorted(draft_dir.glob("chapter-*.md"))

    total_words = 0
    for chapter in draft_chapters:
        total_words += count_words_in_file(chapter)

    # Get target words from state
    target_words = 150000  # Default
    current_chapter = None
    current_scene = None

    if structure_type == "dotcrucible":
        draft_state_file = state_dir / "draft-state.json"
    else:
        draft_state_file = None  # rootlevel doesn't use separate draft state file yet

    if draft_state_file and draft_state_file.exists():
        try:
            with open(draft_state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
                target_words = state.get("target_words", 150000)
                current_chapter = state.get("current_chapter")
                current_scene = state.get("current_scene")
        except (json.JSONDecodeError, OSError):
            pass

    report["writing"] = {
        "chapters_complete": len(draft_chapters),
        "total_chapters": total_chapters,
        "current_chapter": current_chapter,
        "current_scene": current_scene,
        "word_count": total_words,
        "target_words": target_words,
        "percentage": int((total_words / target_words) * 100) if target_words > 0 else 0,
        "last_modified": get_last_modified(draft_dir)
    }

    # Editing status
    editing_info = {
        "started": False,
        "chapters_edited": 0,
        "current_phase": "not_started"
    }

    if structure_type == "dotcrucible":
        edit_state_file = state_dir / "edit-state.json"
        if edit_state_file.exists():
            try:
                with open(edit_state_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    editing_info["started"] = True
                    editing_info["chapters_edited"] = len(state.get("chapters", {}))
                    editing_info["current_phase"] = state.get("current_phase", "assessment")
            except (json.JSONDecodeError, OSError):
                pass

    report["editing"] = editing_info

    # Backup status
    manifest_file = backup_dir / "backup-manifest.json"

    backup_info = {
        "count": 0,
        "latest": None
    }

    if manifest_file.exists():
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
                backup_info["count"] = len(manifest)
                if manifest:
                    backup_info["latest"] = manifest[-1].get("timestamp")
        except (json.JSONDecodeError, OSError):
            pass

    report["backups"] = backup_info

    # Determine current phase
    if report["editing"]["started"]:
        report["phase"] = "editing"
    elif report["writing"]["word_count"] > 0:
        report["phase"] = "writing"
    elif report["outline"]["complete"] > 0:
        report["phase"] = "outlining"
    elif report["planning"]["complete"] > 0 or report["planning"].get("current_document"):
        report["phase"] = "planning"
    else:
        report["phase"] = "not_started"

    # Calculate overall progress (weighted)
    # Planning: 10%, Outline: 15%, Writing: 60%, Editing: 15%
    overall = (
        (report["planning"]["percentage"] * 0.10) +
        (report["outline"]["percentage"] * 0.15) +
        (report["writing"]["percentage"] * 0.60) +
        (report["editing"].get("percentage", 0) * 0.15)
    )
    report["overall_progress"] = int(overall)

    return report


def format_report_text(report: dict) -> str:
    """Format the report as readable text output."""
    if not report.get("success"):
        return f"Error: {report.get('error', 'Unknown error')}"

    lines = [
        "═" * 50,
        f"CRUCIBLE PROJECT STATUS",
        "═" * 50,
        "",
        f"📚 {report['title']}",
        f"   Phase: {report['phase'].upper()}",
        f"   Progress: {report['overall_progress']}% complete",
        "",
        f"PLANNING    {'█' * (report['planning']['percentage'] // 5)}{'░' * (20 - report['planning']['percentage'] // 5)} {report['planning']['percentage']}%",
    ]

    for doc, status in report["planning"]["documents"].items():
        icon = "✓" if status == "complete" else "○"
        lines.append(f"├─ {doc}: {icon}")

    lines.extend([
        "",
        f"OUTLINING   {'█' * (report['outline']['percentage'] // 5)}{'░' * (20 - report['outline']['percentage'] // 5)} {report['outline']['percentage']}%",
        f"├─ Chapters outlined: {report['outline']['complete']}/{report['outline']['total']}",
        "",
        f"WRITING     {'█' * (report['writing']['percentage'] // 5)}{'░' * (20 - report['writing']['percentage'] // 5)} {report['writing']['percentage']}%",
        f"├─ Chapters written: {report['writing']['chapters_complete']}/{report['writing']['total_chapters']}",
        f"├─ Word count: {report['writing']['word_count']:,} / {report['writing']['target_words']:,}",
    ])

    if report["writing"]["current_chapter"]:
        lines.append(f"├─ Current: Chapter {report['writing']['current_chapter']}, Scene {report['writing'].get('current_scene', '?')}")

    editing_status = 'Not started' if not report['editing']['started'] else f"{report['editing']['chapters_edited']} chapters edited"
    lines.extend([
        "",
        f"EDITING     {editing_status}",
        "",
        f"Last backup: {report['backups']['latest'] or 'Never'}",
        "═" * 50,
    ])

    return "\n".join(lines)


def main():
    # Read input
    start_path = None
    output_format = "json"

    if len(sys.argv) >= 2:
        start_path = Path(sys.argv[1])
        if len(sys.argv) >= 3:
            output_format = sys.argv[2]
    else:
        try:
            input_data = json.load(sys.stdin)
            if "path" in input_data:
                start_path = Path(input_data["path"])
            output_format = input_data.get("format", "json")
        except json.JSONDecodeError:
            pass

    project_root, structure_type = find_crucible_project(start_path)
    report = generate_status_report(project_root, structure_type)

    if output_format == "text":
        print(format_report_text(report))
    else:
        print(json.dumps(report, indent=2))

    sys.exit(0 if report.get("success") else 1)


if __name__ == "__main__":
    main()
