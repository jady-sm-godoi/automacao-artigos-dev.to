# Implementation Plan: Artigo Blog Generator

**Branch**: `001-artigo-blog-generator` | **Date**: 2026-04-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-artigo-blog-generator/spec.md`

## Summary

CLI tool em Python que processa anotações markdown da pasta `/source` e gera artigos formatados em estilo Medium na pasta `/artigos`, usando Agno com GPT-4o. Sistema com template configurável para personalização do prompt do agente.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Agno (AI agents), OpenAI SDK (GPT-4o), Click or Typer (CLI)

**Storage**: Filesystem (pastas `source/` e `artigos/`)

**Testing**: pytest

**Target Platform**: Linux/multi-platform (CLI)

**Project Type**: CLI tool

**Performance Goals**: Geração de artigo em menos de 2 minutos

**Constraints**: Requer API key OpenAI configurada via variável de ambiente

**Scale/Scope**: 1 usuário por vez, processa arquivos markdown locais

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Python Code Quality | ✅ PASS | Ruff para lint/format, 79 chars, imports organizados |
| II. Testing Standards | ✅ PASS | pytest, markers, parametrização |
| III. Git Workflow | ✅ PASS | Conventional Commits, branches dev/main/hml |

## Project Structure

### Documentation (this feature)

```text
specs/001-artigo-blog-generator/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI contracts)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py              # Entry point com CLI
├── cli.py               # Comandos CLI (generate)
├── agent.py             # Agente Agno
├── services/
│   ├── __init__.py
│   ├── reader.py       # Leitor de arquivos markdown
│   ├── generator.py    # Gerador de artigos
│   └── template.py     # Gerenciador de templates
├── models/
│   ├── __init__.py
│   └── artigo.py        # Modelos de dados
└── config.py            # Configurações

tests/
├── unit/
│   ├── test_reader.py
│   ├── test_generator.py
│   └── test_template.py
└── integration/
    └── test_cli.py

source/                  # Anotações de entrada (criado automaticamente)
artigos/                 # Artigos gerados (criado automaticamente)
templates/
└── prompt_template.md  # Template do prompt Agno

pyproject.toml
```

**Structure Decision**: Single project structure com módulos organizados em `src/`, seguindo convenções Python. CLI principal em `main.py`, comandos em `cli.py`, lógica de negócio em `services/`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | - | - |

## Notes

- Agno agent usa GPT-4o para geração do artigo
- Template de prompt em `templates/prompt_template.md`
- Diretórios `source/` e `artigos/` criados automaticamente se não existirem