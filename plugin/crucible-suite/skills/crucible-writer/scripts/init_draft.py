#!/usr/bin/env python3
"""Initialize a new Crucible draft project."""

import json
import os
import sys
from datetime import datetime


def init_draft(
    path: str, 
    title: str, 
    chapters: int = 25, 
    target_words: int = 100000,
    book_number: int = 1,
    series_name: str = None
) -> dict:
    """
    Initialize a new draft project directory.
    
    Args:
        path: Directory path for the project
        title: Book title
        chapters: Expected chapter count
        target_words: Target word count
        book_number: Book number in series (1 for standalone)
        series_name: Series name (None for standalone)
    
    Returns:
        dict with project info
    """
    # Create directory structure
    os.makedirs(path, exist_ok=True)
    os.makedirs(os.path.join(path, "draft", "chapters"), exist_ok=True)
    os.makedirs(os.path.join(path, "manuscript"), exist_ok=True)
    
    # Calculate words per chapter
    words_per_chapter = target_words // chapters
    
    # Initialize story bible
    story_bible = {
        "meta": {
            "title": title,
            "series": series_name,
            "book_number": book_number,
            "target_words": target_words,
            "target_chapters": chapters,
            "words_per_chapter": words_per_chapter,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat()
        },
        "progress": {
            "current_chapter": 1,
            "current_scene": 1,
            "total_words": 0,
            "chapters_complete": 0,
            "status": "initialized"
        },
        "chapters": {},
        "character_states": {},
        "established_facts": [],
        "foreshadowing": {
            "planted": [],
            "paid_off": []
        },
        "timeline": {},
        "invented_details": [],
        "locations": {},
        "relationships": {}
    }
    
    # Initialize style profile (empty, to be filled)
    style_profile = {
        "meta": {
            "captured": False,
            "sample_source": None,
            "updated": datetime.now().isoformat()
        },
        "sentences": {
            "average_length": None,
            "variation": None,
            "structure_mix": None,
            "rhythm": None
        },
        "vocabulary": {
            "register": None,
            "density": None,
            "signature_words": [],
            "avoid_words": []
        },
        "dialogue": {
            "attribution_style": None,
            "character_distinction": None,
            "subtext_level": None
        },
        "description": {
            "sensory_focus": None,
            "metaphor_density": None,
            "setting_integration": None
        },
        "interiority": {
            "pov_depth": None,
            "emotion_approach": None,
            "reflection_frequency": None
        },
        "pacing": {
            "transition_style": None,
            "white_space": None,
            "tension_technique": None
        },
        "signature_elements": [],
        "genre_conventions": {
            "genre": None,
            "subgenre": None,
            "specific_conventions": []
        }
    }
    
    # Initialize project state
    project_state = {
        "title": title,
        "path": path,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "phase": "setup",
        "outline_loaded": False,
        "style_captured": False,
        "last_session": {
            "started": None,
            "ended": None,
            "words_written": 0,
            "scenes_completed": 0
        }
    }
    
    # Save files
    bible_path = os.path.join(path, "story-bible.json")
    style_path = os.path.join(path, "style-profile.json")
    state_path = os.path.join(path, "project-state.json")
    
    with open(bible_path, "w") as f:
        json.dump(story_bible, f, indent=2)
    
    with open(style_path, "w") as f:
        json.dump(style_profile, f, indent=2)
    
    with open(state_path, "w") as f:
        json.dump(project_state, f, indent=2)
    
    # Create placeholder for outline
    outline_path = os.path.join(path, "outline.md")
    with open(outline_path, "w") as f:
        f.write(f"# {title} — Chapter Outline\n\n")
        f.write("[Paste or upload your crucible-outliner output here]\n")
    
    print(f"✅ Initialized draft project: {title}")
    print(f"   Location: {path}")
    print(f"   Target: {target_words:,} words across {chapters} chapters")
    print(f"   Per chapter: ~{words_per_chapter:,} words")
    print()
    print("📁 Directory structure created:")
    print(f"   {path}/")
    print("   ├── story-bible.json")
    print("   ├── style-profile.json")
    print("   ├── project-state.json")
    print("   ├── outline.md (placeholder)")
    print("   ├── draft/")
    print("   │   └── chapters/")
    print("   └── manuscript/")
    print()
    print("📋 Next steps:")
    print("   1. Load your chapter outline")
    print("   2. Capture your writing style")
    print("   3. Begin drafting chapter 1")
    
    return {
        "story_bible": story_bible,
        "style_profile": style_profile,
        "project_state": project_state
    }


# Note: load_draft() functionality is in separate load_draft.py script


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: init_draft.py <path> <title> [--chapters N] [--target-words N]")
        print("  path: Directory for the project")
        print("  title: Book title")
        print("  --chapters: Expected chapter count (default: 25)")
        print("  --target-words: Target word count (default: 100000)")
        sys.exit(1)
    
    path = sys.argv[1]
    title = sys.argv[2]
    
    # Parse optional arguments
    chapters = 25
    target_words = 100000
    
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--chapters" and i + 1 < len(sys.argv):
            chapters = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--target-words" and i + 1 < len(sys.argv):
            target_words = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1
    
    init_draft(path, title, chapters, target_words)
