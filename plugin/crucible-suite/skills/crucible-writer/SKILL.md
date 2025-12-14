---
name: crucible-writer
# prettier-ignore
description: First-draft writing assistant for Crucible-planned novels. Use when author has completed planning (crucible-planner) and outlining (crucible-outliner) and wants to write the actual prose. Handles scene-by-scene drafting, style matching, continuity tracking, and hallucination prevention. Triggers on "write my novel," "draft chapter X," "start writing from my outline," "help me write my book," or when user has Crucible outline and wants prose output. Works with any Crucible-planned story.
---

# Crucible Writer

Transform Crucible outlines into first-draft prose while maintaining style consistency, plot fidelity, and narrative quality.

## Critical Principles

**Context Window is Limited.** Never try to hold the entire novel in context. Load only what's needed for the current scene. Save constantly.

**The Outline is Law.** Never invent plot points, characters, or events not in the outline. If something seems missing, ASK the author—don't improvise.

**Style is Sacred.** Capture the author's voice early. Maintain it relentlessly. When in doubt, match the sample.

**Save Everything.** After every scene, update the story bible and save the draft. Progress must survive session breaks.

## Before Starting

**Read these references based on the writing phase:**
- `references/context-management.md` — Critical: Managing limited AI context
- `references/writing-process.md` — Scene-by-scene drafting approach
- `references/style-capture.md` — Learning and maintaining author voice
- `references/anti-hallucination.md` — Verification protocols
- `references/prose-craft.md` — Genre conventions and techniques

## Questioning Rules

1. **ALWAYS use AskUserQuestion tool** for all user questions (provides interactive UI)
2. **Max 4 options per question** (tool limit) + "Other" is automatic
3. **Max 4 questions per AskUserQuestion call**
4. **Reference user's story elements** by name (characters, places, etc.)
5. **Save state after every scene and chapter**

**CRITICAL: Use the AskUserQuestion tool, NOT plain text A/B/C options.**

## Required Inputs

Before writing can begin, gather:

1. **Complete Chapter Outline** (required) — The crucible-outliner output
2. **Crucible Summary Card** (required) — Quick reference for theme, characters
3. **Style Sample** (required) — 2,000+ words of author's existing prose OR detailed style preferences
4. **Constellation Bible** (as needed) — Character details
5. **World Forge** (as needed) — Setting details

## Workflow Overview

```
Phase 1: PROJECT SETUP
         ↓
Phase 2: STYLE CAPTURE
         ↓
Phase 3: CHAPTER WRITING (repeat for each chapter)
         │
         ├─→ Load Context
         ├─→ Write Scene-by-Scene  
         ├─→ Verify Against Outline
         ├─→ Update Story Bible
         └─→ Save Progress
         ↓
Phase 4: COMPILE MANUSCRIPT
```

---

## Phase 1: Project Setup

### Initialize the Draft Project

```bash
python scripts/init_draft.py "./draft-project" "Book Title" --chapters 28 --target-words 150000
```

### Request Essential Documents

```
To begin writing, I need:

1. **Your complete chapter outline** (from crucible-outliner)
2. **The Crucible Summary Card** (for quick reference)
3. **A style sample** — either:
   - 2,000+ words of your previous writing, OR
   - Detailed description of your desired prose style

Please upload or paste these now.
```

### Confirm Writing Parameters

Present the extracted parameters, then use AskUserQuestion:
```
**Writing Parameters:**

Target words per chapter: [calculated from total ÷ chapters]
POV style: [First/Third Limited/Third Omniscient/Multiple]
Tense: [Past/Present]
Genre conventions to follow: [Cultivation fantasy / Epic fantasy / etc.]
Pacing preference: [Dense/Balanced/Breezy]
```

```json
{
  "questions": [
    {
      "header": "Parameters",
      "question": "Do these writing parameters look correct?",
      "options": [
        {"label": "Confirm settings", "description": "Proceed with these parameters"},
        {"label": "Adjust settings", "description": "Modify one or more parameters"}
      ],
      "multiSelect": false
    }
  ]
}
```

---

## Phase 2: Style Capture

**CRITICAL:** Read `references/style-capture.md` before this phase.

