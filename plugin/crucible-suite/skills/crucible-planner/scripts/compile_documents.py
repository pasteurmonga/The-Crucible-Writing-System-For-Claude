#!/usr/bin/env python3
"""
Compile all planning documents from collected answers.

Usage:
    python compile_documents.py <project_path>

Generates all 9 planning documents plus a summary card.
"""

import json
import os
import sys
from datetime import datetime


def load_state(project_path: str) -> dict:
    """Load state from project directory."""
    state_path = os.path.join(project_path, "state.json")
    with open(state_path, 'r') as f:
        return json.load(f)


def generate_crucible_thesis(state: dict, output_dir: str) -> str:
    """Generate the Crucible Thesis document."""
    answers = state["answers"]["doc1_crucible_thesis"]
    project = state["project"]
    
    content = f"""# Crucible Thesis: {project['title']}

## The Forging Question

> Can the protagonist become {answers.get('forging_become', '[what they must become]')} without becoming {answers.get('dark_mirror_represents', '[what the dark mirror represents]')}?

---

## The Three Strands

### The Burden (Quest Strand)
**Nature:** {answers.get('burden_type', '[burden type]')}

The external weight that must be carried toward resolution.

### The Fire (Fire Strand)
**Nature:** {answers.get('fire_type', '[fire type]')}

The internal power that threatens to consume.

### The Core Bond (Constellation Strand)
**Bond Type:** {answers.get('core_bond_type', '[bond type]')}

The anchor that cannot break.

---

## The Dark Mirror

**Connection:** {answers.get('dark_mirror_connection', '[connection]')}
**Their Truth:** "{answers.get('antagonist_truth', '[antagonist philosophy]')}"

What the protagonist could become if the forging fails.

---

## The Theme

> {answers.get('theme', '[theme statement]')}

---

## The Surrender

At the Apex, the protagonist must willingly surrender: **{answers.get('surrender_type', '[surrender]')}**

---

## The Blade's Purpose

After the forging, the protagonist becomes: **{answers.get('blade_purpose', '[purpose]')}**

---

## Original Premise

{project['premise']}
"""
    
    filepath = os.path.join(output_dir, "crucible-thesis.md")
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath


def generate_quest_strand(state: dict, output_dir: str) -> str:
    """Generate the Quest Strand Map."""
    answers = state["answers"]["doc2_quest_strand"]
    project = state["project"]
    
    content = f"""# Quest Strand Map: {project['title']}

## The Burden

**Origin:** {answers.get('burden_origin', '[origin]')}
**Why This Protagonist:** {answers.get('why_protagonist', '[reason]')}

---

## Quest Arc by Movement

### Movement I — Discovery
The burden is discovered/received.

### Movement II — First Attempt
First significant obstacle; first failure.

### Movement III — Expansion
Quest scope expands: {answers.get('quest_escalation', '[escalation]')}

### Movement IV — Convergence
All threads converging toward resolution.

### Movement V — Resolution
The burden ends: {answers.get('resolution_method', '[resolution]')}

---

## The Antagonist's Stake

**Why They Oppose:** {answers.get('antagonist_stake', '[stake]')}

---

## The Impossible Element

**What Makes It Hopeless:** {answers.get('impossible_requirement', '[requirement]')}
"""
    
    filepath = os.path.join(output_dir, "strand-maps", "quest-strand.md")
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath


def generate_fire_strand(state: dict, output_dir: str) -> str:
    """Generate the Fire Strand Map."""
    answers = state["answers"]["doc3_fire_strand"]
    project = state["project"]
    
    content = f"""# Fire Strand Map: {project['title']}

## The Fire

**Manifestation:** {answers.get('fire_manifestation', '[manifestation]')}

---

## The Danger

**If Unmastered:** {answers.get('fire_danger', '[danger]')}

---

## The Cost

**Each Use Costs:** {answers.get('cost_of_use', '[cost]')}

---

## Fire Arc by Movement

### Movement I — Awakening
The Fire first manifests.

### Movement II — Instability
Control is partial/unreliable.

### Movement III — Hardening
**The Line Crossed:** {answers.get('hardening_line', '[line]')}

### Movement IV — Mastery
**How Achieved:** {answers.get('mastery_method', '[method]')}

### Movement V — Surrender/Transformation
The Fire is transformed or surrendered at the Apex.

---

## Mastery Requirements

**What Mastery Requires:** {answers.get('mastery_path', '[requirements]')}
"""
    
    filepath = os.path.join(output_dir, "strand-maps", "fire-strand.md")
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath


