<!-- SPECKIT START -->
## Projeto: Automacao Artigos

### Descrição
CLI tool em Python que processa anotações markdown da pasta `/source` e gera
artigos formatados em estilo Medium na pasta `/artigos`, usando Agno com
GPT-4o. Também publica artigos no Dev.to via API.

### Status Atual
- [x] Especificação criada (`specs/001-artigo-blog-generator/spec.md`)
- [x] Plano implementado (`specs/001-artigo-blog-generator/plan.md`)
- [x] Tarefas definidas (`specs/001-artigo-blog-generator/tasks.md`) - 41 tarefas
- [x] Implementação: COMPLETA
- [x] Artigos gerados com sucesso (ex: `artigos/github-speckit.md`)
- [x] Publicação no Dev.to implementada (comando `publish`)
- [x] Telegram Bot (`specs/003-telegram-bot-integration/spec.md`) — IMPLEMENTADO

### Stack Tecnológica
- **Linguagem**: Python 3.11+
- **AI Agent**: Agno
- **LLM**: GPT-4o (OpenAI)
- **CLI**: Typer
- **HTTP**: httpx
- **Markdown**: python-frontmatter
- **UI Terminal**: Rich
- **Telegram Bot**: python-telegram-bot

### Estrutura do Projeto
```text
src/
├── main.py           # Entry point
├── cli.py            # Comandos CLI (generate, publish, bot)
├── agent.py          # Agente Agno
├── config.py         # Configurações
├── logger.py         # Logger estruturado
├── services/
│   ├── reader.py     # Leitor markdown
│   ├── generator.py  # Gerador artigos
│   ├── template.py   # Templates prompt
│   ├── publisher.py  # Publicação Dev.to
│   └── telegram_bot.py  # Bot Telegram
└── models/
    └── artigo.py     # Modelos dados

tests/
├── unit/
│   ├── test_reader.py
│   ├── test_template.py
│   ├── test_generator.py
│   ├── test_publisher.py
│   └── test_telegram_bot.py
└── integration/
    └── test_cli.py

source/               # Anotações entrada
source/imagens/       # Imagens via Telegram
artigos/             # Artigos gerados
templates/
└── prompt_template.md
```

### Docs

Este projeto usa GitHub Spec Kit para gerenciamento de especificações.

- *Spec principal*: specs/001-artigo-blog-generator/spec.md
- *Plano técnico*: specs/001-artigo-blog-generator/plan.md
- *Tarefas*: specs/001-artigo-blog-generator/tasks.md
- *Constitution (regras)*: .specify/memory/constitution.md

On session start: read specs/001-artigo-blog-generator/spec.md
e .specify/memory/constitution.md

### Comandos Úteis
```bash
# Instalar dependências
uv sync

# Linting
task lint

# Formatar código
task format

# Gerar artigo
artigo generate

# Publicar artigo no Dev.to (rascunho)
artigo publish <nome>

# Publicar artigo (publicado)
artigo publish <nome> --published

# Iniciar bot do Telegram
artigo bot

# Ajuda
artigo --help
```

### Convenções de Código
- Linha máxima: 79 caracteres
- Ruff para lint (`ruff check`) e format (`ruff format`)
- Imports: stdlib → third-party → local
- HTTP status codes via `HTTPStatus` (não magic numbers)
- Testes em `tests/unit/` e `tests/integration/`
- Conventional Commits (feat:/fix:/chore:/refact:)

### Testes
91 testes (unitários + integração):
```bash
uv run pytest -v
```

### Próximos Passos (da tasks.md)
1. Phase 1: Setup (T001-T009) ✅
2. Phase 2: Foundational (T010-T016) ✅
3. Phase 3: User Story 1 - Geração de Artigo (T017-T024) ✅
4. Phase 4: User Story 2 - CLI (T025-T029) ✅
5. Phase 5: User Story 3 - Estilo Medium (T030-T032) ✅
6. Phase 6: Polish & Testes (T033-T041) ✅
7. Phase 7: Publicação Dev.to (T042-T054) ✅
8. Phase 8: Telegram Bot Integration — IMPLEMENTADO ✅

### Referências
- Plano: `specs/001-artigo-blog-generator/plan.md`
- Especificação: `specs/001-artigo-blog-generator/spec.md`
- Tarefas: `specs/001-artigo-blog-generator/tasks.md`
- Constitution: `.specify/memory/constitution.md`
- API Dev.to: https://developers.forem.com/api/v1#tag/articles
- Telegram Bot: `specs/003-telegram-bot-integration/plan.md`
<!-- SPECKIT END -->
