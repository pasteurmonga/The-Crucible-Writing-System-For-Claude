#!/usr/bin/env python3
"""Save draft progress and chapter content."""

import json
import os
import sys
from datetime import datetime


def save_scene(
    path: str, 
    chapter: int, 
    scene: int, 
    content: str,
    scene_summary: str = None
) -> dict:
    """
    Save a scene draft.
    
    Args:
        path: Project directory
        chapter: Chapter number
        scene: Scene number
        content: Scene prose content
        scene_summary: Brief summary for story bible
    
    Returns:
        Updated progress info
    """
    # Load project state
    bible_path = os.path.join(path, "story-bible.json")
    state_path = os.path.join(path, "project-state.json")

    # Load story bible with error handling
    if not os.path.exists(bible_path):
        raise FileNotFoundError(f"Story bible not found at {bible_path}. Run init_draft.py first.")

    try:
        with open(bible_path, "r", encoding="utf-8") as f:
            story_bible = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in story-bible.json: {e}")

    # Load project state with error handling
    if not os.path.exists(state_path):
        raise FileNotFoundError(f"Project state not found at {state_path}. Run init_draft.py first.")

    try:
        with open(state_path, "r", encoding="utf-8") as f:
            project_state = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in project-state.json: {e}")
    
    # Create chapter file if needed
    chapter_dir = os.path.join(path, "draft", "chapters")
    chapter_file = os.path.join(chapter_dir, f"ch{chapter:02d}.md")
    
    # Read existing chapter content or create new
    if os.path.exists(chapter_file):
        with open(chapter_file, "r") as f:
            chapter_content = f.read()
    else:
        chapter_content = f"# Chapter {chapter}\n\n"
    
    # Add scene marker and content
    scene_marker = f"\n## Scene {scene}\n\n"
    
    # If scene already exists, replace it; otherwise append
    if scene_marker in chapter_content:
        # Find and replace the scene
        start = chapter_content.find(scene_marker)
        next_scene = chapter_content.find(f"\n## Scene {scene + 1}\n", start)
        if next_scene == -1:
            # Last scene in chapter
            chapter_content = chapter_content[:start] + scene_marker + content + "\n"
        else:
            chapter_content = chapter_content[:start] + scene_marker + content + "\n" + chapter_content[next_scene:]
    else:
        # Append new scene
        chapter_content += scene_marker + content + "\n"
    
    # Save chapter file
    with open(chapter_file, "w") as f:
        f.write(chapter_content)
    
    # Count words in scene
    word_count = len(content.split())
    
    # Update story bible
    chapter_key = str(chapter)
    if chapter_key not in story_bible["chapters"]:
        story_bible["chapters"][chapter_key] = {
            "title": f"Chapter {chapter}",
            "word_count": 0,
            "scenes": {},
            "summary": "",
            "final_state": {},
            "completed": False
        }
    
    story_bible["chapters"][chapter_key]["scenes"][str(scene)] = {
        "word_count": word_count,
        "summary": scene_summary or "",
        "saved": datetime.now().isoformat()
    }
    
    # Recalculate chapter word count
    total_chapter_words = sum(
        s["word_count"] for s in story_bible["chapters"][chapter_key]["scenes"].values()
    )
    story_bible["chapters"][chapter_key]["word_count"] = total_chapter_words
    
    # Recalculate total words
    total_words = sum(
        ch["word_count"] for ch in story_bible["chapters"].values()
    )
    story_bible["progress"]["total_words"] = total_words
    story_bible["progress"]["current_chapter"] = chapter
    story_bible["progress"]["current_scene"] = scene
    story_bible["meta"]["updated"] = datetime.now().isoformat()
    
    # Update project state
    project_state["updated"] = datetime.now().isoformat()
    project_state["phase"] = "writing"
    
    # Save files
    with open(bible_path, "w") as f:
        json.dump(story_bible, f, indent=2)
    
    with open(state_path, "w") as f:
        json.dump(project_state, f, indent=2)
    
    print(f"✅ Saved Chapter {chapter}, Scene {scene}")
    print(f"   Words in scene: {word_count:,}")
    print(f"   Chapter total: {total_chapter_words:,}")
    print(f"   Book total: {total_words:,}")
    
    return {
        "scene_words": word_count,
        "chapter_words": total_chapter_words,
        "total_words": total_words
    }


