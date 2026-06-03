# Automacao Artigos

**CLI tool em Python** que transforma suas anotações Markdown em artigos
bonitões no estilo Medium usando IA (GPT-4o via Agno) e ainda publica
tudo no Dev.to pra você. ✨

```
anotações.md  →  [Agno + GPT-4o]  →  artigo-medium.md  →  Dev.to
```

## Quick Start 🚀

Bora botar pra rodar em 5 minutos?

**Pré-requisitos**: Python 3.11+ e [uv](https://docs.astral.sh/uv/).

```bash
# 1. Baixar o projeto
git clone <repo-url>
cd automacao_artigos

# 2. Instalar dependências
uv sync

# 3. Configurar chaves de API (crie um arquivo .env na raiz)
echo 'OPENAI_API_KEY="sk-..."' >> .env
echo 'DEVTO_API_KEY="sua-chave-aqui"' >> .env
```

> A chave da Dev.to você pega em: https://dev.to/settings/account →
> "DEV Community API Keys"

```bash
# 4. Gerar um artigo a partir das anotações em source/
artigo generate

# 5. Publicar no Dev.to (como rascunho)
artigo publish github-speckit
```

Pronto! 🎉 Seu artigo saiu do forno e foi pro Dev.to.

---

## Sumário

- [Para Usuários](#para-usuarios)
  - [Instalação](#instalacao)
  - [Uso](#uso)
  - [Gerar Artigo](#gerar-artigo)
  - [Publicar no Dev.to](#publicar-no-devto)
  - [Bot do Telegram](#bot-do-telegram)
  - [Formato das Anotações](#formato-das-anotacoes)
  - [Personalização](#personalizacao)
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

Configure as chaves de API:

```bash
# Crie um arquivo .env na raiz do projeto
OPENAI_API_KEY="sk-..."
DEVTO_API_KEY="sua-chave-aqui"
```

> Obtenha a DEVTO_API_KEY em: https://dev.to/settings/account →
> "DEV Community API Keys"

### Uso

```bash
# Gera artigo a partir da pasta source/
artigo generate

# Publica artigo no Dev.to (como rascunho)
artigo publish github-speckit

# Publica artigo já publicado
artigo publish github-speckit --published

# Inicia o bot do Telegram
artigo bot

# Ajuda
artigo --help
artigo publish --help
```

### Gerar Artigo

```bash
# Pastas personalizadas
artigo generate --source ./minhas-notas --output ./meus-artigos

# Com verbose
artigo generate --verbose

# Template personalizado
artigo generate --template ./meu-template.md
```

### Publicar no Dev.to

```bash
# Publicar como rascunho (padrão)
artigo publish <nome-do-arquivo>

# Publicar direto (visível no feed)
artigo publish <nome-do-arquivo> --published

# Especificar diretório dos artigos
artigo publish <nome> --output ./meus-artigos

# Especificar chave manualmente
artigo publish <nome> --devto-key "minha-chave"
```

O nome do arquivo pode ser com ou sem `.md`. Se não encontrar, o sistema
lista os artigos disponíveis.

### Bot do Telegram

```bash
# Iniciar o bot
artigo bot
```

**Pré-requisito**: Token do bot configurado no `.env`:
```
TELEGRAM_BOT_TOKEN="seu-token-aqui"
```

> Obtenha o token em https://t.me/BotFather → `/newbot`

**Comandos disponíveis no bot:**

| Comando | Descrição |
|---------|-----------|
| `/start` | Mensagem de boas-vindas |
| `/ajuda` | Lista todos os comandos |
| Texto livre | Salva como arquivo .md em /source |
| Imagem | Salva em /source/imagens/ |
| `/gerar` | Gera artigo com as anotações e retorna no chat |
| `/listar` | Lista anotações salvas em /source |
| `/status` | Exibe contagem de anotações e imagens |
| `/publicar <nome>` | Publica artigo no Dev.to (rascunho) |
| `/publicar <nome> --published` | Publica artigo (visível) |

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
O template agora gera artigos com frontmatter YAML compatível com Dev.to
(`title`, `description`, `tags`).

Variáveis disponíveis:

| Variável | Descrição |
|----------|-----------|
| `{{titulo}}` | Título extraído das anotações |
| `{{tags}}` | Tags combinadas |
| `{{conteudo}}` | Conteúdo bruto das anotações |

---

## Para Programadores

### Arquitetura

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  CLI      │───▶│  Reader  │───▶│Generator │───▶│Publisher │───▶│  Dev.to  │
│ (Typer)   │    │(Markdown)│    │(Agno+IA) │    │ (httpx)  │    │   API    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
                      │                              ▲
                      ▼                              │
                 Anotações                      Template
                 .md source/                    prompt.md
```

**Fluxo de Geração**:

1. `cli.py` recebe comando `generate` e monta a `Config`
2. `reader.py` varre `source/`, extrai frontmatter e conteúdo
3. `template.py` renderiza o prompt substituindo variáveis
4. `agent.py` envia o prompt ao GPT-4o (com retry 3x)
5. `generator.py` salva o artigo em `artigos/`

**Fluxo de Publicação**:

1. `cli.py` recebe comando `publish` com nome do artigo
2. `publisher.py` lê o arquivo, extrai frontmatter (title, description, tags)
3. `publisher.py` envia POST para `https://dev.to/api/articles`
4. Resultado exibido: URL e ID do artigo publicado

### Stack

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | Python 3.11+ |
| AI Agent | [Agno](https://github.com/agno-agi/agno) |
| LLM | GPT-4o (OpenAI) |
| CLI | [Typer](https://typer.tiangolo.com/) |
| HTTP | [httpx](https://www.python-httpx.org/) |
| Markdown | python-frontmatter |
| Terminal UI | [Rich](https://rich.readthedocs.io/) |
| Lint/Format | Ruff |
| Testes | pytest |
| Pacote | uv / setuptools |

### Estrutura do Projeto

```
src/
├── main.py              # Entry point (carrega .env, chama app)
├── cli.py               # Comandos CLI `generate` e `publish`
├── agent.py             # Agente Agno com retry logic
├── config.py            # Dataclass de configuração
├── logger.py            # Logger estruturado
├── models/
│   └── artigo.py        # Dataclasses Anotacao e Artigo
└── services/
    ├── reader.py        # Leitura de arquivos .md
    ├── generator.py     # Orquestração da geração
    ├── template.py      # Renderização de templates
    ├── publisher.py     # Publicação no Dev.to via API
    └── telegram_bot.py  # Bot Telegram (handlers, comandos)

tests/
├── unit/
│   ├── test_reader.py
│   ├── test_template.py
│   ├── test_generator.py
│   └── test_publisher.py
└── integration/
    └── test_cli.py

source/                  # Anotações de entrada
artigos/                 # Artigos gerados
templates/
└── prompt_template.md  # Template do prompt Agno (c/ frontmatter Dev.to)
```

### Setup Dev

```bash
git clone <repo-url>
cd automacao_artigos
uv sync --extra dev
```

### Comandos

```bash
# Geração
uv run artigo generate

# Publicação
uv run artigo publish <nome>

# Lint
uv run ruff check .

# Format
uv run ruff format .

# Testes
uv run pytest
uv run pytest -v          # verbose
uv run pytest tests/unit/ # só unitários
```

### Testes

91 testes divididos em:

```
tests/
├── unit/               # Testes isolados (mock-free)
│   ├── test_reader.py  # Reader, frontmatter, edge cases
│   ├── test_template.py# Template rendering, erros
│   ├── test_generator.py# Slug, montagem, tags
│   ├── test_publisher.py# API Dev.to, frontmatter, erros HTTP
│   └── test_telegram_bot.py  # Bot Telegram, handlers, comandos
└── integration/
    └── test_cli.py     # CLI flags, generate, publish, bot
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
- HTTP status codes via `HTTPStatus` (não magic numbers)

**Commits**: Conventional Commits — `feat:`, `fix:`, `chore:`, `refact:`
