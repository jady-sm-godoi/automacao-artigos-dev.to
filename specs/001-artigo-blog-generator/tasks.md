---

description: "Task list for artigo blog generator"

---

# Tasks: Artigo Blog Generator

**Input**: Design documents from `specs/001-artigo-blog-generator/`

**Prerequisites**: plan.md, spec.md

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (US1, US2, US3)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create src/ directory structure
- [x] T002 [P] Create src/__init__.py
- [x] T003 [P] Create src/services/__init__.py
- [x] T004 [P] Create src/models/__init__.py
- [x] T005 [P] Create tests/unit/__init__.py and tests/integration/__init__.py
- [x] T006 [P] Create templates/ directory
- [x] T007 Configure pyproject.toml with dependencies (agno, typer, python-frontmatter, rich)
- [x] T008 Create .python-version if not exists
- [x] T009 Run `uv sync` to install dependencies

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T010 Create src/config.py with Config dataclass (source_dir, output_dir, template_path, modelo, verbose)
- [x] T011 Create src/models/artigo.py with Anotacao and Artigo dataclasses
- [x] T012 Create templates/prompt_template.md with placeholders {{conteudo}}, {{titulo}}, {{tags}}
- [x] T013 Create src/services/template.py (load and render template)
- [x] T014 Create src/services/reader.py (read markdown files with frontmatter support)
- [x] T015 [P] Create src/agent.py with Agno Agent using GPT-4o
- [x] T016 Create src/services/generator.py (orchestrates reader + agent + writer)

---

## Phase 3: User Story 1 - Geração de Artigo (Priority: P1)

**Goal**: Transform markdown annotations from `/source` into Medium-style articles in `/artigos`

**Independent Test**: Run `python -m main generate` with sample .md files and verify output in `/artigos`

- [x] T017 [US1] Create src/cli.py with Typer app and `generate` command
- [x] T018 [US1] Implement directory validation (create if not exists, notify user)
- [x] T019 [US1] Implement multi-file processing (read all .md from source recursively)
- [x] T020 [US1] Implement article generation with Agno agent
- [x] T021 [US1] Implement output file naming (use title, add counter if exists)
- [x] T022 [US1] Implement frontmatter metadata extraction and inclusion in output
- [x] T023 [US1] Create src/main.py as entry point with `__main__`
- [x] T024 [US1] Test generation end-to-end with sample annotations

**Checkpoint**: User can run `python -m main generate` and get a Medium-style article

---

## Phase 4: User Story 2 - Interface de Linha de Comando (Priority: P2)

**Goal**: CLI with help, progress feedback, and default paths

**Independent Test**: Run `python -m main generate --help` and verify output

- [x] T025 [P] [US2] Add `--help` support with Typer documentation
- [x] T026 [P] [US2] Add progress output with rich (reading files, processing, saving)
- [x] T027 [P] [US2] Add default paths when no arguments provided
- [x] T028 [P] [US2] Add `--source`, `--output`, `--template`, `--verbose` CLI options
- [x] T029 [US2] Test CLI help and argument parsing

**Checkpoint**: CLI is user-friendly and provides clear feedback

---

## Phase 5: User Story 3 - Estilo Medium (Priority: P3)

**Goal**: Generated article follows Medium visual style

**Independent Test**: Generate article and verify markdown formatting

- [x] T030 [P] [US3] Refine prompt_template.md for Medium style (paragraphs, structure, tone)
- [x] T031 [P] [US3] Ensure markdown formatting preserved (headings, lists, bold, code blocks)
- [x] T032 [US3] Test with various annotation formats (basic, code, quotes)

**Checkpoint**: Articles are professional and readable in Medium style

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T033 [P] Error handling for API failures (retry logic, user-friendly messages)
- [X] T034 [P] Add logging for debugging
- [X] T035 [P] Handle edge cases (empty files, short content, non-md files)
- [X] T036 Create tests for src/services/reader.py
- [X] T037 Create tests for src/services/template.py
- [X] T038 Create tests for src/services/generator.py
- [X] T039 Create integration test for CLI (test_cli.py)
- [X] T040 Run `uv run ruff check .` and `uv run ruff format .` to ensure code quality
- [X] T041 Update quickstart.md if needed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 and US2 can proceed in parallel after Foundational
  - US3 can proceed in parallel with US1/US2
- **Polish (Phase 6)**: Depends on all user stories being complete

### Within Each User Story

- Core implementation before edge cases
- Integration before testing
- Story complete before moving to next priority

---

## Parallel Opportunities

### Setup Phase (T001-T009)
- T002, T003, T004, T005, T006 can run in parallel (creating empty files/dirs)
- T007, T008 can run in parallel (configuration files)

### Foundational Phase (T010-T016)
- T011 (models) can run parallel with T010 (config)
- T013, T014, T015, T016 all depend on T010-T012 but T013-T015 can overlap
- T015 (agent) and T016 (generator) depend on T013 and T014

### User Story 2 (T025-T029)
- T025, T026, T027, T028 can run in parallel (different CLI features)

### User Story 3 (T030-T032)
- T030 and T031 can run in parallel (template refinement and formatting)
- T032 depends on both

### Polish Phase (T033-T041)
- T033, T034, T035 can run in parallel (error handling, logging, edge cases)
- Unit tests (T036-T038) can run in parallel
- T039 (integration) depends on T017-T028 complete
- T040 can run anytime after code is written

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (core generation)
4. **STOP and VALIDATE**: Test `python -m main generate` works
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 → Test independently → MVP ready
3. Add US2 → Test independently → Better UX
4. Add US3 → Test independently → Polish complete
5. Polish → Final touches

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each phase or logical group
- Stop at any checkpoint to validate independently
- Run `task lint` and `task format` before committing