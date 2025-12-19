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
- `/crucible-suite:crucible-plan` - Start or continue planning with premise
- `/crucible-suite:crucible-outline` - Generate chapter outlines from planning
- `/crucible-suite:crucible-write` - Draft prose from outlines
- `/crucible-suite:crucible-edit` - Revision and editing workflows
- `/crucible-suite:crucible-status` - Show comprehensive project status
- `/crucible-suite:crucible-continue` - Auto-detect and resume from any phase
- `/crucible-suite:crucible-review` - Manual bi-chapter review trigger
- `/crucible-suite:crucible-restore` - Restore from backups

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

## [1.0.2] - 2025-12-14

### Added

#### Answer Persistence System
- Full context storage for planning answers (question + answer + description)
- CLI interface for `save_state.py` with 5 parameters:
  - `--answer <document> <key> <question> <answer> <description>`
  - `--progress <doc_num> <question_num>`
  - `--complete <doc_num>`
  - `--scope <length> <complexity>`
- New `question-key-mapping.md` reference file with all 75 question-to-state-key mappings
- Answer Persistence Workflow section in crucible-planner SKILL.md
- Resuming Planning section in crucible-continue.md with saved answer display

#### Backward Compatibility
- `get_answer()` helper function in `compile_documents.py` handles both old (string) and new (dict) answer formats

### Changed
- Planning answers now stored as objects with full context instead of plain strings
- `/crucible-continue` now displays previously saved answers when resuming planning sessions

### Fixed
- Session recovery now preserves full question context, not just answer values
- Planning progress can be properly resumed after session failures

## [1.0.3] - 2025-12-14

### Added

#### Version Tracking
- Added `VERSION` file for simple version tracking
- Added `bump_version.py` script for version management:
  - `python bump_version.py patch` - 1.0.3 -> 1.0.4
  - `python bump_version.py minor` - 1.0.3 -> 1.1.0
  - `python bump_version.py major` - 1.0.3 -> 2.0.0
- Script updates both VERSION file and plugin.json

### Improved

#### Status Report Formatting
- Redesigned `format_report_text()` with clean ASCII box layout
- Added visual progress bars `[####----]` for each phase
- Added status icons: `[x]` complete, `[>]` in progress, `[ ]` pending
- Organized sections with clear headers (PLANNING, OUTLINE, WRITING, EDITING, BACKUP)
- Cross-platform ASCII characters (works on Windows cmd/PowerShell)

### Fixed

#### Project Detection Bug
- Fixed `status_reporter.py` and `detect_project.py` failing to find planner-created projects
- Root cause: Scripts looked for `.crucible/` directory but `init_project.py` creates `state.json` at project root
- Updated `find_crucible_project()` to detect both structures:
  - `dotcrucible`: Legacy `.crucible/` directory structure
  - `rootlevel`: `state.json` at project root (planner-created)

#### Status Reporter
- Fixed document completion detection to match state.json format (string keys like `"doc1_crucible_thesis"`)
- Fixed phase detection to recognize in-progress planning (checks `current_document` field)
- Updated path resolution for planning, outline, draft, and backup directories based on structure type

#### Detect Project
- Same structure detection improvements as status_reporter.py
- Planning progress now correctly reads from `state.json` for rootlevel projects
- File-based fallback detection for outline and draft directories

### Changed
- Both detection scripts now return structure type alongside project root
- Status report includes `structure_type` field in output

## [1.0.4] - 2025-12-14

### Fixed

#### Hook System Overhaul
- **Stop hook**: Changed from prompt-based to command-based
  - Prompt hooks cannot access file system, making review checks impossible
  - New `check_stop_conditions.py` script reads `draft-state.json` directly
  - Properly blocks session end when bi-chapter review is due
  - Prevents infinite loops via `stop_hook_active` check

- **SubagentStop hook**: Removed entirely
  - Prompt hooks cannot access agent output or file system
  - Was non-functional for validating review agent completeness

#### Hook Behavior
- Stop hook now correctly enforces bi-chapter reviews
- Exit code 2 with descriptive stderr message tells Claude exactly what to do
- Session cannot end until required reviews are completed

### Added

#### Scripts
- `check_stop_conditions.py` - Stop hook enforcement script
  - Reads project state from `.crucible/state/draft-state.json`
  - Checks `chapters_complete` vs `last_review_at_chapter`
  - Returns exit code 2 with action instructions when blocked
  - Returns exit code 0 when session can safely end

#### Enhanced Backup Script
- `backup_on_change.py` now includes chapter detection and review reminders:
  - `is_chapter_file()` - Detects chapter files by name patterns
  - `check_review_status()` - Checks if bi-chapter review is due
  - Outputs `hookSpecificOutput.additionalContext` as soft reminder
  - Claude receives context about pending reviews after chapter edits

### Changed

#### Hook Configuration
- SessionStart timeout increased from 10s to 15s for larger projects
- Stop hook now uses command type instead of prompt type
- Removed SubagentStop hook from configuration
- Updated description to reflect "review enforcement" purpose

### Technical Details
- All hooks now use command-based approach for file system access
- PostToolUse provides soft reminders via `additionalContext`
- Stop hook provides hard enforcement via exit code 2
- Hybrid approach: gentle nudges + strict gates

