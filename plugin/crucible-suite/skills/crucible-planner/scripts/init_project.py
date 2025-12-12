#!/usr/bin/env python3
"""
Initialize a new Crucible Planner project.

Usage:
    python init_project.py <project_path> <title> <premise>

Example:
    python init_project.py "./my-novel" "The Ashen Crown" "A healer discovers her power comes from stealing life"
"""

import json
import os
import sys
from datetime import datetime


def init_project(project_path: str, title: str, premise: str) -> dict:
    """Initialize a new Crucible planning project."""
    
    # Create directory structure
    directories = [
        project_path,
        os.path.join(project_path, "planning"),
        os.path.join(project_path, "planning", "strand-maps"),
        os.path.join(project_path, "planning", "forge-points"),
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Initialize state
    state = {
        "project": {
            "title": title,
            "premise": premise,
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "scope": {
            "target_length": None,  # "standard", "epic", "extended"
            "complexity": None,     # "single", "dual", "ensemble"
            "chapters": None
        },
        "progress": {
            "current_document": 1,
            "current_question": 1,
            "documents_complete": [],
            "total_questions_answered": 0
        },
        "answers": {
            "doc1_crucible_thesis": {},
            "doc2_quest_strand": {},
            "doc3_fire_strand": {},
            "doc4_constellation_strand": {},
            "doc5_forge_points": {
                "fp0_ignition": {},
                "fp1_first": {},
                "fp2_second": {},
                "fp3_third": {},
                "apex": {}
            },
            "doc6_dark_mirror": {},
            "doc7_constellation_bible": {
                "protagonist": {},
                "characters": []
            },
            "doc8_mercy_ledger": {
                "mercy_1": {},
                "mercy_2": {},
                "mercy_3": {},
                "mercy_4": {}
            },
            "doc9_world_forge": {}
        }
    }
    
    # Save state
    state_path = os.path.join(project_path, "state.json")
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"✅ Initialized Crucible project: {title}")
    print(f"   Location: {os.path.abspath(project_path)}")
    print(f"   State file: {state_path}")
    print(f"\n📁 Directory structure created:")
    print(f"   {project_path}/")
    print(f"   ├── state.json")
    print(f"   └── planning/")
    print(f"       ├── strand-maps/")
    print(f"       └── forge-points/")
    
    return state


def main():
    if len(sys.argv) < 4:
        print("Usage: python init_project.py <project_path> <title> <premise>")
        print("Example: python init_project.py ./my-novel \"The Ashen Crown\" \"A healer discovers...\"")
        sys.exit(1)
    
    project_path = sys.argv[1]
    title = sys.argv[2]
    premise = " ".join(sys.argv[3:])
    
    init_project(project_path, title, premise)


if __name__ == "__main__":
    main()
