# Quickstart: Artigo Blog Generator

## Pré-requisitos

- Python 3.11+
- Chave de API OpenAI configurada

## Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd automacao_artigos

# Instale dependências
uv sync

# Configure a API key (crie um .env ou exporte)
export OPENAI_API_KEY="sua-chave-aqui"

# (Opcional) Adicione ao seu shell profile
echo 'export OPENAI_API_KEY="sua-chave-aqui"' >> ~/.zshrc
```

## Uso Básico

```bash
# Gere um artigo a partir das anotações em /source
artigo

# Via entry point (após uv sync)
artigo

# Com verbose
artigo --verbose

# Especifique diretórios personalizados
artigo --source ./minhas-notas --output ./meus-artigos
```

## Estrutura de Diretórios

```
.
├── source/          # Suas anotações .md aqui
│   ├── nota-1.md
│   └── tema/
│       └── nota-2.md
├── artigos/         # Artigos gerados aparecem aqui
│   └── titulo-artigo.md
└── templates/
    └── prompt_template.md  # Customize o estilo do artigo
```

## Formato das Anotações

### Basic (sem metadados)

```markdown
# Minhas anotações sobre Python

Notas brutas aqui...

- Ponto importante 1
- Ponto importante 2
```

### Com Frontmatter

```markdown
---
title: "Título do Artigo"
tags: ["python", "tutorial"]
date: 2026-04-29
---

# Minhas anotações

Conteúdo aqui...
```

## Personalização

Edite `templates/prompt_template.md` para alterar o estilo do artigo gerado.

## Comandos

| Comando | Descrição |
|---------|-----------|
| `artigo` | Gera artigo a partir de /source |
| `artigo --help` | Mostra ajuda geral |

| `uv run pytest` | Executa os testes |

## Troubleshooting

### "No API key found"

```bash
export OPENAI_API_KEY="sk-..."
```

### "Directory not found"

O sistema cria automaticamente, mas você pode criar manualmente:

```bash
mkdir -p source artigos templates
```

### Artigo vazio ou muito curto

Verifique se suas anotações têm pelo menos 100 caracteres.