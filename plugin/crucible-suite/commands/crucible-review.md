---
allowed-tools: Read, Glob, Grep, Bash, Task
argument-hint: [chapter range] | "latest"
description: Manually trigger a bi-chapter review using 5 specialized agents. Use between automatic reviews or for specific chapters.
model: sonnet
---

# /crucible-review

Trigger a manual review of your chapters using specialized review agents.

## Usage

- `/crucible-review latest` - Review most recent 2 chapters
- `/crucible-review 5-6` - Review chapters 5 and 6
- `/crucible-review 1-4` - Review chapters 1 through 4

## Execution Instructions

**IMPORTANT:** When this command is invoked, you MUST:

1. **Determine chapter range** from the argument:
   - `latest` → Read `.crucible/state/draft-state.json` to find the last 2 completed chapters
   - `X-Y` → Use chapters X through Y
   - Single number → Review that chapter only

2. **Locate the chapter files** in `.crucible/draft/chapters/` or `draft/chapters/`

3. **Launch ALL 5 review agents in parallel** using the Task tool:

```
Task(subagent_type="voice-checker", prompt="Review chapters [X-Y] located at [paths]. Load the style sample from .crucible/style/ and analyze for voice consistency. Return a structured report.")

Task(subagent_type="continuity-checker", prompt="Review chapters [X-Y] located at [paths]. Load the story bible from .crucible/story-bible/ and check for continuity errors. Return a structured report.")

Task(subagent_type="outline-checker", prompt="Review chapters [X-Y] located at [paths]. Load the chapter outlines from .crucible/outline/by-chapter/ and verify adherence. Return a structured report.")

Task(subagent_type="timeline-checker", prompt="Review chapters [X-Y] located at [paths]. Analyze chronological consistency and temporal logic. Return a structured report.")

Task(subagent_type="prose-checker", prompt="Review chapters [X-Y] located at [paths]. Analyze prose craft including pacing, show vs tell, and dialogue. Return a structured report.")
```

4. **Wait for all agents to complete** and collect their reports

5. **Compile a consolidated report** showing:
   - All critical issues (from any agent)
   - All warnings (grouped by type)
   - All suggestions
   - Overall scores from each agent

6. **Update the draft state** to record the review:
```json
{
  "last_review_at_chapter": Y,
  "last_review_timestamp": "ISO-8601 timestamp",
  "review_pending": false
}
```

## What Each Agent Does

### 1. Voice Checker (`voice-checker`)
- Analyzes voice consistency against your style sample
- Identifies tone shifts
- Checks POV adherence
- Evaluates character voice distinction

### 2. Continuity Checker (`continuity-checker`)
- Verifies character details match story bible
- Checks physical descriptions
- Validates relationship states
- Flags potential plot holes

### 3. Outline Checker (`outline-checker`)
- Verifies all planned scenes are present
- Checks beat coverage
- Identifies deviations from outline
- Notes acceptable creative changes

### 4. Timeline Checker (`timeline-checker`)
- Verifies chronological consistency
- Checks time references
- Validates travel times
- Tracks character age/state progression

### 5. Prose Checker (`prose-checker`)
- Evaluates show vs tell balance
- Identifies pacing issues
- Assesses dialogue effectiveness
- Highlights strongest passages

## Review Output

Present a consolidated report:

```
═══════════════════════════════════════
BI-CHAPTER REVIEW COMPLETE
Chapters: [X-Y]
═══════════════════════════════════════

CRITICAL ISSUES (Must Fix)
─────────────────────────────────────
[Collected from all agents]

WARNINGS (Should Fix)
─────────────────────────────────────
Voice: [issues]
Continuity: [issues]
Outline: [issues]
Timeline: [issues]
Prose: [issues]

SUGGESTIONS (Consider)
─────────────────────────────────────
[Collected from all agents]

OVERALL SCORES
─────────────────────────────────────
Voice Consistency: X/10
Continuity: X/10
Outline Fidelity: X/10
Timeline: X/10
Prose Quality: X/10
AVERAGE: X/10

NEXT STEPS
─────────────────────────────────────
A) Address critical issues now
B) Continue writing (will return to issues)
C) Show detailed report from specific agent
```

## When to Use

- When you want feedback before the automatic bi-chapter trigger
- After making significant revisions
- When something feels "off" but you can't identify it
- Before sending chapters to beta readers
- To check specific problem areas

## Prerequisites

Requires written chapters to review. Works best with:
- Style sample on file (`.crucible/style/`)
- Story bible populated (`.crucible/story-bible/`)
- Chapter outlines available (`.crucible/outline/by-chapter/`)
