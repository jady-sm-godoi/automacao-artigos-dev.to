# Implementation Plan: Telegram Bot Integration

**Branch**: `003-telegram-bot-integration` | **Date**: 2026-05-22 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/003-telegram-bot-integration/spec.md`

## Summary

Adicionar integração com Telegram ao CLI existente: um bot que recebe textos
e imagens, salva como anotações .md em /source, e responde a comandos para
gerar artigos (/gerar) e publicar no Dev.to (/publicar).

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: python-telegram-bot >=21.0, httpx (já existe)

**Storage**: File system (/source para .md, /source/imagens para imagens)

**Testing**: pytest (existente), com mocking da API do Telegram via
`python-telegram-bot`'s patching utilities

**Target Platform**: Linux server

**Project Type**: CLI tool com Telegram bot sidecar

**Performance Goals**: Resposta a comandos < 3s, download de imagem < 10s,
geração de artigo < 3min

**Constraints**: Limite de 4096 chars por mensagem Telegram, rate limiting
da API do Telegram (~30 msg/s)

**Scale/Scope**: Uso pessoal (1 bot, múltiplos usuários)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| Python line length 79 | ✅ OK | Segue padrão existente |
| Ruff lint + format | ✅ OK | task lint/task format |
| Imports stdlib→third→local | ✅ OK | Segue padrão existente |
| HTTPStatus codes | ✅ OK | Apenas comunicação com Telegram usa PTB, não raw HTTP |
| pytest tests | ✅ OK | Testes com mock da API Telegram |
| Conventional Commits | ✅ OK | Segue padrão |
| Complexity justified | ✅ OK | Nova integração horizontal: 1 novo service + 1 comando CLI |

**Post-Design Re-check**: Nenhuma violação detectada. O design adiciona 1
arquivo service e estende o CLI, sem aumentar complexidade arquitetural.

## Project Structure

### Documentation (this feature)

```text
specs/003-telegram-bot-integration/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 research
├── data-model.md        # Phase 1 data model
├── quickstart.md        # Phase 1 quickstart
├── checklists/
│   └── requirements.md  # Quality checklist
└── contracts/
    └── telegram-bot-commands.md  # Bot command contract
```

### Source Code (repository root)

```text
src/
├── main.py
├── cli.py                # + "bot" command
├── agent.py
├── config.py             # + TELEGRAM_BOT_TOKEN
├── logger.py
├── models/
│   └── artigo.py
└── services/
    ├── reader.py
    ├── generator.py
    ├── template.py
    ├── publisher.py
    └── telegram_bot.py   # NEW

tests/
├── unit/
│   ├── test_reader.py
│   ├── test_template.py
│   ├── test_generator.py
│   ├── test_publisher.py
│   └── test_telegram_bot.py   # NEW
└── integration/
    └── test_cli.py       # + "bot" command tests
```

**Structure Decision**: Single project — adiciona 1 novo service
(`telegram_bot.py`), estende `cli.py` com comando `bot`, estende
`config.py` com token. Sem módulos ou pacotes novos.

## Implementation Phases

### Phase 1: Core Bot Service

**Files**: `src/services/telegram_bot.py`, `src/config.py` (extend)

**Tasks**:
1. Adicionar `TELEGRAM_BOT_TOKEN` ao `Config` em `config.py`
2. Criar `TelegramBotService` em `telegram_bot.py`:
   - Inicialização com Application (PTB) + token
   - Handlers de texto (salva .md em /source)
   - Handler de imagem (download + salva em /source/imagens/)
   - Handler de comandos: /start, /ajuda
   - Handler de fallback para tipos não suportados
   - Validação de tamanho mínimo (100 chars)
   - Naming de arquivos: `<timestamp>-<chat_id>-<seq>`
   - Criação automática de pastas /source e /source/imagens

### Phase 2: Comandos de Geração e Publicação

**Files**: `src/services/telegram_bot.py` (extend)

**Tasks**:
1. Comando `/gerar`:
   - Executa subprocesso `artigo generate`
   - Captura saída e verifica sucesso
   - Lê artigo gerado de /artigos/
   - Envia artigo como texto (≤4000 chars) ou arquivo .md (>4000 chars)
   - Tratamento de erro (falha, timeout, sem conteúdo)
2. Comando `/publicar`:
   - Extrai nome do artigo dos args
   - Verifica flag --published
   - Executa subprocesso `artigo publish <nome> [--published]`
   - Retorna URL do artigo publicado ou erro
3. Comando `/listar`:
   - Lista arquivos .md em /source/
   - Exibe nomes e timestamps
4. Comando `/status`:
   - Contagem de .md e imagens em /source

### Phase 3: CLI Command

**Files**: `src/cli.py` (extend), `tests/`

**Tasks**:
1. Adicionar comando `artigo bot` ao CLI do Typer
2. Testes unitários para `TelegramBotService` (mockando PTB)
3. Testes de integração para o comando `artigo bot --help`
4. Testes edge cases (token ausente, conteúdo vazio, imagem inválida)

### Phase 4: Polish & QA

**Files**: Todos os novos + `pyproject.toml` (extend)

**Tasks**:
1. Adicionar `python-telegram-bot` às dependências
2. Rodar `task lint` e `task format`
3. Rodar `uv run pytest -v` — todos os testes passando
4. Teste manual com bot real no Telegram
5. Atualizar AGENTS.md com novos arquivos e comandos

## Dependencies

| Package | Version | Source | Purpose |
|---------|---------|--------|---------|
| python-telegram-bot | >=21.0 | PyPI | Telegram Bot API client |

## Test Strategy

| Test Level | File | Approach |
|------------|------|----------|
| Unit | `tests/unit/test_telegram_bot.py` | Mock PTB Application e handlers. Testar cada handler isoladamente com mensagens simuladas. |
| Unit | `tests/unit/test_config.py` (extend) | Testar carregamento de TELEGRAM_BOT_TOKEN |
| Integration | `tests/integration/test_cli.py` (extend) | Testar `artigo bot --help` e validação de token ausente |
| Manual | Telegram real | Testar fluxo completo: enviar texto → /gerar → receber artigo |

## Complexity Tracking

N/A — Nenhuma violação de constitution. Design simples: 1 novo service,
extensão de CLI existente.
