# Crucible Suite

A complete writing system for epic fantasy novels using the Crucible Structure—a 36-beat narrative framework with three interwoven story strands.

## Overview

Crucible Suite guides authors through the complete novel-writing process:

1. **Planning** - Interactive questionnaire generates 7 comprehensive planning documents
2. **Outlining** - Transform planning documents into detailed chapter-by-chapter outlines
3. **Writing** - Scene-by-scene drafting with style matching and anti-hallucination protocols
4. **Editing** - Multi-level revision from developmental editing to final polish

## Features

- **36-Beat Narrative Framework** - Structured story beats ensure compelling pacing
- **Three Interwoven Strands** - Quest (external), Fire (internal), Constellation (relationships)
- **Five Forge Points** - Critical convergence moments where all strands collide
- **Mercy Engine** - Track acts of mercy that pay off in the climax
- **Bi-Chapter Reviews** - Automated quality checks every 2 chapters
- **Anti-Hallucination Protocols** - Strict verification against planning documents
- **Automatic Backups** - Never lose your work

## Installation

### From GitHub (Recommended)

```bash
# Add the marketplace
/plugin marketplace add https://github.com/forsonny/The-Crucible-Writing-System-For-Claude.git

# Install the plugin
/plugin install crucible-suite@crucible-writing-system

# Restart Claude Code to activate
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/forsonny/The-Crucible-Writing-System-For-Claude.git
   ```
2. Add as local marketplace:
   ```bash
   /plugin marketplace add ./The-Crucible-Writing-System-For-Claude
   ```
3. Install:
   ```bash
   /plugin install crucible-suite@crucible-writing-system
   ```
4. Restart Claude Code

## Quick Start

### Start a New Project

```
/crucible-suite:crucible-plan [your premise]
```

Example:
```
/crucible-suite:crucible-plan A young blacksmith discovers she can forge weapons that steal memories. When her village is destroyed by a memory-hunting cult, she must master her forbidden gift to save the last people who remember the old ways.
```

### Continue Where You Left Off

```
/crucible-suite:crucible-continue
```

### Check Project Status

```
/crucible-suite:crucible-status
```

## Commands

| Command | Description |
|---------|-------------|
| `/crucible-suite:crucible-plan [premise]` | Start planning with a premise |
| `/crucible-suite:crucible-outline [book#]` | Create chapter outlines |
| `/crucible-suite:crucible-write [chapter#]` | Draft prose scene-by-scene |
| `/crucible-suite:crucible-edit [chapter#\|all]` | Revision and editing |
| `/crucible-suite:crucible-status` | Show project progress |
| `/crucible-suite:crucible-continue` | Resume from any phase |
| `/crucible-suite:crucible-review [range]` | Trigger manual review |
| `/crucible-suite:crucible-restore [timestamp]` | Restore from backup |

## The Crucible Structure

### Three Strands

- **Quest Strand** - The external mission or goal
- **Fire Strand** - Internal power, curse, or transformation
- **Constellation Strand** - Relationships and community

### Five Movements

1. **Ignition** (Beats 1-6) - Setup and catalyst
2. **First Tempering** (Beats 7-14) - Rising complications
3. **Scattering** (Beats 15-22) - Midpoint crisis
4. **Brightest Burning** (Beats 23-28) - Dark night
5. **Final Forging** (Beats 29-34) - Climax and resolution

### Forge Points

Critical moments where all three strands collide:

1. **Ignition Forge Point** (~10%)
2. **First Crucible** (~25%)
3. **Second Crucible** (~50%)
4. **Third Crucible** (~75%)
5. **Apex Willed Surrender** (~90%)

## Review Agents

Five specialized agents analyze your prose during bi-chapter reviews:

| Agent | Focus |
|-------|-------|
| **voice-checker** | Style and voice consistency |
| **continuity-checker** | Plot and character continuity |
| **outline-checker** | Adherence to chapter outlines |
| **timeline-checker** | Chronological consistency |
| **prose-checker** | Craft-level feedback |

## Project Structure

When you start a Crucible project, it creates:

```
your-project/
├── CLAUDE.md                    # Project memory
├── story-bible.json             # Continuity tracking (JSON)
├── style-profile.json           # Author voice profile
├── outline/                     # Chapter outlines
│   ├── master-outline.md
│   ├── chapter-summaries.md
│   ├── scene-breakdown.md
│   ├── foreshadowing-tracker.md
│   ├── character-threads.md
│   └── by-chapter/
├── planning/                    # Planning documents
│   ├── crucible-thesis.md
│   ├── strand-maps/
│   ├── forge-points/
│   ├── dark-mirror-profile.md
│   ├── constellation-bible.md
│   ├── mercy-ledger.md
│   └── world-forge.md
├── draft/                       # Written prose
│   └── chapters/
├── manuscript/                  # Compiled output
└── .crucible/
    ├── state/                   # Session state files
    │   ├── planning-state.json
    │   ├── outline-state.json
    │   ├── draft-state.json
    │   └── edit-state.json
    └── backups/                 # Automatic backups
```

