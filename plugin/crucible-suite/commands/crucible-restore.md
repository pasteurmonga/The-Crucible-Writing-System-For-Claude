---
allowed-tools: Read, Write, Glob, Bash
argument-hint: [timestamp] | "latest"
description: Restore your project from a backup. Lists available backups and allows selective restoration.
model: haiku
---

# /crucible-restore

Restore your Crucible project from a previous backup.

## Usage

- `/crucible-restore` - List available backups
- `/crucible-restore latest` - Restore from most recent backup
- `/crucible-restore 2024-01-15-1432` - Restore from specific timestamp

## What This Does

1. Lists all available backups with timestamps
2. Shows what changed since each backup
3. Allows selective or full restoration
4. Creates a pre-restore backup (safety net)

## Backup Types

### Automatic Backups
Created automatically when you:
- Complete a chapter
- Finish a planning document
- Complete a bi-chapter review
- Use Write or Edit tools on project files

### Manual Backups
Can be triggered anytime with the backup script.

## Restoration Options

When restoring, you can choose:

### Full Restore
Restores entire project to backup state:
- All chapters
- Planning documents
- Story bible
- State files

### Selective Restore
Restore specific components:
- Single chapter
- Planning documents only
- Story bible only
- State files only

## Example

```
/crucible-restore

Available Backups for "The Memory Forge"
═══════════════════════════════════════

1. 2024-01-15-1432 (2 hours ago)
   └─ Chapter 11 partial, 63,450 words

2. 2024-01-15-1030 (6 hours ago)
   └─ Chapter 10 complete, 60,200 words

3. 2024-01-14-2145 (yesterday)
   └─ Chapter 10 partial, 58,100 words

4. 2024-01-14-1500 (yesterday)
   └─ Bi-chapter review complete (Ch 8-9)

Select backup to restore:
A) Backup 1 (latest)
B) Backup 2
C) Backup 3
D) Backup 4
E) Enter specific timestamp
```

## Safety Features

- **Pre-restore backup**: Current state is always saved before restoration
- **Confirmation required**: Shows exactly what will change
- **Selective restore**: Can restore just what you need
- **Undo restore**: Can restore the pre-restore backup if needed

## When to Use

- After a session went wrong
- When you prefer an earlier version
- After accidental deletions
- To recover from corruption
- To compare with previous versions
