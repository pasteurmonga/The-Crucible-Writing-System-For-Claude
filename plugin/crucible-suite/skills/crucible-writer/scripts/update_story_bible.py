#!/usr/bin/env python3
"""Update the story bible with new facts, foreshadowing, and character states."""

import json
import os
import sys
from datetime import datetime


def load_bible(path: str) -> dict:
    """Load the story bible."""
    bible_path = os.path.join(path, "story-bible.json")
    with open(bible_path, "r") as f:
        return json.load(f)


def save_bible(path: str, bible: dict) -> None:
    """Save the story bible."""
    bible["meta"]["updated"] = datetime.now().isoformat()
    bible_path = os.path.join(path, "story-bible.json")
    with open(bible_path, "w") as f:
        json.dump(bible, f, indent=2)


def add_established_fact(path: str, fact: str, chapter: int, scene: int = None) -> None:
    """
    Record a fact established in the narrative.
    
    Args:
        path: Project directory
        fact: The fact that was established
        chapter: Chapter where established
        scene: Scene where established (optional)
    """
    bible = load_bible(path)
    
    location = f"ch{chapter}" + (f".{scene}" if scene else "")
    
    bible["established_facts"].append({
        "fact": fact,
        "established_in": location,
        "added": datetime.now().isoformat()
    })
    
    save_bible(path, bible)
    print(f"✅ Added established fact: {fact[:50]}...")


def add_foreshadowing_plant(
    path: str, 
    thread: str, 
    chapter: int, 
    scene: int,
    expected_payoff: str = None
) -> None:
    """
    Record a foreshadowing plant.
    
    Args:
        path: Project directory
        thread: Description of what was planted
        chapter: Chapter where planted
        scene: Scene where planted
        expected_payoff: Where/when this should pay off
    """
    bible = load_bible(path)
    
    bible["foreshadowing"]["planted"].append({
        "thread": thread,
        "planted_in": f"ch{chapter}.{scene}",
        "expected_payoff": expected_payoff,
        "paid_off": False,
        "added": datetime.now().isoformat()
    })
    
    save_bible(path, bible)
    print(f"✅ Recorded foreshadowing plant: {thread[:50]}...")


def record_payoff(path: str, thread: str, chapter: int, scene: int) -> None:
    """
    Record that a foreshadowing thread was paid off.
    
    Args:
        path: Project directory
        thread: Description matching the original plant
        chapter: Chapter where paid off
        scene: Scene where paid off
    """
    bible = load_bible(path)
    
    # Find the plant
    for plant in bible["foreshadowing"]["planted"]:
        if thread.lower() in plant["thread"].lower():
            plant["paid_off"] = True
            plant["paid_in"] = f"ch{chapter}.{scene}"
            
            # Also record in paid_off list
            bible["foreshadowing"]["paid_off"].append({
                "thread": plant["thread"],
                "planted_in": plant["planted_in"],
                "paid_in": f"ch{chapter}.{scene}",
                "recorded": datetime.now().isoformat()
            })
            
            save_bible(path, bible)
            print(f"✅ Recorded payoff for: {thread[:50]}...")
            return
    
    print(f"⚠️ Could not find matching plant for: {thread[:50]}...")


def update_character_state(
    path: str, 
    character: str, 
    updates: dict,
    chapter: int = None
) -> None:
    """
    Update a character's current state.
    
    Args:
        path: Project directory
        character: Character name
        updates: Dict of state updates (location, emotional_state, knows, etc.)
        chapter: Chapter of update (for tracking)
    """
    bible = load_bible(path)
    
    if character not in bible["character_states"]:
        bible["character_states"][character] = {
            "location": None,
            "emotional_state": None,
            "knows": [],
            "relationships": {},
            "history": []
        }
    
    # Record current state to history if changing
    if chapter:
        history_entry = {
            "chapter": chapter,
            "state": dict(bible["character_states"][character])
        }
        if "history" not in bible["character_states"][character]:
            bible["character_states"][character]["history"] = []
        bible["character_states"][character]["history"].append(history_entry)
    
    # Apply updates
    for key, value in updates.items():
        if key == "knows" and isinstance(value, str):
            # Append to knows list
            if "knows" not in bible["character_states"][character]:
                bible["character_states"][character]["knows"] = []
            bible["character_states"][character]["knows"].append(value)
        elif key == "relationships" and isinstance(value, dict):
            # Update relationships dict
            if "relationships" not in bible["character_states"][character]:
                bible["character_states"][character]["relationships"] = {}
            bible["character_states"][character]["relationships"].update(value)
        else:
            bible["character_states"][character][key] = value
    
    save_bible(path, bible)
    print(f"✅ Updated state for: {character}")


def add_invented_detail(
    path: str, 
    detail: str, 
    chapter: int, 
    scene: int,
    category: str = "general"
) -> None:
    """
    Record an invented detail for author review.
    
    Args:
        path: Project directory
        detail: What was invented
        chapter: Chapter where used
        scene: Scene where used
        category: Type of invention (character, location, power, etc.)
    """
    bible = load_bible(path)
    
    bible["invented_details"].append({
        "detail": detail,
        "category": category,
        "chapter": chapter,
        "scene": scene,
        "reviewed": False,
        "approved": None,
        "added": datetime.now().isoformat()
    })
    
    save_bible(path, bible)
    print(f"⚠️ Flagged invented detail: {detail[:50]}...")


