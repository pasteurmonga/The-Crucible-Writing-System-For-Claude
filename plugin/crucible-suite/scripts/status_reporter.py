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


def generate_status_report(project_root: Path) -> dict:
    """Generate a comprehensive status report."""

    if project_root is None:
        return {
            "success": False,
            "error": "No Crucible project found"
        }

    crucible_dir = project_root / ".crucible"

    report = {
        "success": True,
        "project_root": str(project_root),
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

    # Get title from CLAUDE.md
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
    planning_dir = crucible_dir / "planning"
    planning_docs = {
        "crucible-thesis.md": "Thesis",
        "strand-maps": "Strand Maps",
        "forge-points": "Forge Points",
        "dark-mirror-profile.md": "Dark Mirror",
        "constellation-bible.md": "Constellation Bible",
        "mercy-ledger.md": "Mercy Ledger",
        "world-forge.md": "World Forge"
    }

    planning_complete = 0
    planning_total = len(planning_docs)
    planning_status = {}

    for doc, name in planning_docs.items():
        doc_path = planning_dir / doc
        if doc_path.exists():
            planning_status[name] = "complete"
            planning_complete += 1
        else:
            planning_status[name] = "pending"

    report["planning"] = {
        "complete": planning_complete,
        "total": planning_total,
        "percentage": int((planning_complete / planning_total) * 100) if planning_total > 0 else 0,
        "documents": planning_status,
        "last_modified": get_last_modified(planning_dir)
    }

    # Outline status
    outline_dir = crucible_dir / "outline"
    by_chapter_dir = outline_dir / "by-chapter"

    outline_chapters = []
    if by_chapter_dir.exists():
        outline_chapters = sorted(by_chapter_dir.glob("ch*.md"))

    # Try to get total from state or default
    total_chapters = 25  # Default
    state_file = crucible_dir / "state" / "outline-state.json"
    if state_file.exists():
        try:
            with open(state_file, "r", encoding="utf-8") as f:
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
    draft_dir = crucible_dir / "draft"
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
    draft_state_file = crucible_dir / "state" / "draft-state.json"
    current_chapter = None
    current_scene = None

    if draft_state_file.exists():
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
    edit_state_file = crucible_dir / "state" / "edit-state.json"
    editing_info = {
        "started": False,
        "chapters_edited": 0,
        "current_phase": "not_started"
    }

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
    backup_dir = crucible_dir / "backups"
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
    elif report["planning"]["complete"] > 0:
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

    lines.extend([
        "",
        f"EDITING     {'Not started' if not report['editing']['started'] else f'{report[\"editing\"][\"chapters_edited\"]} chapters edited'}",
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

    project_root = find_crucible_project(start_path)
    report = generate_status_report(project_root)

    if output_format == "text":
        print(format_report_text(report))
    else:
        print(json.dumps(report, indent=2))

    sys.exit(0 if report.get("success") else 1)


if __name__ == "__main__":
    main()
