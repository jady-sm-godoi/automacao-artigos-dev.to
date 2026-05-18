# 🤖 Automacao Artigos

**CLI tool em Python** que transforma anotações Markdown em artigos formatados
no estilo Medium usando IA (GPT-4o via Agno).

```
anotações.md  →  [Agno + GPT-4o]  →  artigo-medium.md
```

---

## Sumário

- [Para Usuários](#para-usuarios)
  - [Instalação](#instalacao)
  - [Uso](#uso)
  - [Formato das Anotações](#formato-das-anotacoes)
  - [Personalização](#personalizacao)
  - [Exemplo](#exemplo)
- [Para Programadores](#para-programadores)
  - [Arquitetura](#arquitetura)
  - [Stack](#stack)
  - [Estrutura do Projeto](#estrutura-do-projeto)
  - [Setup Dev](#setup-dev)
  - [Comandos](#comandos)
  - [Testes](#testes)
  - [Convenções](#convencoes)

---

## Para Usuários

### Instalação

**Pré-requisitos**: Python 3.11+ e [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo-url>
cd automacao_artigos
uv sync
```

Configure a chave da OpenAI:

```bash
export OPENAI_API_KEY="sk-..."
# Ou crie um arquivo .env na raiz do projeto
```

### Uso

```bash
# Gera artigo a partir da pasta source/
artigo

# Com verbose (mostra mais detalhes)
artigo --verbose

# Pastas personalizadas
artigo --source ./minhas-notas --output ./meus-artigos

# Ajuda
artigo --help
```

### Formato das Anotações

Coloque arquivos `.md` na pasta `source/`. O sistema lê todos
recursivamente (subpastas inclusas).

**Básico** (só conteúdo):

```markdown
# Ideias sobre Python

- Async/await melhora legibilidade
- Type hints reduzem bugs
```

**Com metadados** (frontmatter YAML):

```markdown
---
title: "Python Avançado"
tags: [python, tutorial, dev]
---

Conteúdo aqui...
```

> **Nota**: Anotações com menos de 100 caracteres são ignoradas.
> Arquivos vazios e não-`.md` também.

### Personalização

Edite `templates/prompt_template.md` para alterar o prompt do agente.
Variáveis disponíveis:

| Variável | Descrição |
|----------|-----------|
| `{{titulo}}` | Título extraído das anotações |
| `{{tags}}` | Tags combinadas |
| `{{conteudo}}` | Conteúdo bruto das anotações |

### Exemplo

```
source/
├── python.md          →  artigos/
├── async.md               └── dominando-python-assincrono.md
└── ferramentas/
    └── ruff.md
```

---

## Para Programadores

### Arquitetura

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  CLI      │───▶│  Reader  │───▶│Generator │───▶│  Artigo  │
│ (Typer)   │    │(Markdown)│    │(Agno+IA) │    │  .md     │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                      │                              ▲
                      ▼                              │
                 Anotações                      Template
                 .md source/                    prompt.md
```

**Fluxo**:

1. `cli.py` recebe comando `generate` e monta a `Config`
2. `reader.py` varre `source/`, extrai frontmatter e conteúdo
3. `template.py` renderiza o prompt substituindo variáveis
4. `agent.py` envia o prompt ao GPT-4o (com retry 3x)
5. `generator.py` salva o artigo em `artigos/`

### Stack

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | Python 3.11+ |
| AI Agent | [Agno](https://github.com/agno-agi/agno) |
| LLM | GPT-4o (OpenAI) |
| CLI | [Typer](https://typer.tiangolo.com/) |
| Markdown | python-frontmatter |
| Terminal UI | [Rich](https://rich.readthedocs.io/) |
| Lint/Format | Ruff |
| Testes | pytest |
| Pacote | uv / setuptools |

### Estrutura do Projeto

```
src/
├── main.py              # Entry point (carrega .env, chama app)
├── cli.py               # Comando CLI `generate`
├── agent.py             # Agente Agno com retry logic
├── config.py            # Dataclass de configuração
├── logger.py            # Logger estruturado
├── models/
│   └── artigo.py        # Dataclasses Anotacao e Artigo
└── services/
    ├── reader.py        # Leitura de arquivos .md
    ├── generator.py     # Orquestração da geração
    └── template.py      # Renderização de templates

tests/
├── unit/
│   ├── test_reader.py   # 11 testes
│   ├── test_template.py # 6 testes
│   └── test_generator.py# 9 testes
└── integration/
    └── test_cli.py      # 4 testes

source/                  # Anotações de entrada
artigos/                 # Artigos gerados
templates/
└── prompt_template.md  # Template do prompt Agno
```

### Setup Dev

```bash
git clone <repo-url>
cd automacao_artigos
uv sync --group dev
```

### Comandos

```bash
# Rodar o projeto
uv run artigo

# Lint
uv run ruff check .

# Formatar
uv run ruff format .

# Testes
uv run pytest
uv run pytest -v        # verbose
uv run pytest tests/unit/  # só unitários
```

### Testes

30 testes divididos em:

```
tests/
├── unit/               # Testes isolados (mock-free)
│   ├── test_reader.py  # Reader, frontmatter, edge cases
│   ├── test_template.py# Template rendering, erros
│   └── test_generator.py# Slug, montagem, tags
└── integration/
    └── test_cli.py     # CLI flags, diretórios, erros
```

Rodar:
```bash
uv run pytest -v
```

### Convenções

**Código**:
- Line length: 79 chars
- Imports: stdlib → third-party → local
- Ruff rules: E (pycodestyle), F (pyflakes), PL (pylint), I (isort)

**Commits**: Conventional Commits — `feat:`, `fix:`, `chore:`, `refact:`
