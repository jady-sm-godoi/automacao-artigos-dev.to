# Automacao Artigos Constitution

## Core Principles

### I. Python Code Quality

**Formatting & Style**
- Maximum line length: 79 characters
- Use `# noqa: E501` only after exhausting line breaks
- Leave one blank line at end of Python files
- Ruff for linting: `ruff check` (flags E501, PLR2004)
- Ruff for formatting: `ruff format`

**Commands**
- `task lint`: Verify code with `ruff check`
- `task format`: Fix auto-fixable issues + format (`ruff check --fix && ruff format .`)
- Run `task lint` before committing

**Imports**
- All imports at top of file
- Order: stdlib → third-party → local
- Inline imports allowed only when no cyclic dependency and conditional use

**Magic Numbers**
- Magic numbers (>2) in comparisons: suppress with `# noqa: PLR2004` or extract constant
- Use `HTTPStatus` for HTTP status codes (not magic numbers)

### II. Testing Standards

**File Naming**: `tests_<app>__<type>.py` (e.g., `tests_event__models.py`)

**Layout**: `src/tests/<app>/` — one subfolder per app

**Test Style**
- Use `@pytest.mark.parametrize` for parameterized tests
- Use `HTTPStatus` constants for assertions
- Magic numbers in asserts: suppress with `# noqa: PLR2004` or extract constant

**Markers**: `slow`, `events`

**Timeouts**: 90-180s for large test suites

### III. Git Workflow

**Commits**
- Format: Conventional Commits (Add:/Fix:/Chore:/Refact:/Feat:)
- Subject ≤50 characters (guideline, ~80% adherence)
- Body only if necessary

**Branches**: `dev`, `hml`, `main` — active branches

## Code Quality Gates

- `task lint` MUST pass before committing
- `task format` MUST run before committing (includes lint fix + format)
- Ruff rules enforced: E501 (line length), PLR2004 (magic numbers)
- Check specific rules: `ruff check --select E501,PLR2004 <file>`

## Governance

**Compliance**
- All PRs/reviews must verify adherence to these principles
- Complexity must be justified in implementation plans

**Amendments**
- Constitution supersedes all other practices
- Amendments require documentation of changes
- Version must increment per semantic versioning

**Versioning Policy**
- MAJOR: Backward incompatible governance/principle removals or redefinitions
- MINOR: New principle/section added or materially expanded guidance
- PATCH: Clarifications, wording, typo fixes, non-semantic refinements

**Version**: 1.0.0 | **Ratified**: 2026-04-29 | **Last Amended**: 2026-04-29