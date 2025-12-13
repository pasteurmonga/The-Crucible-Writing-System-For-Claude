---
name: crucible-planner
# prettier-ignore
description: Interactive planning system for epic fantasy novels using the Crucible Structure—a 36-beat narrative framework with three interwoven story strands (Quest, Fire, Constellation), four Forge Points, and a Mercy Engine. Use when user wants to plan a fantasy novel, provides a story premise/synopsis, asks to "plan my fantasy book," wants to create planning documents for an epic fantasy, or mentions the Crucible Structure. Guides users through multi-choice questions to generate 7 comprehensive planning documents from a simple premise.
---

# Crucible Planner

Interactive planning system for epic fantasy novels using the Crucible Structure.

## Overview

Starting from a simple premise, guide users through multi-choice questions to build seven interconnected planning documents:

1. **Crucible Thesis** — philosophical core
2. **Strand Maps** — Quest, Fire, Constellation (3 separate maps)
3. **Forge Point Blueprints** — five convergence crises
4. **Dark Mirror Profile** — antagonist design
5. **Constellation Bible** — character relationships
6. **Mercy Ledger** — mercy/payoff tracking
7. **World Forge** — world-building

## Before Starting

**Always read these references:**
- `references/crucible-structure.md` (the 36-beat structure)
- `references/question-sequences.md` (complete question flows)

## Workflow

```
Phase 1: INTAKE → Accept premise, initialize state, confirm scope
Phase 2: QUESTIONING → 9 document cycles with multi-choice questions
Phase 3: COMPILATION → Generate documents, present package
```

## Phase 1: Intake

### Accept Premise

Extract from user input:
- Core concept (1-2 sentences)
- Protagonist sketch
- Central conflict hint

**If premise too vague**, use AskUserQuestion:
```json
{
  "questions": [
    {
      "header": "Protagonist",
      "question": "Who is your protagonist?",
      "options": [
        {"label": "Reluctant chosen one", "description": "A chosen one who doesn't want the role"},
        {"label": "Ordinary person", "description": "Thrust into extraordinary circumstances"},
        {"label": "Fallen powerful", "description": "A powerful figure who's lost everything"},
        {"label": "Seeking redemption", "description": "A morally gray character seeking redemption"}
      ],
      "multiSelect": false
    }
  ]
}
```

### Initialize State

```bash
python scripts/init_project.py "./crucible-project" "Title" "Premise"
```

### Confirm Scope

Use AskUserQuestion for scope confirmation:
```json
{
  "questions": [
    {
      "header": "Length",
      "question": "What's your target novel length?",
      "options": [
        {"label": "Standard (100-150K)", "description": "~20-25 chapters"},
        {"label": "Epic (150-250K)", "description": "~25-35 chapters"},
        {"label": "Extended (250K+)", "description": "35+ chapters or series"}
      ],
      "multiSelect": false
    },
    {
      "header": "POV",
      "question": "What's your narrative complexity?",
      "options": [
        {"label": "Single protagonist", "description": "One main POV character"},
        {"label": "Dual protagonists", "description": "Two main POV characters"},
        {"label": "Ensemble cast", "description": "3-5 POV characters"}
      ],
      "multiSelect": false
    }
  ]
}
```

## Phase 2: Document Generation

### Questioning Rules

1. **ALWAYS use AskUserQuestion tool** for all questions (provides interactive UI)
2. **Max 4 options per question** (tool limit) + "Other" is automatic
3. **Max 4 questions per AskUserQuestion call**
4. **Reference previous answers** to build coherence
5. **Save state after each cluster**
6. **Verify before moving to next document**

### Question Format

**CRITICAL: Use the AskUserQuestion tool, NOT plain text options.**

Example AskUserQuestion call:
```json
{
  "questions": [
    {
      "header": "Burden",
      "question": "What form does the external burden take in your story?",
      "options": [
        {"label": "Physical object", "description": "An artifact that must be destroyed or protected"},
        {"label": "Person to save", "description": "Someone who must be rescued or kept alive"},
        {"label": "Knowledge/truth", "description": "Information that must be revealed or protected"},
        {"label": "Mission/quest", "description": "A task that must be completed"}
      ],
      "multiSelect": false
    }
  ]
}
```

**Header examples** (max 12 chars): "Burden", "Fire Type", "Bond", "Antagonist", "Theme", "Sacrifice"

**For verification questions**, use multiSelect: true to allow checking multiple items.

### Document Sequence

See `references/question-sequences.md` for complete question banks.

