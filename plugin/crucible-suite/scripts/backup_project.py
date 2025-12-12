#!/usr/bin/env python3
"""
Script: backup_project.py
Purpose: Create a full backup of a Crucible project
Crucible Suite Plugin
"""

import sys
import json
import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

# Ensure Python 3.8+
if sys.version_info < (3, 8):
    print("Error: Python 3.8+ required", file=sys.stderr)
    sys.exit(1)

# Import shared utilities
try:
    from cross_platform import (
        get_crucible_root, ensure_directory, get_timestamp,
        safe_read_json, format_output
    )
except ImportError:
    # Fallback if not in path
    def get_crucible_root():
        current = Path.cwd()
        for directory in [current] + list(current.parents):
            if (directory / ".crucible").exists():
                return directory
        return None

    def ensure_directory(path):
        path.mkdir(parents=True, exist_ok=True)
        return True

    def get_timestamp():
        return datetime.now().strftime("%Y%m%d-%H%M%S")

    def format_output(data, for_hook=False):
        return json.dumps(data, indent=2)


def create_full_backup(project_root: Path = None, backup_dir: Path = None) -> dict:
    """Create a complete backup of the Crucible project."""

    # Find project root if not specified
    if project_root is None:
        project_root = get_crucible_root()
        if project_root is None:
            return {
                "success": False,
                "error": "No Crucible project found. Run from project directory or specify path."
            }

    project_root = Path(project_root)
    crucible_dir = project_root / ".crucible"

    if not crucible_dir.exists():
        return {
            "success": False,
            "error": f"No .crucible directory found in {project_root}"
        }

    # Set up backup directory
    if backup_dir is None:
        backup_dir = crucible_dir / "backups"

    ensure_directory(backup_dir)

    # Create timestamped backup
    timestamp = get_timestamp()
    backup_name = f"crucible-backup-{timestamp}"
    backup_path = backup_dir / f"{backup_name}.zip"

    # Directories to backup
    backup_targets = [
        crucible_dir / "planning",
        crucible_dir / "outline",
        crucible_dir / "draft",
        crucible_dir / "story-bible",
        crucible_dir / "style",
        crucible_dir / "state",
    ]

    # Also backup CLAUDE.md if it exists
    claude_md = project_root / "CLAUDE.md"

    files_backed_up = 0
    total_size = 0

    try:
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Backup .crucible subdirectories
            for target in backup_targets:
                if target.exists():
                    for file_path in target.rglob("*"):
                        if file_path.is_file():
                            arcname = file_path.relative_to(project_root)
                            zipf.write(file_path, arcname)
                            files_backed_up += 1
                            total_size += file_path.stat().st_size

            # Backup CLAUDE.md
            if claude_md.exists():
                zipf.write(claude_md, "CLAUDE.md")
                files_backed_up += 1
                total_size += claude_md.stat().st_size

        # Record backup in manifest
        manifest_path = backup_dir / "backup-manifest.json"
        manifest = []
        if manifest_path.exists():
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
            except json.JSONDecodeError:
                manifest = []

        manifest.append({
            "timestamp": timestamp,
            "file": backup_path.name,
            "files_count": files_backed_up,
            "size_bytes": total_size,
            "created": datetime.now().isoformat()
        })

        # Keep only last 20 backups in manifest
        manifest = manifest[-20:]

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return {
            "success": True,
            "backup_path": str(backup_path),
            "files_backed_up": files_backed_up,
            "size_bytes": total_size,
            "timestamp": timestamp,
            "message": f"Backup created: {backup_path.name}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Backup failed: {str(e)}"
        }


def main():
    # Read input
    project_root = None
    backup_dir = None

    if len(sys.argv) >= 2:
        project_root = Path(sys.argv[1])
        if len(sys.argv) >= 3:
            backup_dir = Path(sys.argv[2])
    else:
        try:
            input_data = json.load(sys.stdin)
            if "project_root" in input_data:
                project_root = Path(input_data["project_root"])
            if "backup_dir" in input_data:
                backup_dir = Path(input_data["backup_dir"])
        except json.JSONDecodeError:
            pass

    result = create_full_backup(project_root, backup_dir)
    print(format_output(result))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