### Analyze the Style Sample

Extract and document:

```
**STYLE PROFILE**

Sentence Structure:
- Average length: [Short/Medium/Long/Varied]
- Complexity: [Simple/Compound/Complex/Mixed]
- Rhythm pattern: [Staccato/Flowing/Varied]

Vocabulary:
- Register: [Formal/Informal/Mixed]
- Density: [Sparse/Rich/Purple]
- Unusual word frequency: [Low/Medium/High]

Dialogue:
- Tag style: [Minimal/Standard/Elaborate]
- Dialect/Voice distinction: [Strong/Moderate/Subtle]
- Subtext usage: [Heavy/Moderate/Light]

Description:
- Sensory focus: [Visual/Auditory/Tactile/Mixed]
- Metaphor density: [Sparse/Moderate/Rich]
- Setting integration: [Separate blocks/Woven in]

Interiority:
- Internal monologue: [Rare/Occasional/Frequent]
- Emotional showing vs. telling: [Show-heavy/Balanced/Tell-heavy]

Pacing:
- Scene transitions: [Abrupt/Smooth/Varied]
- White space usage: [Dense paragraphs/Frequent breaks]

**SIGNATURE ELEMENTS:**
[List 3-5 distinctive features of this author's voice]
```

### Confirm Style Profile

Present the style profile and sample, then use AskUserQuestion:
```
Based on your sample, here's your style profile:

[Show extracted profile]

**Sample of how I'll write in this style:**

[Write 200-word sample matching the style]
```

```json
{
  "questions": [
    {
      "header": "Style",
      "question": "Does this capture your writing voice?",
      "options": [
        {"label": "Captures my voice", "description": "Proceed with this style profile"},
        {"label": "Needs adjustment", "description": "Specify what's off about the style"},
        {"label": "Show another sample", "description": "See a different example in this style"}
      ],
      "multiSelect": false
    }
  ]
}
```

---

## Phase 3: Chapter Writing

### Pre-Chapter Context Loading

**For each chapter, load ONLY:**

1. **Current chapter outline** (from the full outline)
2. **Previous chapter summary** (from story bible—NOT full text)
3. **Active character states** (from story bible)
4. **Relevant foreshadowing** (plants that pay off OR are planted this chapter)
5. **Style profile** (from Phase 2)

**Do NOT load:**
- Full text of previous chapters (too large)
- Chapters not adjacent to current
- Planning documents not directly relevant

### Scene-by-Scene Writing

Each chapter contains multiple scenes. Write ONE SCENE AT A TIME:

```
**WRITING: Chapter [X], Scene [Y]**

From outline:
- Goal: [scene goal]
- Conflict: [what opposes]
- Turn: [how it shifts]
- Key moments: [listed]
- Plants/Payoffs: [listed]

Writing this scene now...
```

**After each scene:**
1. Show word count
2. Ask if author wants to review before continuing
3. Option to revise before moving on

### Scene Writing Protocol

For each scene, follow this sequence:

1. **State what you're writing** (goal, conflict, turn)
2. **Write the prose** (matching style profile)
3. **Verify against outline** (all required elements present?)
4. **Note any plants/payoffs** executed
5. **Update running word count**

### Chapter Completion

After all scenes in a chapter:

```
**Chapter [X] Complete**

Word count: [X,XXX]
Target: [X,XXX]
Status: [Under/On target/Over]

**Outline Verification:**
- [✓] All required scenes written
- [✓] All key moments included
- [✓] All plants executed
- [✓] All payoffs resolved (for this chapter)
- [✓] Chapter turn achieved
- [✓] Ending hook present

**Continuity Check:**
- [✓] Character states consistent
- [✓] Timeline consistent
- [✓] No new elements invented
```

Use AskUserQuestion for chapter approval:
```json
{
  "questions": [
    {
      "header": "Chapter",
      "question": "How would you like to proceed with this chapter?",
      "options": [
        {"label": "Approve & save", "description": "Save chapter and continue to next"},
        {"label": "Review scene", "description": "Look at a specific scene in detail"},
        {"label": "Revise", "description": "Make changes before saving"}
      ],
      "multiSelect": false
    }
  ]
}
```

