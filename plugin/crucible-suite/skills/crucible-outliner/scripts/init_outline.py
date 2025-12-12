#!/usr/bin/env python3
"""Initialize a new Crucible outline project."""

import json
import os
import sys
from datetime import datetime


def init_outline(path: str, title: str, book_info: str = "Standalone") -> dict:
    """
    Initialize a new outline project directory.
    
    Args:
        path: Directory path for the project
        title: Book title
        book_info: "Standalone" or "Book X of Y"
    
    Returns:
        dict with project info
    """
    # Create directory structure
    os.makedirs(path, exist_ok=True)
    os.makedirs(os.path.join(path, "outline"), exist_ok=True)
    os.makedirs(os.path.join(path, "outline", "by-chapter"), exist_ok=True)
    
    # Initialize state
    state = {
        "title": title,
        "book_info": book_info,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "phase": "setup",
        "crucible_elements": {},
        "structure": {
            "chapter_count": None,
            "beat_mapping": [],
            "movements": {}
        },
        "chapters": [],
        "foreshadowing": [],
        "character_threads": {},
        "current_chapter": 0
    }
    
    # Save state
    state_path = os.path.join(path, "state.json")
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)
    
    print(f"✅ Initialized outline project: {title}")
    print(f"   Location: {path}")
    print(f"   Book: {book_info}")
    print(f"   State file: {state_path}")
    print()
    print("📁 Directory structure created:")
    print(f"   {path}/")
    print("   ├── state.json")
    print("   └── outline/")
    print("       └── by-chapter/")
    
    return state


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: init_outline.py <path> <title> [book_info]")
        print("  path: Directory for the project")
        print("  title: Book title")
        print("  book_info: 'Standalone' or 'Book X of Y' (optional)")
        sys.exit(1)
    
    path = sys.argv[1]
    title = sys.argv[2]
    book_info = sys.argv[3] if len(sys.argv) > 3 else "Standalone"
    
    init_outline(path, title, book_info)
