---
description: "Task list for Telegram Bot Integration feature"
---

# Tasks: Telegram Bot Integration

**Input**: Design documents from `specs/003-telegram-bot-integration/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included per project conventions (pytest)

**Organization**: Tasks are grouped by user story to enable independent
implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [X] T055 Add python-telegram-bot >=21.0 to pyproject.toml dependencies
- [X] T056 [P] Add TELEGRAM_BOT_TOKEN to src/config.py and .env.example
- [X] T057 Create /source/imagens directory (auto-create logic)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story
can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T058 [P] Create TelegramBotService skeleton in
  src/services/telegram_bot.py with Application setup and polling loop

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Envio de Texto e Anotações (Priority: P1) 🎯 MVP

**Goal**: Usuário envia texto ao bot → salvo como .md em /source

**Independent Test**: Enviar mensagem de texto com >100 chars ao bot e
verificar arquivo .md criado em /source

### Implementation for User Story 1

- [X] T059 [P] [US1] Implement text message handler that saves content as
  .md file in src/services/telegram_bot.py
- [X] T060 [P] [US1] Implement filename generation with timestamp pattern
  `<timestamp>-<chat_id>.md` in src/services/telegram_bot.py
- [X] T061 [US1] Implement minimum length validation (100 chars) with
  rejection message in src/services/telegram_bot.py
- [X] T062 [US1] Implement /start command handler with welcome message in
  src/services/telegram_bot.py
- [X] T063 [US1] Wire up Application with token and all handlers, implement
  start_polling() entry point in src/services/telegram_bot.py
- [X] T064 [US1] Add `artigo bot` CLI command in src/cli.py that
  instantiates and starts TelegramBotService

**Checkpoint**: Bot responde a texto e /start. Arquivos .md aparecem em
/source.

---

## Phase 4: User Story 2 - Envio de Imagens (Priority: P1)

**Goal**: Usuário envia imagem ao bot → salva em /source/imagens/

**Independent Test**: Enviar imagem (jpg/png/gif/webp) ao bot e verificar
arquivo salvo em /source/imagens/

### Implementation for User Story 2

- [X] T065 [P] [US2] Implement image download handler that saves to
  /source/imagens/ in src/services/telegram_bot.py
- [X] T066 [P] [US2] Implement image format validation (jpg, png, gif,
  webp) with rejection message in src/services/telegram_bot.py
- [X] T067 [US2] Implement unsupported file type handler with clear
  rejection message in src/services/telegram_bot.py

**Checkpoint**: Bot aceita imagens e rejeita arquivos não suportados.
Arquivos em /source/imagens/.

---

## Phase 5: User Story 3 - Geração de Artigo via Bot (Priority: P1)

**Goal**: Usuário envia /gerar → bot executa geração → retorna artigo

**Independent Test**: Enviar anotações, depois /gerar, e verificar artigo
retornado no chat

### Implementation for User Story 3

- [ ] T068 [US3] Implement /gerar command handler that validates content
  exists in /source in src/services/telegram_bot.py
- [ ] T069 [US3] Implement subprocess execution of `artigo generate` and
  capture result in src/services/telegram_bot.py
- [ ] T070 [US3] Implement article reading from /artigos/ and sending as
  text (≤4000 chars) or .md file attachment (>4000 chars) in
  src/services/telegram_bot.py
- [ ] T071 [US3] Implement error handling for /gerar (no content, timeout,
  API failure) in src/services/telegram_bot.py

**Checkpoint**: /gerar retorna artigo completo no chat ou erro amigável.

---

## Phase 6: User Story 4 - Gerenciamento de Conteúdo (Priority: P2)

**Goal**: Usuário consulta conteúdo via /listar, /status, /ajuda

**Independent Test**: Enviar /listar e /status e verificar respostas
corretas com base no conteúdo de /source

### Implementation for User Story 4

- [ ] T072 [P] [US4] Implement /listar command listing .md files in /source
  in src/services/telegram_bot.py
- [ ] T073 [P] [US4] Implement /status command showing count of
  annotations and images in src/services/telegram_bot.py
- [ ] T074 [US4] Implement /ajuda command listing all available commands
  in src/services/telegram_bot.py

**Checkpoint**: Comandos de consulta funcionam e retornam informações
corretas.

---

## Phase 7: User Story 5 - Publicação Dev.to via Bot (Priority: P3)

**Goal**: Usuário envia /publicar → artigo publicado no Dev.to

**Independent Test**: Enviar /publicar com nome de artigo existente e
verificar URL de retorno

### Implementation for User Story 5

- [ ] T075 [US5] Implement /publicar command handler in
  src/services/telegram_bot.py
- [ ] T076 [US5] Implement subprocess execution of
  `artigo publish <nome> [--published]` in
  src/services/telegram_bot.py
- [ ] T077 [US5] Implement error handling for /publicar (artigo não
  encontrado, chave Dev.to ausente) in src/services/telegram_bot.py

**Checkpoint**: /publicar publica artigo no Dev.to e retorna URL.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Testes, lint, documentação

- [ ] T078 Create unit tests for all handlers in
  tests/unit/test_telegram_bot.py (mock PTB Application)
- [ ] T079 Extend CLI integration tests for `artigo bot` command in
  tests/integration/test_cli.py
- [ ] T080 [P] Run `task lint` and `task format` — fix all issues
- [ ] T081 [P] Update docs (README.md, AGENTS.md) with bot setup
  instructions
- [ ] T082 Run full test suite: `uv run pytest -v` — all tests passing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-7)**: Depend on Foundational
  - US1, US2 can proceed in parallel after Phase 2
  - US3 depends on US1 (precisa de anotações em /source)
  - US4 can proceed after US1 (opera sobre /source)
  - US5 depends on US3 (precisa de artigo gerado)
- **Polish (Phase 8)**: Depends on all desired stories complete

### User Story Dependencies

- **US1 (P1)**: No dependencies on other stories — MVP candidate
- **US2 (P1)**: No dependencies on other stories — parallel with US1
- **US3 (P1)**: Depends on US1 (conteúdo em /source) e Foundational
- **US4 (P2)**: Depends on US1 (opera sobre /source)
- **US5 (P3)**: Depends on US3 (artigo gerado)

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T056 and T057 can run in parallel
- T059 and T060 can run in parallel (US1 text + filename)
- T065 and T066 can run in parallel (US2 download + validation)
- T072 and T073 can run in parallel (US4 listar + status)
- US1 and US2 can be implemented in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all parallel tasks for User Story 1 together:
Task: "Implement text message handler in src/services/telegram_bot.py"
Task: "Implement filename generation with timestamp in src/services/telegram_bot.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 + 3)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 (text input) + Phase 4: US2 (images)
4. Complete Phase 5: US3 (generate via bot)
5. **STOP and VALIDATE**: Test fluxo completo no Telegram real
6. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 + US2 + US3 → Fluxo completo testável (MVP!)
3. Add US4 → Gerenciamento
4. Add US5 → Publicação
5. Phase 8 → Polish

### Parallel Team Strategy

- Developer A: US1 (text handler) + US4 (management commands)
- Developer B: US2 (image handler) + US5 (publication)
- Developer C: US3 (generation command) + Polish
- All depend on Phase 1+2 first

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story should be independently completable
- Commit after each task or logical group
- Avoid: vague tasks, same file conflicts, cross-story dependencies