def generate_constellation_strand(state: dict, output_dir: str) -> str:
    """Generate the Constellation Strand Map."""
    answers = state["answers"]["doc4_constellation_strand"]
    project = state["project"]
    
    content = f"""# Constellation Strand Map: {project['title']}

## Core Constellation

### The Core Bond
From Crucible Thesis.

### The Faithful
**Who:** {answers.get('faithful_companion', '[faithful]')}

### The Sacrifice
**Who Dies:** {answers.get('sacrifice_character', '[sacrifice]')}

---

## Constellation Arc by Movement

### Movement I — Formation
Core companions commit.

### Movement II — Testing
First strain on relationships.

### Movement III — Expansion & Fracture
**New Allies:** {answers.get('constellation_expansion', '[allies]')}
**The Strain:** {answers.get('betrayal_source', '[strain]')}

### Movement IV — Sacrifice & Anchor
The sacrifice occurs; core bond proves unbreakable.

### Movement V — Resolution
Constellation holds through final trial.

### Coda — New Constellation
**After the Forging:** {answers.get('constellation_fate', '[fate]')}

---

## The Bond That Saves

**Which Bond Anchors:** {answers.get('bond_that_saves', '[bond]')}
"""
    
    filepath = os.path.join(output_dir, "strand-maps", "constellation-strand.md")
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath


def generate_forge_points(state: dict, output_dir: str) -> list:
    """Generate all Forge Point documents."""
    fp_answers = state["answers"]["doc5_forge_points"]
    project = state["project"]
    filepaths = []
    
    forge_points = [
        ("fp0_ignition", "0", "Ignition", "I", "10%"),
        ("fp1_first", "1", "First Crucible", "II", "30%"),
        ("fp2_second", "2", "Second Crucible", "III", "55%"),
        ("fp3_third", "3", "Third Crucible", "IV", "75%"),
        ("apex", "Apex", "Willed Surrender", "V", "85%")
    ]
    
    for key, num, name, movement, percentage in forge_points:
        answers = fp_answers.get(key, {})
        
        content = f"""# Forge Point {num}: {name}

**Placement:** End of Movement {movement} (~{percentage})

---

## The Three Crises

### Quest Crisis
{answers.get('quest_crisis', '[quest crisis]')}

### Fire Crisis
{answers.get('fire_crisis', '[fire crisis]')}

### Constellation Crisis
{answers.get('constellation_crisis', '[constellation crisis]')}

---

## The Impossible Choice

The protagonist cannot resolve all three.

---

## The Sacrifice

**What Is Sacrificed:** {answers.get('sacrifice', '[sacrifice]')}

---

## The Aftermath

This shapes the protagonist and propels the story into the next movement.
"""
        
        filename = f"fp{num.lower().replace(' ', '-')}-{name.lower().replace(' ', '-')}.md"
        filepath = os.path.join(output_dir, "forge-points", filename)
        with open(filepath, 'w') as f:
            f.write(content)
        filepaths.append(filepath)
    
    return filepaths


def generate_dark_mirror(state: dict, output_dir: str) -> str:
    """Generate the Dark Mirror Profile."""
    answers = state["answers"]["doc6_dark_mirror"]
    project = state["project"]
    
    content = f"""# Dark Mirror Profile: {project['title']}

## The Parallel Path

**Origin Parallel:** {answers.get('origin_parallel', '[parallel]')}

---

## The Divergence Point

**The Moment:** {answers.get('divergence', '[divergence]')}

---

## The Antagonist's Truth

> "{answers.get('antagonist_want', '[philosophy]')}"

**Why It's Compelling:** The truth within their worldview.

---

## The Dark Mirror's Offer (Beat 26)

**The Offer:** {answers.get('compelling_offer', '[offer]')}
**Why It's Tempting:** {answers.get('why_tempting', '[temptation]')}
**The Hidden Cost:** {answers.get('hidden_cost', '[cost]')}

---

## The Defeat

**How They're Defeated:** {answers.get('defeat_method', '[method]')}
**The Antagonist's End:** {answers.get('antagonist_end', '[end]')}
"""
    
    filepath = os.path.join(output_dir, "dark-mirror-profile.md")
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath


def generate_constellation_bible(state: dict, output_dir: str) -> str:
    """Generate the Constellation Bible."""
    answers = state["answers"]["doc7_constellation_bible"]
    project = state["project"]
    protagonist = answers.get("protagonist", {})
    characters = answers.get("characters", [])
    
    content = f"""# Constellation Bible: {project['title']}

## The Protagonist

### Before the Forging
**Unlit State:** {protagonist.get('unlit_state', '[state]')}
**The Wound:** {protagonist.get('wound', '[wound]')}
**The Lie:** {protagonist.get('lie', '[lie]')}

### After the Forging
**Forged State:** To be determined through the story.
**The Truth:** What they learn.
**The Blade's Purpose:** From Crucible Thesis.

---

## Core Constellation

Characters and their roles in the constellation.

"""
    
    for char in characters:
        content += f"""### {char.get('name', 'Character')}
**Role:** {char.get('role', '[role]')}
**Relationship:** {char.get('relationship', '[relationship]')}

"""
    
    filepath = os.path.join(output_dir, "constellation-bible.md")
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath


