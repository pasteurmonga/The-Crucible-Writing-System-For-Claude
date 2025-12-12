# Changelog

All notable changes to the Crucible Suite plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-11

### Added

#### Skills
- **crucible-planner** - Interactive planning system with 7 document generation
- **crucible-outliner** - Chapter-by-chapter outline generator
- **crucible-writer** - Scene-by-scene prose drafting with style matching
- **crucible-editor** - Multi-level revision and editing workflow

#### Commands
- `/crucible-plan` - Start or continue planning with premise
- `/crucible-outline` - Generate chapter outlines from planning
- `/crucible-write` - Draft prose from outlines
- `/crucible-edit` - Revision and editing workflows
- `/crucible-status` - Show comprehensive project status
- `/crucible-continue` - Auto-detect and resume from any phase
- `/crucible-review` - Manual bi-chapter review trigger
- `/crucible-restore` - Restore from backups

#### Agents
- **voice-checker** - Voice and style consistency analysis
- **continuity-checker** - Plot and character continuity tracking
- **outline-checker** - Outline fidelity verification
- **timeline-checker** - Chronological consistency analysis
- **prose-checker** - Craft-level feedback

#### Hooks
- **SessionStart** - Automatic project context loading
- **PostToolUse** - Incremental backup on Write/Edit
- **Stop** - Quality gate for bi-chapter reviews
- **SubagentStop** - Review agent completion verification

#### Rules
- `fantasy-writing.md` - Genre conventions and prose guidelines
- `crucible-structure.md` - 36-beat framework rules
- `anti-hallucination.md` - Verification protocols

#### Templates
- `CLAUDE.md` - Project memory template
- Project structure scaffolding

#### Scripts
- `backup_project.py` - Full project backup
- `backup_on_change.py` - Incremental backup
- `detect_project.py` - Project state detection
- `status_reporter.py` - Status report generation
- `load_project_context.py` - Session context injection
- `cross_platform.py` - Shared utilities

### Technical Details
- All SKILL.md files under 500 lines with progressive disclosure
- Cross-platform Python 3.8+ scripts
- JSON-based state management
- Automatic backup with 20-backup retention

## [1.0.1] - 2025-12-11

### Fixed

#### Hook Configuration
- Fixed hook timeouts from milliseconds to seconds (hooks use seconds, not ms)
- Removed invalid `matcher` field from SessionStart hook (matchers only valid for PreToolUse/PermissionRequest/PostToolUse)
- Updated prompt hooks with correct JSON response format requirement
- Added missing `hooks` reference to plugin.json

#### Python 3.8 Compatibility
- Fixed `is_relative_to()` usage in backup_on_change.py (method only exists in Python 3.9+)
- Changed to try/except pattern with `relative_to()` for broader compatibility

#### Code Quality
- Removed duplicate `load_draft()` function from init_draft.py
- Fixed unreachable code in update_draft_state.py (`const=-1` → `const=0`)
- Removed unused imports across multiple scripts
- Added error handling for file operations in save_draft.py and diff_report.py

#### Skill/Agent Configuration
- Removed invalid `allowed-tools` field from all SKILL.md files (not valid for skills per docs)
- Added `skills` field to all 5 review agent frontmatter

#### Command Integration
- Added explicit "Execution Instructions" sections to all 8 commands
- Commands now properly invoke their corresponding skills via Task tool

### Added

#### Scripts
- `load_draft.py` - Resume writing sessions from saved state (was missing)
- `update_draft_state.py` - Chapter tracking and bi-chapter review trigger

#### Features
- Bi-chapter review system in crucible-writer skill
- Chapter tracking for automatic review triggers every 2 chapters

#### Utilities
- `find_crucible_project()` function in cross_platform.py
- `extract_title_from_claude_md()` utility in cross_platform.py

### Changed
- Updated README.md with correct GitHub repository URL
- Enhanced backup_on_change.py path detection for Crucible files

## [Unreleased]

### Planned
- Enhanced series support for multi-book projects
- Export to common writing software formats
- Integration with external writing tools
- Custom beat structure modifications
