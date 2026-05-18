<!-- SPECKIT START -->
## Projeto: Automacao Artigos

### Descrição
CLI tool em Python que processa anotações markdown da pasta `/source` e gera artigos formatados em estilo Medium na pasta `/artigos`, usando Agno com GPT-4o.

### Status Atual
- [x] Especificação criada (`specs/001-artigo-blog-generator/spec.md`)
- [x] Plano implementado (`specs/001-artigo-blog-generator/plan.md`)
- [x] Tarefas definidas (`specs/001-artigo-blog-generator/tasks.md`) - 41 tarefas
- [ ] Implementação: NÃO INICIADA

### Stack Tecnológica
- **Linguagem**: Python 3.11+
- **AI Agent**: Agno
- **LLM**: GPT-4o (OpenAI)
- **CLI**: Typer
- **Markdown**: python-frontmatter
- **UI Terminal**: Rich

### Estrutura do Projeto
```text
src/
├── main.py           # Entry point
├── cli.py            # Comandos CLI
├── agent.py          # Agente Agno
├── config.py         # Configurações
├── services/
│   ├── reader.py     # Leitor markdown
│   ├── generator.py  # Gerador artigos
│   └── template.py   # Templates prompt
└── models/
    └── artigo.py     # Modelos dados

tests/
├── unit/
└── integration/

source/               # Anotações entrada
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

On session start: read specs/001-artigo-blog-generator/spec.md e .specify/memory/constitution.md

### Comandos Úteis
```bash
# Instalar dependências
uv sync

# Linting
task lint

# Formatar código
task format

# Gerar artigo
python -m main generate

# Ajudar
python -m main generate --help
```

### Convenções de Código
- Linha máxima: 79 caracteres
- Ruff para lint (`ruff check`) e format (`ruff format`)
- Imports: stdlib → third-party → local
- Testes em `tests/unit/` e `tests/integration/`
- Conventional Commits (feat:/fix:/chore:/refact:)

### Próximos Passos (da tasks.md)
1. Phase 1: Setup (T001-T009)
2. Phase 2: Foundational (T010-T016) - BLOQUEIA user stories
3. Phase 3: User Story 1 - Geração de Artigo (T017-T024)

### Referências
- Plano: `specs/001-artigo-blog-generator/plan.md`
- Especificação: `specs/001-artigo-blog-generator/spec.md`
- Tarefas: `specs/001-artigo-blog-generator/tasks.md`
- Constitution: `.specify/memory/constitution.md`
<!-- SPECKIT END -->