## [1.0.5] - 2025-12-18

### Fixed

#### Hook Output Compliance
- **backup_on_change.py**: Now outputs only `hookSpecificOutput` per official Claude Code hooks specification
  - Removed non-spec fields (`success`, `action`, `backup_result`)
  - Empty `{}` output when no context needed
  - `hookSpecificOutput.additionalContext` only when review reminder is required

#### Model Specification
- Updated model shorthand `haiku` to full model ID `claude-haiku-4-20250514` in 4 files:
  - `commands/crucible-restore.md`
  - `commands/crucible-status.md`
  - `agents/timeline-checker.md`
  - `agents/outline-checker.md`

#### Windows Compatibility
- **safe_write_json()**: Fixed atomicity issue on Windows
  - Added fallback delete-then-move pattern when `Path.replace()` fails
  - Temp file cleanup on error

#### Error Handling
- **backup_on_change.py**: Added comprehensive OSError handling
  - Handles stdin read errors alongside JSON decode errors
  - Graceful handling of filesystem errors during project detection
  - Cleanup block now handles permission errors and file-in-use scenarios

### Changed

#### Path Encoding for Incremental Backups
- **backup_on_change.py**: Now uses base64url encoding for backup filenames
  - Replaces ambiguous underscore-based path flattening
  - Reversible encoding allows exact path reconstruction
  - Example: `draft/chapter-1.md` → `ZHJhZnQvY2hhcHRlci0xLm1k`

- **restore_project.py**: Backward-compatible path decoding
  - Tries base64url decode first (new format)
  - Falls back to underscore heuristics (legacy format)
  - Existing backups remain fully restorable

### Added

#### Shared Utilities
- **cross_platform.py**: New path encoding functions
  - `encode_path_b64(path)` - URL-safe base64 encoding
  - `decode_path_b64(encoded)` - Decode with padding restoration
  - `is_base64_encoded_path(s)` - Format detection for backward compatibility

### Technical Details
- All hook outputs now comply with official `hooks.md` specification
- Base64url encoding uses Python's `base64.urlsafe_b64encode/decode`
- Backward compatibility maintained for all existing incremental backups
- Cross-platform tested on Windows and Unix-like systems

## [1.0.10] - 2025-12-19

### Fixed

#### Model Specification
- Fixed invalid model ID in `crucible-status.md` and `crucible-restore.md`
  - Changed from non-existent `claude-haiku-4-20250514` to valid `claude-haiku-4-5-20251001`
  - Commands were failing with 404 API errors due to invalid model reference

#### Hook Configuration
- Temporarily disabled hooks to resolve plugin cache version mismatch
  - Hooks were referencing stale cached paths after version updates
  - Requires Claude Code restart to properly reload plugin configuration
  - Re-enable hooks after restart by restoring hooks.json content

### Changed

#### Plugin Installation Path
- Updated installed_plugins.json to point to source directory for local development
  - Allows immediate testing of plugin changes without cache rebuild

## [1.0.9] - 2025-12-19

### Added

#### Project Metadata Updates
- Added `--set` argument to `save_state.py` for updating project metadata
  - `--set title "Title"` - Update project title
  - `--set premise "Premise"` - Update project premise
  - Supports multiple `--set` flags in a single call
  - Also works for scope fields: target_length, complexity, chapters
- Example: `python save_state.py ./project --set title "New Title" --set premise "New premise"`

## [1.0.8] - 2025-12-19

### Fixed

#### Scope Answer Handling
- `save_state.py` now handles "scope" as a special document key
  - Previously failed with `KeyError: 'scope'` when skill saved scope answers via `--answer`
  - Scope answers now correctly stored in `state["scope"]` instead of `state["answers"]["scope"]`
  - Added key mapping for variations: `novel_length` -> `target_length`, `narrative_complexity` -> `complexity`
  - Automatically calculates chapter count when target_length is set

## [1.0.7] - 2025-12-19

### Fixed

#### Windows Console Encoding
- Replaced all emoji characters with ASCII equivalents in Python scripts
  - `✅` → `[OK]`
  - `❌` → `[ERROR]`
  - `✓` → `[x]` or `+`
- Windows cmd/PowerShell cannot encode Unicode emoji (charmap codec error)
- Affected 15+ scripts across planner, outliner, writer, and migration tools
- All console output now uses safe ASCII characters

### Changed
- All print statements now Windows-compatible without encoding workarounds

## [1.0.6] - 2025-12-18

### Added

#### New Scripts
- `draft_utils.py` - Shared draft utilities
- `extract_invented_markers.py` - Extract invention markers from prose
- `validate_before_write.py` - Pre-write validation
- `restore_backup.py` / `restore_project.py` - Backup restoration utilities

#### Story Bible Commands
- `story-bible-commands.md` reference for Writer skill

#### Bi-Chapter Review Reference
- `bi-chapter-review.md` documentation for review process

### Changed
- Enhanced cross_platform.py with additional project detection methods
- Updated hook configurations for better reliability
- Improved backup directory handling for different project structures

## [Unreleased]

### Planned
- Enhanced series support for multi-book projects
- Export to common writing software formats
- Integration with external writing tools
- Custom beat structure modifications
