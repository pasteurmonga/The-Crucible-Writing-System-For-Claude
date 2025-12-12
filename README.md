# The Crucible Writing System for Claude

A complete **Claude Code plugin** for writing epic fantasy novels using the Crucible Structure—a 36-beat narrative framework with three interwoven story strands, five Forge Points, and a Mercy Engine.

## What is Crucible Suite?

Crucible Suite transforms Claude Code into a comprehensive novel-writing assistant that guides you through every phase of creating an epic fantasy novel:

| Phase | What It Does |
|-------|--------------|
| **Planning** | Interactive questionnaire generates 7 comprehensive planning documents |
| **Outlining** | Transforms planning into detailed chapter-by-chapter outlines |
| **Writing** | Scene-by-scene drafting with style matching and continuity tracking |
| **Editing** | Multi-level revision from developmental editing to final polish |

## Installation

### Step 1: Add the Marketplace

In Claude Code, run:

```
/plugin marketplace add forsonny/The-Crucible-Writing-System-For-Claude
```

### Step 2: Install the Plugin

```
/plugin install crucible-suite@crucible-writing-system
```

### Step 3: Restart Claude Code

Close and reopen Claude Code to activate the plugin.

## Quick Start

### Start a New Novel

```
/crucible-suite:crucible-plan A young blacksmith discovers she can forge weapons that steal memories. When her village is destroyed by a memory-hunting cult, she must master her forbidden gift to save the last people who remember the old ways.
```

### Continue Where You Left Off

```
/crucible-suite:crucible-continue
```

### Check Your Progress

```
/crucible-suite:crucible-status
```

## Commands

| Command | Description |
|---------|-------------|
| `/crucible-suite:crucible-plan [premise]` | Start planning with a story premise |
| `/crucible-suite:crucible-outline [book#]` | Create chapter outlines from planning docs |
| `/crucible-suite:crucible-write [chapter#]` | Draft prose scene-by-scene |
| `/crucible-suite:crucible-edit [chapter#\|all]` | Revision and editing passes |
| `/crucible-suite:crucible-status` | Show current project progress |
| `/crucible-suite:crucible-continue` | Resume from any phase |
| `/crucible-suite:crucible-review [range]` | Trigger manual quality review |
| `/crucible-suite:crucible-restore [timestamp]` | Restore from automatic backup |

## The Crucible Structure

### Three Interwoven Strands

Every great epic fantasy weaves together three narrative threads:

- **Quest Strand** — The external mission, goal, or journey
- **Fire Strand** — Internal power, curse, transformation, or moral struggle
- **Constellation Strand** — Relationships, community, found family

### Five Forge Points

Critical moments where all three strands collide with maximum dramatic impact:

1. **Ignition Forge** (~10%) — The point of no return
2. **First Crucible** (~25%) — First major test
3. **Second Crucible** (~50%) — Midpoint reversal
4. **Third Crucible** (~75%) — All seems lost
5. **Apex Willed Surrender** (~90%) — Voluntary sacrifice preceding climax

### The Mercy Engine

A unique tracking system for acts of compassion, mercy, and unexpected kindness that pay off during the climax—because in the best fantasy, what you spare comes back to save you.

## Features

- **36-Beat Framework** — Structured story beats ensure compelling pacing
- **Bi-Chapter Reviews** — Five specialized agents check your prose every 2 chapters
- **Anti-Hallucination Protocols** — Strict verification against your planning documents
- **Automatic Backups** — Never lose your work
- **Style Matching** — Captures and maintains your unique voice
- **Continuity Tracking** — Story bible automatically updated as you write

## Review Agents

Every two chapters, five specialized agents analyze your prose:

| Agent | Focus |
|-------|-------|
| `voice-checker` | Style consistency and author voice |
| `continuity-checker` | Plot and character continuity |
| `outline-checker` | Adherence to chapter outlines |
| `timeline-checker` | Chronological consistency |
| `prose-checker` | Craft-level writing feedback |

## Project Structure

When you start a Crucible project, it creates:

```
your-novel/
├── CLAUDE.md                    # Project memory for Claude
└── .crucible/
    ├── planning/                # 7 planning documents
    │   ├── crucible-thesis.md
    │   ├── strand-maps/
    │   ├── forge-points/
    │   ├── dark-mirror-profile.md
    │   ├── constellation-bible.md
    │   ├── mercy-ledger.md
    │   └── world-forge.md
    ├── outline/                 # Chapter outlines
    │   ├── master-outline.md
    │   └── by-chapter/
    ├── draft/                   # Your prose
    │   └── chapters/
    ├── story-bible/             # Continuity tracking
    ├── style/                   # Voice profile
    ├── state/                   # Session state
    └── backups/                 # Automatic backups
```

## Requirements

- **Claude Code** (latest version recommended)
- **Python 3.8+** (for automation scripts)

## Documentation

Full documentation is included in the plugin:

| Skill | Reference Topics |
|-------|------------------|
| `crucible-planner` | Structure, Dark Mirror, Forge Points, Mercy Engine |
| `crucible-outliner` | Beat mapping, narrative craft, templates |
| `crucible-writer` | Anti-hallucination, context management, prose craft |
| `crucible-editor` | Developmental, line editing, copy editing, polish |

Access via `plugin/crucible-suite/skills/[skill]/references/`

## FAQ

**Q: Can I use this for non-fantasy genres?**
A: Yes! The 36-beat structure works for any genre with strong character arcs. The terminology is fantasy-flavored, but the principles are universal.

**Q: How long should my novel be?**
A: Optimized for epic fantasy (120,000–180,000 words). The 36 beats map to ~40–50 chapters.

**Q: What if I already started writing?**
A: Use `/crucible-suite:crucible-continue` to detect your project state. You can generate planning docs retroactively.

**Q: How do reviews work?**
A: Every two chapters, five agents automatically check voice, continuity, outline adherence, timeline, and prose quality. Run `/crucible-suite:crucible-review` for manual checks.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Commands not recognized | Verify plugin installed: `/plugin` → Manage Plugins |
| Python scripts fail | Ensure Python 3.8+ is in PATH |
| Session state lost | Run `/crucible-suite:crucible-restore` to recover from backups |
| Planning seems stuck | Use `/crucible-suite:crucible-status`, then `/crucible-suite:crucible-continue` |

## Contributing

Contributions welcome!

1. **Report Issues** — [Open an issue](https://github.com/forsonny/The-Crucible-Writing-System-For-Claude/issues)
2. **Submit PRs** — Fork, make changes, submit pull request
3. **Share Feedback** — Tell us about your writing experience
4. **Star the Repo** — Help other writers discover Crucible Suite

## License

MIT License — See [LICENSE](plugin/crucible-suite/LICENSE) for details.

## Links

- [Full Plugin Documentation](plugin/crucible-suite/README.md)
- [Changelog](plugin/crucible-suite/CHANGELOG.md)
- [Report Issues](https://github.com/forsonny/The-Crucible-Writing-System-For-Claude/issues)

---

**Built for fantasy writers who want to tell bigger stories.**

*Crucible Suite v1.0.1*