def approve_invention(path: str, detail_index: int, approved: bool = True) -> None:
    """
    Mark an invented detail as reviewed.
    
    Args:
        path: Project directory
        detail_index: Index in invented_details list
        approved: Whether to approve or reject
    """
    bible = load_bible(path)
    
    if detail_index < len(bible["invented_details"]):
        bible["invented_details"][detail_index]["reviewed"] = True
        bible["invented_details"][detail_index]["approved"] = approved
        
        if approved:
            # Add to established facts
            detail = bible["invented_details"][detail_index]["detail"]
            ch = bible["invented_details"][detail_index]["chapter"]
            bible["established_facts"].append({
                "fact": detail,
                "established_in": f"ch{ch}",
                "added": datetime.now().isoformat(),
                "was_invented": True
            })
        
        save_bible(path, bible)
        status = "approved" if approved else "rejected"
        print(f"✅ Invention {detail_index} {status}")
    else:
        print(f"⚠️ Invalid invention index: {detail_index}")


def update_timeline(path: str, chapter: int, timepoint: str) -> None:
    """
    Record when a chapter takes place.
    
    Args:
        path: Project directory
        chapter: Chapter number
        timepoint: When this chapter occurs (e.g., "Year 1, Spring")
    """
    bible = load_bible(path)
    
    bible["timeline"][str(chapter)] = timepoint
    
    save_bible(path, bible)
    print(f"✅ Timeline: Chapter {chapter} → {timepoint}")


def add_location(path: str, name: str, description: str, first_seen: int) -> None:
    """
    Record a location that has been visited.
    
    Args:
        path: Project directory
        name: Location name
        description: Brief description
        first_seen: Chapter where first described
    """
    bible = load_bible(path)
    
    bible["locations"][name] = {
        "description": description,
        "first_seen": f"ch{first_seen}",
        "added": datetime.now().isoformat()
    }
    
    save_bible(path, bible)
    print(f"✅ Added location: {name}")


def get_continuity_report(path: str) -> str:
    """
    Generate a continuity report for review.
    
    Args:
        path: Project directory
    
    Returns:
        Formatted report string
    """
    bible = load_bible(path)
    
    report = []
    report.append("# Continuity Report\n")
    report.append(f"Generated: {datetime.now().isoformat()}\n")
    
    # Progress
    progress = bible["progress"]
    report.append(f"\n## Progress")
    report.append(f"- Current position: Chapter {progress['current_chapter']}, Scene {progress['current_scene']}")
    report.append(f"- Words written: {progress['total_words']:,}")
    report.append(f"- Chapters complete: {progress['chapters_complete']}")
    
    # Unresolved foreshadowing
    unresolved = [p for p in bible["foreshadowing"]["planted"] if not p.get("paid_off")]
    if unresolved:
        report.append(f"\n## Unresolved Foreshadowing ({len(unresolved)})")
        for plant in unresolved:
            report.append(f"- {plant['thread']} (planted: {plant['planted_in']})")
    
    # Unreviewed inventions
    unreviewed = [d for d in bible["invented_details"] if not d.get("reviewed")]
    if unreviewed:
        report.append(f"\n## Unreviewed Inventions ({len(unreviewed)})")
        for i, detail in enumerate(unreviewed):
            report.append(f"- [{i}] {detail['detail']} (ch{detail['chapter']}.{detail['scene']})")
    
    # Character states
    report.append(f"\n## Current Character States")
    for char, state in bible["character_states"].items():
        report.append(f"\n### {char}")
        if state.get("location"):
            report.append(f"- Location: {state['location']}")
        if state.get("emotional_state"):
            report.append(f"- Emotional state: {state['emotional_state']}")
        if state.get("knows"):
            report.append(f"- Knows: {', '.join(state['knows'][-5:])}")  # Last 5 items
    
    return "\n".join(report)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  update_story_bible.py <path> --fact <chapter> <scene> <fact>")
        print("  update_story_bible.py <path> --plant <chapter> <scene> <thread>")
        print("  update_story_bible.py <path> --payoff <chapter> <scene> <thread>")
        print("  update_story_bible.py <path> --character <name> <key> <value>")
        print("  update_story_bible.py <path> --invented <chapter> <scene> <detail>")
        print("  update_story_bible.py <path> --report")
        sys.exit(1)
    
    path = sys.argv[1]
    command = sys.argv[2]
    
    if command == "--fact" and len(sys.argv) >= 6:
        add_established_fact(path, sys.argv[5], int(sys.argv[3]), int(sys.argv[4]))
    elif command == "--plant" and len(sys.argv) >= 6:
        add_foreshadowing_plant(path, sys.argv[5], int(sys.argv[3]), int(sys.argv[4]))
    elif command == "--payoff" and len(sys.argv) >= 6:
        record_payoff(path, sys.argv[5], int(sys.argv[3]), int(sys.argv[4]))
    elif command == "--character" and len(sys.argv) >= 6:
        update_character_state(path, sys.argv[3], {sys.argv[4]: sys.argv[5]})
    elif command == "--invented" and len(sys.argv) >= 6:
        add_invented_detail(path, sys.argv[5], int(sys.argv[3]), int(sys.argv[4]))
    elif command == "--report":
        print(get_continuity_report(path))
