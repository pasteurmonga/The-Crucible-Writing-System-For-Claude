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

**If premise too vague:**
```
I have your core idea. To start planning:

**Who is your protagonist?**
A) A chosen one who doesn't want the role
B) An ordinary person thrust into extraordinary circumstances  
C) A powerful figure who's lost everything
D) A morally gray character seeking redemption
E) Other (describe briefly)
```

### Initialize State

```bash
python scripts/init_project.py "./crucible-project" "Title" "Premise"
```

### Confirm Scope

```
**Target novel length:**
A) Standard (100-150K words) — ~20-25 chapters
B) Epic (150-250K words) — ~25-35 chapters  
C) Extended (250K+ / series) — 35+ chapters

**Narrative complexity:**
A) Single protagonist focus
B) Dual protagonists
C) Ensemble cast (3-5 POVs)
```

## Phase 2: Document Generation

### Questioning Rules

1. **Always use multi-choice** (A/B/C/D/E)
2. **Include "Other" option** for creativity
3. **Max 2-3 questions per message**
4. **Reference previous answers** to build coherence
5. **Save state after each cluster**
6. **Verify before moving to next document**

### Question Format

```
**[DOCUMENT] — Question [X] of [Y]**

[Context from previous answers]

**[Question]**
A) [Option with brief explanation]
B) [Option]
C) [Option]
D) [Option]
E) Other (describe)
```

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

**What's next?**
A) Review and adjust any document
B) Begin chapter outline
C) Start drafting
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
