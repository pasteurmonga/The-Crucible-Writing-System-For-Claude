#!/usr/bin/env python3
"""
Save state for a Crucible Planner project.

Usage:
    python save_state.py <project_path>

Can also be imported and used programmatically:
    from save_state import save_state, update_answer, mark_document_complete
"""

import json
import os
import sys
from datetime import datetime


def load_state(project_path: str) -> dict:
    """Load state from project directory."""
    state_path = os.path.join(project_path, "state.json")
    if not os.path.exists(state_path):
        raise FileNotFoundError(f"No state file found at {state_path}")
    
    with open(state_path, 'r') as f:
        return json.load(f)


def save_state(project_path: str, state: dict) -> None:
    """Save state to project directory."""
    state["project"]["last_updated"] = datetime.now().isoformat()
    
    state_path = os.path.join(project_path, "state.json")
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"✅ State saved: {state_path}")


def update_answer(project_path: str, document: str, question: str, answer: str) -> dict:
    """Update a single answer in the state."""
    state = load_state(project_path)
    
    # Navigate to the right place in state
    if document.startswith("doc5_forge_points"):
        # Handle nested forge points
        parts = document.split(".")
        if len(parts) == 2:
            state["answers"]["doc5_forge_points"][parts[1]][question] = answer
        else:
            state["answers"]["doc5_forge_points"][question] = answer
    elif document.startswith("doc7_constellation_bible"):
        parts = document.split(".")
        if len(parts) == 2:
            if parts[1] == "protagonist":
                state["answers"]["doc7_constellation_bible"]["protagonist"][question] = answer
            else:
                # Handle character additions
                state["answers"]["doc7_constellation_bible"]["characters"].append({
                    "name": parts[1],
                    question: answer
                })
        else:
            state["answers"]["doc7_constellation_bible"][question] = answer
    elif document.startswith("doc8_mercy_ledger"):
        parts = document.split(".")
        if len(parts) == 2:
            state["answers"]["doc8_mercy_ledger"][parts[1]][question] = answer
        else:
            state["answers"]["doc8_mercy_ledger"][question] = answer
    else:
        state["answers"][document][question] = answer
    
    # Update progress
    state["progress"]["total_questions_answered"] += 1
    
    save_state(project_path, state)
    return state


def update_progress(project_path: str, document: int, question: int) -> dict:
    """Update current progress position."""
    state = load_state(project_path)
    state["progress"]["current_document"] = document
    state["progress"]["current_question"] = question
    save_state(project_path, state)
    return state


def mark_document_complete(project_path: str, document_num: int) -> dict:
    """Mark a document as complete."""
    state = load_state(project_path)
    if document_num not in state["progress"]["documents_complete"]:
        state["progress"]["documents_complete"].append(document_num)
    state["progress"]["current_document"] = document_num + 1
    state["progress"]["current_question"] = 1
    save_state(project_path, state)
    print(f"✅ Document {document_num} marked complete")
    return state


def set_scope(project_path: str, target_length: str, complexity: str) -> dict:
    """Set project scope."""
    state = load_state(project_path)
    state["scope"]["target_length"] = target_length
    state["scope"]["complexity"] = complexity
    
    # Calculate approximate chapters
    chapters_map = {
        "standard": 22,
        "epic": 30,
        "extended": 40
    }
    state["scope"]["chapters"] = chapters_map.get(target_length, 25)
    
    save_state(project_path, state)
    return state


def main():
    if len(sys.argv) < 2:
        print("Usage: python save_state.py <project_path>")
        print("\nThis script is primarily used programmatically.")
        print("Import functions: save_state, update_answer, mark_document_complete")
        sys.exit(1)
    
    project_path = sys.argv[1]
    state = load_state(project_path)
    save_state(project_path, state)


if __name__ == "__main__":
    main()