**Document 1: Crucible Thesis (10 questions)**
- The Burden (external mission)
- The Fire (internal power/curse)
- Core Constellation Bond
- Dark Mirror Connection
- Forging Question
- Antagonist's Truth
- The Surrender
- Theme
- Blade's Purpose
- Verification

**Document 2: Quest Strand Map (7 questions)**
- Burden's Origin
- Why This Protagonist
- Antagonist's Stake
- Quest Escalation
- Impossible Requirement
- Resolution Method
- Verification

**Document 3: Fire Strand Map (7 questions)**
- Fire Manifestation
- The Danger
- Cost of Use
- Mastery Path
- Hardening Phase
- Mastery Moment
- Verification

**Document 4: Constellation Strand Map (7 questions)**
- Faithful Companion
- The Sacrifice
- Betrayal Source
- Expansion
- Bond That Saves
- Constellation Fate
- Verification

**Document 5: Forge Point Blueprints (5 × 4 questions)**
For each Forge Point (Ignition, First, Second, Third, Apex):
- Quest Crisis
- Fire Crisis  
- Constellation Crisis
- What is Sacrificed

**Document 6: Dark Mirror Profile (9 questions)**
- Origin Parallel
- The Divergence
- Antagonist's Want
- Compelling Offer
- Why Tempting
- Hidden Cost
- Defeat Method
- Antagonist's End
- Verification

**Document 7: Constellation Bible (12 questions)**
- Protagonist Profile
- Faithful Companion details
- Core Bond Character details
- Mentor/Catalyst
- Sacrifice Character
- Additional cast
- Verification

**Document 8: Mercy Ledger (4 × 4 questions)**
For each of 4 mercies:
- Recipient
- Merciful Act
- Immediate Cost
- Later Payoff

**Document 9: World Forge (9 questions)**
- World's Wound
- Power System Source
- Power Limitations
- Previous Wielders
- Key Locations
- World-Protagonist Mirror
- Magic Rules
- Timeline Framework
- Verification

## Phase 3: Compilation

### Generate Documents

```bash
python scripts/compile_documents.py "./crucible-project"
```

Creates:
```
planning/
├── crucible-thesis.md
├── strand-maps/
│   ├── quest-strand.md
│   ├── fire-strand.md
│   └── constellation-strand.md
├── forge-points/
│   ├── fp0-ignition.md
│   ├── fp1-first-crucible.md
│   ├── fp2-second-crucible.md
│   ├── fp3-third-crucible.md
│   └── apex-willed-surrender.md
├── dark-mirror-profile.md
├── constellation-bible.md
├── mercy-ledger.md
├── world-forge.md
└── crucible-summary.md
```

### Present to User

```
✅ **Crucible Planning Complete!**

📄 [View Crucible Thesis](computer:///path/planning/crucible-thesis.md)
📄 [View Strand Maps](computer:///path/planning/strand-maps/)
📄 [View Forge Points](computer:///path/planning/forge-points/)
📄 [View Dark Mirror Profile](computer:///path/planning/dark-mirror-profile.md)
📄 [View Constellation Bible](computer:///path/planning/constellation-bible.md)
📄 [View Mercy Ledger](computer:///path/planning/mercy-ledger.md)
📄 [View World Forge](computer:///path/planning/world-forge.md)
📋 [View Quick Reference](computer:///path/planning/crucible-summary.md)

Then use AskUserQuestion for next steps:
```json
{
  "questions": [
    {
      "header": "Next Step",
      "question": "What would you like to do next?",
      "options": [
        {"label": "Review documents", "description": "Review and adjust any planning document"},
        {"label": "Begin outlining", "description": "Start creating chapter outlines"},
        {"label": "Start drafting", "description": "Jump straight into writing prose"}
      ],
      "multiSelect": false
    }
  ]
}
```

## State Management

Save after every question cluster:
```bash
python scripts/save_state.py "./crucible-project"
```

Resume interrupted session:
```bash
python scripts/load_state.py "./crucible-project"
```

## Bundled Resources

### references/
- `crucible-structure.md` — Complete 36-beat structure
- `question-sequences.md` — Full question bank by document
- `forge-point-rules.md` — Strand convergence mechanics
- `dark-mirror-guide.md` — Antagonist design
- `mercy-engine-guide.md` — Mercy/payoff mechanics

### assets/templates/
- Document templates for generation

### scripts/
- `init_project.py` — Initialize project
- `save_state.py` — Save progress
- `load_state.py` — Load progress
- `compile_documents.py` — Generate all documents
