---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
argument-hint:
description: Automatically detect project state and resume from where you left off. Works across all phases.
---

# /crucible-continue

Resume your Crucible project from wherever you left off.

## CRITICAL: How to Present Options

When presenting choices to the user, you MUST use the AskUserQuestion tool.

### WRONG - Never do this:
```
Would you like to:
A) Continue planning
B) Review premise
C) Start fresh
D) Something else
```

### RIGHT - Always do this:
Use the AskUserQuestion tool with this format:
```json
{
  "questions": [
    {
      "header": "Continue",
      "question": "How would you like to proceed?",
      "options": [
        {"label": "Continue planning", "description": "Resume from current position"},
        {"label": "Review premise", "description": "Check the premise before continuing"},
        {"label": "Start fresh", "description": "Begin planning with a new premise"},
        {"label": "Something else", "description": "Do something different"}
      ],
      "multiSelect": false
    }
  ]
}
```

## Execution Steps

1. **Read state files** to determine current phase
2. **Display project status** as plain text (title, phase, progress)
3. **Use AskUserQuestion tool** to present options (NOT plain text A/B/C/D)
4. **Invoke the appropriate skill** based on user selection

## State Files to Check

- `.crucible/state/planning-state.json` - Planning progress
- `.crucible/state/outline-state.json` - Outlining progress  
- `.crucible/state/draft-state.json` - Writing progress
- `.crucible/state/edit-state.json` - Editing progress

## Phase-Specific Options

### Planning Phase
Use AskUserQuestion with these options:
- Continue planning (resume from current document/question)
- Review premise (check premise before continuing)
- Start fresh (begin with new premise)
- Something else

### Outlining Phase
Use AskUserQuestion with these options:
- Continue outlining (resume from current chapter)
- Review previous (check previous chapter first)
- See full status (view outline progress)
- Something else

### Writing Phase
Use AskUserQuestion with these options:
- Continue writing (resume from current scene)
- Review previous (check previous scene first)
- See full status (view writing progress)
- Something else

### Editing Phase
Use AskUserQuestion with these options:
- Continue editing (resume from current chapter)
- Review changes (see what has been edited)
- See full status (view editing progress)
- Something else

## Prerequisites

Requires an existing Crucible project with state files.
