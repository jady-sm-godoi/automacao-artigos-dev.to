# Research: Artigo Blog Generator

## Decisions

### Decision 1: Framework CLI - Typer vs Click

**Choice**: Typer (baseado em Click)

**Rationale**:
- Typer oferece typing automático e documentação via `--help`
- Menos código boilerplate comparado a Click puro
- Integração natural com FastAPI CLI tools
- Suporta async nativamente

**Alternatives considered**:
- Click: Mais baixo nível, mais código para mesma funcionalidade
- argparse: Muito verboso para CLI complexa

---

### Decision 2: Estrutura de Arquivos Markdown

**Choice**: Suporte a frontmatter YAML para metadados

**Rationale**:
- Frontmatter é padrão widely adopted (Jekyll, Hugo, Obsidian)
- Permite título, tags, data, autor sem modificar corpo
- Python library `python-frontmatter` facilita parsing

**Alternatives considered**:
- Metadados no nome do arquivo: Limita flexibilidade
- Seção especial no topo do arquivo: Menos padronizado

---

### Decision 3: Template de Prompt

**Choice**: Arquivo Markdown com placeholders

**Rationale**:
- Editores de texto comum reconhecem `.md`
- Placeholders como `{{conteudo}}` são legíveis
- Fácil de versionar e colaborar

**Format**:
```markdown
# Template de Artigo Medium

## Instruções
Você é um escritor profissional...

## Conteúdo para transformar
{{conteudo}}

## Regras
- Linguagem formal mas acessível
- Parágrafos de 3-4 sentenças
...
```

---

### Decision 4: Manejo de Arquivos de Saída

**Choice**: Usar título do artigo para nome do arquivo, com versionamento numérico

**Rationale**:
- Artigos `titulo-artigo.md`, `titulo-artigo-1.md`, `titulo-artigo-2.md`
- Facilita identificação visual
- Não sobrescreve versões anteriores

**Alternatives considered**:
- Timestamp: Dificulta identificar conteúdo
- UUID: Impossível ler depois

---

### Decision 5: Processamento de Múltiplos Arquivos

**Choice**: Concatenar em ordem alfabética com separadores

**Rationale**:
- Ordem previsível e reproduzível
- Separadores visuais entre fontes diferentes
- Usuário pode controlar ordem via nomes de arquivo

---

## Dependencies

### Required Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| agno | >=2.0 | AI Agent framework |
| openai | >=1.0 | OpenAI API client |
| typer | >=0.9 | CLI framework |
| python-frontmatter | >=1.0 | Parse YAML frontmatter |
| rich | >=13.0 | Terminal output styling |
| click | >=8.0 | Typer dependency |

### Optional

| Library | Purpose |
|---------|---------|
| pytest | Testing |
| pytest-asyncio | Async tests |
| ruff | Linting/formatting |

---

## Best Practices

### Agno Agent Setup

```python
from agno import Agent, Model

agent = Agent(
    model=Model(model_name="gpt-4o"),
    markdown=True,
)
```

### CLI Structure

```
python -m main generate          # Gera artigo
python -m main generate --help   # Mostra ajuda
python -m main init              # Cria estrutura inicial
```

### Error Handling

- Validação de arquivos antes de processar
- Mensagens claras de erro
- Exit codes apropriados (0 sucesso, 1 erro)