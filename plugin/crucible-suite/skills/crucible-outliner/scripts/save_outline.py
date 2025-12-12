#!/usr/bin/env python3
"""Save outline project state."""

import json
import os
import sys
from datetime import datetime


def save_outline(path: str, updates: dict = None) -> dict:
    """
    Save or update outline project state.
    
    Args:
        path: Project directory path
        updates: Optional dict of state updates to merge
    
    Returns:
        Updated state dict
    """
    state_path = os.path.join(path, "state.json")
    
    # Load existing state
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state = json.load(f)
    else:
        raise FileNotFoundError(f"No state file found at {state_path}")
    
    # Merge updates if provided
    if updates:
        state = deep_merge(state, updates)
    
    # Update timestamp
    state["updated"] = datetime.now().isoformat()
    
    # Save state
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)
    
    print(f"✅ State saved: {state_path}")
    
    # Print progress summary
    if state.get("chapters"):
        completed = len([c for c in state["chapters"] if c.get("completed")])
        total = state["structure"].get("chapter_count", "?")
        print(f"   Progress: {completed}/{total} chapters outlined")
    
    return state


def deep_merge(base: dict, updates: dict) -> dict:
    """Deep merge two dictionaries."""
    result = base.copy()
    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def add_chapter(path: str, chapter_data: dict) -> dict:
    """
    Add or update a chapter in the outline.
    
    Args:
        path: Project directory path
        chapter_data: Chapter outline data
    
    Returns:
        Updated state dict
    """
    state_path = os.path.join(path, "state.json")
    
    with open(state_path, "r") as f:
        state = json.load(f)
    
    chapter_num = chapter_data.get("number", len(state["chapters"]) + 1)
    
    # Update or append chapter
    existing_idx = None
    for i, ch in enumerate(state["chapters"]):
        if ch.get("number") == chapter_num:
            existing_idx = i
            break
    
    if existing_idx is not None:
        state["chapters"][existing_idx] = chapter_data
        action = "Updated"
    else:
        state["chapters"].append(chapter_data)
        action = "Added"
    
    state["updated"] = datetime.now().isoformat()
    state["current_chapter"] = chapter_num
    
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)
    
    print(f"✅ {action} Chapter {chapter_num}: {chapter_data.get('title', 'Untitled')}")
    
    return state


def add_foreshadowing(path: str, thread_data: dict) -> dict:
    """
    Add a foreshadowing thread.
    
    Args:
        path: Project directory path
        thread_data: Foreshadowing thread data
    
    Returns:
        Updated state dict
    """
    state_path = os.path.join(path, "state.json")
    
    with open(state_path, "r") as f:
        state = json.load(f)
    
    state["foreshadowing"].append(thread_data)
    state["updated"] = datetime.now().isoformat()
    
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)
    
    print(f"✅ Added foreshadowing thread: {thread_data.get('name', 'Unnamed')}")
    
    return state


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: save_outline.py <path> [updates_json]")
        print("  path: Project directory")
        print("  updates_json: Optional JSON string of state updates")
        sys.exit(1)
    
    path = sys.argv[1]
    updates = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
    
    save_outline(path, updates)
