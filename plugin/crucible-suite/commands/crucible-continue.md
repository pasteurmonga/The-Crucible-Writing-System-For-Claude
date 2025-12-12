---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
argument-hint:
description: Automatically detect project state and resume from where you left off. Works across all phases.
model: sonnet
---

# /crucible-continue

Resume your Crucible project from wherever you left off.

## Execution Instructions

**IMPORTANT:** When this command is invoked, you MUST:

1. **Read state files** to determine current phase:
   - Check `.crucible/state/planning-state.json` for planning progress
   - Check `.crucible/state/outline-state.json` for outlining progress
   - Check `.crucible/state/draft-state.json` for writing progress
   - Check `.crucible/state/edit-state.json` for editing progress

2. **Determine the active phase** based on which state file has incomplete work

3. **Invoke the appropriate skill**:
   - If planning incomplete → Follow `crucible-planner` skill
   - If outlining incomplete → Follow `crucible-outliner` skill
   - If writing incomplete → Follow `crucible-writer` skill
   - If editing incomplete → Follow `crucible-editor` skill

4. **Check for pending bi-chapter reviews** in `draft-state.json`:
   - If `review_pending: true`, trigger the review before continuing

## Usage

- `/crucible-suite:crucible-continue` - Auto-detect and resume

## What This Does

1. Scans your project for Crucible state files
2. Determines the current phase and progress
3. Loads relevant context for that phase
4. Offers to continue from the exact stopping point

## Auto-Detection Logic

The command checks for:

### Planning Phase
- Looks for `.crucible/state/planning-state.json`
- Identifies which document was in progress
- Resumes questioning sequence

### Outlining Phase
- Looks for `.crucible/state/outline-state.json`
- Identifies which chapter was being outlined
- Resumes from that chapter

### Writing Phase
- Looks for `.crucible/state/draft-state.json`
- Identifies current chapter and scene
- Loads story bible and style profile
- Resumes scene-by-scene writing

### Editing Phase
- Looks for `.crucible/state/edit-state.json`
- Identifies which chapter and editing level
- Resumes editing workflow

## Example

```
/crucible-suite:crucible-continue

Detecting Crucible project state...

Found: The Memory Forge
Current Phase: WRITING
Progress: Chapter 11, Scene 2 of 4

Last session ended: 2024-01-15 14:32
Word count: 63,450

Ready to continue writing Chapter 11, Scene 2:
"The Forge of Memories"

A) Continue from Scene 2
B) Review Scene 1 first
C) See full chapter status
D) Do something else
```

## When to Use

- At the start of any writing session
- When you're not sure where you left off
- After a break of any length
- When switching between devices

## Prerequisites

Requires an existing Crucible project with state files. If no project is found, you'll be prompted to start with `/crucible-suite:crucible-plan`.