### Update Story Bible

After each chapter, run:

```bash
python scripts/update_story_bible.py "./draft-project" --chapter X
```

The story bible tracks:
- Chapter-by-chapter summaries
- Character locations/states at each chapter end
- Established facts (names, places, rules)
- Foreshadowing planted (awaiting payoff)
- Foreshadowing paid off
- Timeline progression
- Word counts
- **Completed chapter count** (for bi-chapter review tracking)

---

## Bi-Chapter Review System

**CRITICAL:** Every 2 chapters, a comprehensive review MUST be triggered to catch issues early.

### Chapter Tracking

After completing each chapter, update the draft state:

```bash
python scripts/update_draft_state.py "./draft-project" --chapter-complete X
```

The draft state file (`.crucible/state/draft-state.json`) tracks:
```json
{
  "chapters_complete": 6,
  "last_review_at_chapter": 4,
  "review_pending": true,
  "current_chapter": 7,
  "current_scene": 1
}
```

### Review Trigger Logic

**After completing each chapter, check:**

```
chapters_since_last_review = chapters_complete - last_review_at_chapter

IF chapters_since_last_review >= 2:
    TRIGGER bi-chapter review
    UPDATE last_review_at_chapter = chapters_complete
```

### Triggering the Review

When a bi-chapter review is needed, present:

```
═══════════════════════════════════════
BI-CHAPTER REVIEW REQUIRED
═══════════════════════════════════════

You've completed chapters [X] and [Y].
Time for a quality check before continuing.

This review runs 5 specialized agents:
• voice-checker — Style consistency
• continuity-checker — Plot/character continuity
• outline-checker — Outline fidelity
• timeline-checker — Chronological consistency
• prose-checker — Craft-level feedback
```

Use AskUserQuestion:
```json
{
  "questions": [
    {
      "header": "Review",
      "question": "How would you like to proceed with the bi-chapter review?",
      "options": [
        {"label": "Run full review (Recommended)", "description": "Run all 5 review agents now"},
        {"label": "Skip for now", "description": "Continue writing without review (not recommended)"},
        {"label": "Selective review", "description": "Choose which agents to run"}
      ],
      "multiSelect": false
    }
  ]
}
```

### Invoking Review Agents

**IMPORTANT:** To invoke the review agents, use the Task tool with subagent_type for each agent:

```
Task(subagent_type="voice-checker", prompt="Review chapters X-Y for voice consistency...")
Task(subagent_type="continuity-checker", prompt="Review chapters X-Y for continuity...")
Task(subagent_type="outline-checker", prompt="Review chapters X-Y for outline adherence...")
Task(subagent_type="timeline-checker", prompt="Review chapters X-Y for timeline consistency...")
Task(subagent_type="prose-checker", prompt="Review chapters X-Y for prose quality...")
```

Launch all 5 agents in parallel for efficiency. Each agent will return a structured report.

### After Review

After all agents complete:

1. **Compile findings** from all 5 reports
2. **Categorize by severity** (Critical/Warning/Suggestion)
3. **Present consolidated report** to author
4. **Update state** with `last_review_at_chapter`
5. **Address critical issues** before continuing

```
═══════════════════════════════════════
BI-CHAPTER REVIEW COMPLETE
Chapters: [X-Y]
═══════════════════════════════════════

CRITICAL ISSUES (Must Fix Before Continuing)
─────────────────────────────────────
[Issues from all agents that require immediate attention]

WARNINGS (Should Address Soon)
─────────────────────────────────────
[Issues to fix during this session or next]

SUGGESTIONS (Consider Later)
─────────────────────────────────────
[Nice-to-haves for polishing]

OVERALL SCORES
─────────────────────────────────────
Voice Consistency: X/10
Continuity: X/10
Outline Fidelity: X/10
Timeline: X/10
Prose Quality: X/10
```

Use AskUserQuestion:
```json
{
  "questions": [
    {
      "header": "Review Action",
      "question": "How would you like to proceed after this review?",
      "options": [
        {"label": "Address issues now", "description": "Fix critical issues before continuing"},
        {"label": "Continue writing", "description": "Note issues and continue (will return later)"},
        {"label": "Show detailed reports", "description": "View full reports from each agent"}
      ],
      "multiSelect": false
    }
  ]
}
```