## Requirements

- Claude Code
- Python 3.8+ (for automation scripts)

---

## Documentation

Crucible Suite includes extensive reference documentation within each skill:

| Skill | Reference Files |
|-------|-----------------|
| **crucible-planner** | `crucible-structure.md`, `dark-mirror-guide.md`, `forge-point-rules.md`, `mercy-engine-guide.md`, `question-sequences.md` |
| **crucible-outliner** | `beat-to-chapter-mapping.md`, `narrative-craft.md`, `outline-templates.md` |
| **crucible-writer** | `anti-hallucination.md`, `context-management.md`, `prose-craft.md`, `style-capture.md`, `writing-process.md` |
| **crucible-editor** | `copy-editing-standards.md`, `developmental-checklist.md`, `line-editing-guide.md`, `polish-techniques.md` |

Access these via the `skills/[skill-name]/references/` directories.

## FAQ

**Q: Can I use Crucible Suite for non-fantasy genres?**
A: The 36-beat structure works well for any genre with strong character arcs. The terminology is fantasy-flavored, but the underlying principles—external goal, internal transformation, relationship dynamics—are universal.

**Q: How long should my novel be?**
A: Crucible Suite is optimized for epic fantasy (120,000-180,000 words). The 36 beats map to approximately 40-50 chapters at 3,000-4,000 words each.

**Q: Can I modify the beat structure?**
A: The planning documents you generate are fully editable. Adjust beat placement, merge beats, or split them as needed for your story.

**Q: What if I already have a partial draft?**
A: Use `/crucible-suite:crucible-continue` to detect your project state. You can generate planning documents retroactively or start outlining from any point.

**Q: How do bi-chapter reviews work?**
A: Every two chapters, the system automatically runs five review agents (voice, continuity, outline, timeline, prose) to catch issues early. You can also trigger reviews manually with `/crucible-suite:crucible-review`.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Commands not recognized** | Ensure plugin is installed: check `~/.claude/plugins/crucible-suite/` exists |
| **Python scripts fail** | Verify Python 3.8+ is installed and in PATH |
| **Session state lost** | Run `/crucible-suite:crucible-restore` to recover from automatic backups |
| **Review agents timeout** | Large chapters may need more time; break into smaller scenes |
| **Planning seems stuck** | Use `/crucible-suite:crucible-status` to check progress, `/crucible-suite:crucible-continue` to resume |

## Contributing

Contributions are welcome! Here's how to help:

1. **Report Issues** - Found a bug or have a feature request? [Open an issue](https://github.com/forsonny/The-Crucible-Writing-System-For-Claude/issues)
2. **Submit PRs** - Fork the repo, make changes, and submit a pull request
3. **Share Feedback** - Tell us about your writing experience with Crucible Suite
4. **Spread the Word** - Star the repo and share with other fantasy writers

### Development Setup

```bash
# Clone the repository
git clone https://github.com/forsonny/The-Crucible-Writing-System-For-Claude.git

# Navigate to plugin directory
cd The-Crucible-Writing-System-For-Claude

# Test scripts
python scripts/detect_project.py
```

## License

MIT License - See [LICENSE](LICENSE) for details.

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/forsonny/The-Crucible-Writing-System-For-Claude/issues)
- **Documentation**: Reference files in `skills/*/references/` directories
- **Changelog**: See [CHANGELOG.md](CHANGELOG.md) for version history

## Acknowledgments

- **Crucible Structure Framework** - The 36-beat narrative structure at the heart of this system
- **Claude Code Plugin System** - Built on Anthropic's extensible plugin architecture
- **The Fantasy Writing Community** - For inspiration and feedback on narrative frameworks

## Credits

**Crucible Suite** was created to make epic fantasy novel writing more structured and achievable. The system combines:

- A proven 36-beat narrative framework designed specifically for epic fantasy
- Three interwoven story strands (Quest, Fire, Constellation) that create narrative depth
- The Mercy Engine concept—acts of compassion that pay off in the climax
- Five Forge Points where all elements converge for maximum dramatic impact

Built with ❤️ for fantasy writers who want to tell bigger stories.

---

*Version 1.0.16 • [Changelog](CHANGELOG.md) • [License](LICENSE)*