def complete_chapter(
    path: str, 
    chapter: int,
    chapter_summary: str,
    final_character_states: dict = None
) -> dict:
    """
    Mark a chapter as complete and save summary.
    
    Args:
        path: Project directory
        chapter: Chapter number
        chapter_summary: 100-200 word summary
        final_character_states: Character states at chapter end
    
    Returns:
        Updated progress info
    """
    bible_path = os.path.join(path, "story-bible.json")

    if not os.path.exists(bible_path):
        raise FileNotFoundError(f"Story bible not found at {bible_path}")

    try:
        with open(bible_path, "r", encoding="utf-8") as f:
            story_bible = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in story-bible.json: {e}")

    chapter_key = str(chapter)
    
    if chapter_key not in story_bible["chapters"]:
        raise ValueError(f"Chapter {chapter} not found")
    
    story_bible["chapters"][chapter_key]["summary"] = chapter_summary
    story_bible["chapters"][chapter_key]["completed"] = True
    story_bible["chapters"][chapter_key]["completed_at"] = datetime.now().isoformat()
    
    if final_character_states:
        story_bible["chapters"][chapter_key]["final_state"] = final_character_states
        # Also update current character states
        for char, state in final_character_states.items():
            if char not in story_bible["character_states"]:
                story_bible["character_states"][char] = {}
            story_bible["character_states"][char].update(state)
    
    # Update progress
    completed = sum(1 for ch in story_bible["chapters"].values() if ch.get("completed", False))
    story_bible["progress"]["chapters_complete"] = completed
    story_bible["progress"]["current_chapter"] = chapter + 1
    story_bible["progress"]["current_scene"] = 1
    story_bible["meta"]["updated"] = datetime.now().isoformat()
    
    with open(bible_path, "w") as f:
        json.dump(story_bible, f, indent=2)
    
    target = story_bible["meta"]["target_chapters"]
    
    print(f"✅ Chapter {chapter} marked complete")
    print(f"   Progress: {completed}/{target} chapters ({completed/target*100:.1f}%)")
    print(f"   Total words: {story_bible['progress']['total_words']:,}")
    
    return {
        "chapters_complete": completed,
        "total_words": story_bible["progress"]["total_words"]
    }


def save_session_end(path: str, words_written: int, scenes_completed: int) -> None:
    """
    Save end-of-session information.
    
    Args:
        path: Project directory
        words_written: Words written this session
        scenes_completed: Scenes completed this session
    """
    state_path = os.path.join(path, "project-state.json")
    
    with open(state_path, "r") as f:
        project_state = json.load(f)
    
    project_state["last_session"]["ended"] = datetime.now().isoformat()
    project_state["last_session"]["words_written"] = words_written
    project_state["last_session"]["scenes_completed"] = scenes_completed
    project_state["updated"] = datetime.now().isoformat()
    
    with open(state_path, "w") as f:
        json.dump(project_state, f, indent=2)
    
    print(f"✅ Session saved")
    print(f"   Words this session: {words_written:,}")
    print(f"   Scenes completed: {scenes_completed}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  save_draft.py <path> --scene <chapter> <scene> <content_file>")
        print("  save_draft.py <path> --complete-chapter <chapter> <summary_file>")
        print("  save_draft.py <path> --end-session <words> <scenes>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if len(sys.argv) > 2:
        if sys.argv[2] == "--scene" and len(sys.argv) >= 6:
            chapter = int(sys.argv[3])
            scene = int(sys.argv[4])
            with open(sys.argv[5], "r") as f:
                content = f.read()
            save_scene(path, chapter, scene, content)
        elif sys.argv[2] == "--complete-chapter" and len(sys.argv) >= 5:
            chapter = int(sys.argv[3])
            with open(sys.argv[4], "r") as f:
                summary = f.read()
            complete_chapter(path, chapter, summary)
        elif sys.argv[2] == "--end-session" and len(sys.argv) >= 5:
            words = int(sys.argv[3])
            scenes = int(sys.argv[4])
            save_session_end(path, words, scenes)