---

## Phase 4: Compile Manuscript

After all chapters complete:

```bash
python scripts/compile_manuscript.py "./draft-project"
```

Creates:
```
manuscript/
├── full-manuscript.md       # Complete draft
├── full-manuscript.docx     # Word format
├── chapter-word-counts.md   # Statistics
└── continuity-report.md     # Potential issues flagged
```

---

## Hallucination Prevention Protocol

**CRITICAL:** Read `references/anti-hallucination.md` for full protocol.

### The Three Laws

1. **If it's not in the outline, don't write it.** Missing a scene? Ask the author.
2. **If you're unsure about a detail, ask.** Don't guess character names, places, rules.
3. **If you need to invent minor details, flag them.** Mark with [INVENTED] for author review.

### Verification Checkpoints

**Before writing each scene:**
- Do I have the scene outline loaded?
- Do I know the required elements?
- Are there unknowns I need to ask about?

**After writing each scene:**
- Did I include all required elements?
- Did I invent anything significant?
- Does this match what came before?

**Before saving each chapter:**
- Full outline verification
- Continuity check against story bible
- Flag any [INVENTED] details for author

---

## Continuing a Paused Session

When returning to a draft:

```
**Loading Draft: [Title]**

Last saved: [timestamp]
Chapters complete: [X of Y]
Current chapter: [X], Scene [Y]
Total words: [X,XXX]

Loading story bible and style profile...

Ready to continue.
```

Use AskUserQuestion:
```json
{
  "questions": [
    {
      "header": "Resume",
      "question": "How would you like to continue?",
      "options": [
        {"label": "Resume writing", "description": "Continue from Scene [Y] of Chapter [X]"},
        {"label": "Review current", "description": "Review what was written in current chapter"},
        {"label": "Jump to chapter", "description": "Go to a different chapter"},
        {"label": "Show story bible", "description": "View current story bible state"}
      ],
      "multiSelect": false
    }
  ]
}
```

---

## Handling Author Feedback

When author requests changes:

**Scene-level revision:**
```
Revising Chapter [X], Scene [Y]...
[Show original]
[Show revision]
Confirm replacement? (Y/N)
```

**Style adjustment:**
```
Adjusting style profile...
[Show what's changing]
[Write sample in adjusted style]
Confirm adjustment? (Y/N)
```

**Plot deviation (author wants to change outline):**

When the author wants to deviate from the outline, use AskUserQuestion:
```json
{
  "questions": [
    {
      "header": "Deviation",
      "question": "This differs from the outline. How would you like to proceed?",
      "options": [
        {"label": "Update outline (Recommended)", "description": "Modify outline to match—keeps all docs in sync"},
        {"label": "Proceed without update", "description": "Continue but may cause continuity issues later"},
        {"label": "Discuss first", "description": "Talk through the implications before deciding"}
      ],
      "multiSelect": false
    }
  ]
}
```

---

## Word Count Management

Target words per chapter = Total target ÷ Number of chapters

**If running short:**
- Expand sensory details
- Add interiority/reflection
- Lengthen dialogue exchanges
- Add transitional beats

**If running long:**
- Tighten dialogue
- Reduce description density
- Cut redundant beats
- Trust the reader more

**Per-scene targets:**
- Action scenes: 1,500-2,500 words
- Dialogue scenes: 1,000-2,000 words
- Reflection scenes: 800-1,500 words
- Transitional scenes: 500-1,000 words

---

## Multi-Book Series Handling

When writing Book 2+:

1. **Load previous book's story bible** (not full manuscript)
2. **Request updated character states** from author
3. **Note unresolved foreshadowing** to track
4. **Request series-level outline** for cross-book threads

---

## Emergency Context Recovery

If session breaks unexpectedly:

1. Run `python scripts/load_draft.py "./draft-project"`
2. Review story bible for current state
3. Re-load style profile
4. Resume from last saved scene

**All progress is preserved in:**
- `draft/chapters/` — Written prose
- `story-bible.json` — State tracking
- `style-profile.json` — Voice settings