def generate_mercy_ledger(state: dict, output_dir: str) -> str:
    """Generate the Mercy Ledger."""
    answers = state["answers"]["doc8_mercy_ledger"]
    project = state["project"]
    
    content = f"""# Mercy Ledger: {project['title']}

## Mercy Engine Overview

The protagonist shows mercy four times. Each costs something. Each pays off unexpectedly.

"""
    
    mercies = [
        ("mercy_1", "1", "The Seed", "II", "IV"),
        ("mercy_2", "2", "The Investment", "III", "V"),
        ("mercy_3", "3", "The Risk", "IV", "V"),
        ("mercy_4", "4", "The Impossible Gift", "V", "V (Beat 31)")
    ]
    
    for key, num, name, movement, payoff_movement in mercies:
        mercy = answers.get(key, {})
        content += f"""---

## Mercy {num}: {name}

**Movement:** {movement}
**Recipient:** {mercy.get('recipient', '[recipient]')}

**The Merciful Act:** {mercy.get('act', '[act]')}

**Immediate Cost:** {mercy.get('cost', '[cost]')}

**Later Payoff (Movement {payoff_movement}):** {mercy.get('payoff', '[payoff]')}

"""
    
    content += """---

## The Unexpected Agents (Beat 31)

At the moment of three failures, those who received mercy act to enable victory.
"""
    
    filepath = os.path.join(output_dir, "mercy-ledger.md")
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath


def generate_world_forge(state: dict, output_dir: str) -> str:
    """Generate the World Forge document."""
    answers = state["answers"]["doc9_world_forge"]
    project = state["project"]
    
    content = f"""# World Forge: {project['title']}

## The World's Wound

**The Cosmic Problem:** {answers.get('world_wound', '[wound]')}

---

## Power System

### Source
**Type:** {answers.get('power_source', '[source]')}

### Limitations
{answers.get('power_limitations', '[limitations]')}

### Previous Wielders
{answers.get('previous_wielders', '[previous wielders]')}

---

## World-Protagonist Mirror

How the world reflects the protagonist's state:
{answers.get('world_mirror', '[mirror description]')}

---

## Key Locations

{answers.get('key_locations', '[locations]')}

---

## History

**Relevant Past:** {answers.get('history', '[history]')}
"""
    
    filepath = os.path.join(output_dir, "world-forge.md")
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath


def generate_summary(state: dict, output_dir: str) -> str:
    """Generate the Crucible Summary Card."""
    project = state["project"]
    thesis = state["answers"]["doc1_crucible_thesis"]
    
    content = f"""# Crucible Summary: {project['title']}

## The Forging Question
> Can the protagonist become {thesis.get('forging_become', '[X]')} without becoming {thesis.get('dark_mirror_represents', '[Y]')}?

## Three Strands
- **Quest:** {thesis.get('burden_type', '[burden]')}
- **Fire:** {thesis.get('fire_type', '[fire]')}
- **Constellation:** {thesis.get('core_bond_type', '[bond]')}

## Four Forge Points + Apex
1. **Ignition:** Ordinary world destroyed
2. **First Crucible:** First impossible choice
3. **Second Crucible:** Trust broken
4. **Third Crucible:** Someone dies
5. **Apex:** Willed surrender

## The Mercy Engine
Four costly mercies enable victory through unexpected agents.

## Theme
> {thesis.get('theme', '[theme]')}

## The Blade's Purpose
{thesis.get('blade_purpose', '[purpose]')}

---

*Generated by Crucible Planner*
*{datetime.now().strftime('%Y-%m-%d')}*
"""
    
    filepath = os.path.join(output_dir, "crucible-summary.md")
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath


def compile_all(project_path: str) -> list:
    """Compile all documents."""
    state = load_state(project_path)
    output_dir = os.path.join(project_path, "planning")
    
    # Ensure directories exist
    os.makedirs(os.path.join(output_dir, "strand-maps"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "forge-points"), exist_ok=True)
    
    files_created = []
    
    print("📝 Generating planning documents...")
    
    files_created.append(generate_crucible_thesis(state, output_dir))
    print("   ✅ Crucible Thesis")
    
    files_created.append(generate_quest_strand(state, output_dir))
    print("   ✅ Quest Strand Map")
    
    files_created.append(generate_fire_strand(state, output_dir))
    print("   ✅ Fire Strand Map")
    
    files_created.append(generate_constellation_strand(state, output_dir))
    print("   ✅ Constellation Strand Map")
    
    files_created.extend(generate_forge_points(state, output_dir))
    print("   ✅ Forge Point Blueprints (5)")
    
    files_created.append(generate_dark_mirror(state, output_dir))
    print("   ✅ Dark Mirror Profile")
    
    files_created.append(generate_constellation_bible(state, output_dir))
    print("   ✅ Constellation Bible")
    
    files_created.append(generate_mercy_ledger(state, output_dir))
    print("   ✅ Mercy Ledger")
    
    files_created.append(generate_world_forge(state, output_dir))
    print("   ✅ World Forge")
    
    files_created.append(generate_summary(state, output_dir))
    print("   ✅ Summary Card")
    
    print(f"\n✅ Generated {len(files_created)} documents in {output_dir}")
    
    return files_created


def main():
    if len(sys.argv) < 2:
        print("Usage: python compile_documents.py <project_path>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    try:
        files = compile_all(project_path)
        print("\n📁 Files created:")
        for f in files:
            print(f"   {f}")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
