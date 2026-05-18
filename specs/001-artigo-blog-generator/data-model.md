# Data Model: Artigo Blog Generator

## Entities

### Anotacao

Arquivo markdown de entrada com conteúdo do usuário.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| caminho | Path | Yes | Caminho completo do arquivo |
| nome | str | Yes | Nome do arquivo sem extensão |
| conteudo | str | Yes | Corpo do markdown (sem frontmatter) |
| frontmatter | dict | No | Metadados YAML (título, tags, data) |
| tamanho | int | Yes | Tamanho em caracteres do conteúdo |

**Validation Rules**:
- Arquivo deve ter extensão `.md`
- Conteúdo deve ter pelo menos 100 caracteres (senão ignorar com warning)
- Arquivo vazio (0 bytes) é ignorado silenciosamente

**Relationships**:
- Zero ou mais Anotacoes são processadas para gerar um Artigo

---

### Artigo

Arquivo markdown de saída gerado.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| titulo | str | Yes | Título do artigo (extraído ou gerado) |
| conteudo | str | Yes | Corpo do artigo formatado |
| tags | list[str] | No | Tags extraídas ou definidas |
| data_criacao | datetime | Yes | Data de geração |
| fontes | list[Path] | Yes | Lista de arquivos de origem |

**Validation Rules**:
- Título deve ter entre 5 e 200 caracteres
- Conteúdo deve ter pelo menos 200 caracteres

**Relationships**:
- Gerado a partir de uma ou mais Anotacoes

---

### Template

Arquivo de prompt configurável para o agente Agno.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| caminho | Path | Yes | Caminho do arquivo template |
| variaveis | list[str] | Yes | Lista de placeholders esperados |

**Placeholders esperados**:
- `{{conteudo}}`: Anotações a serem transformadas
- `{{titulo}}`: Título fornecido ou "Artigo sem título"
- `{{tags}}`: Tags extraídas ou vazio

---

### Configuracao

Parâmetros de execução.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| source_dir | Path | "source" | Diretório de anotações |
| output_dir | Path | "artigos" | Diretório de saída |
| template_path | Path | "templates/prompt_template.md" | Template do prompt |
| modelo | str | "gpt-4o" | Modelo OpenAI |
| verbose | bool | True | Exibir progresso |

**Sources**:
- Valores padrão hardcoded
- Podem ser sobrescritos via CLI args

---

## State Transitions

### Fluxo de Processamento

```
[CLI Input] → [Validate Dirs] → [Load Config] → [Read Anotacoes]
      ↓
[Process Template] → [Call Agent] → [Generate Artigo] → [Save Output]
      ↓
[Report Success/Error]
```

### Estados de Erro

| Estado | Descrição | Ação |
|--------|-----------|------|
| DIR_NOT_FOUND | Diretório source não existe | Criar e avisar usuário |
| NO_FILES | Nenhum arquivo .md encontrado | Mensagem informativa |
| TEMPLATE_MISSING | Template não encontrado | Erro com path do template |
| API_ERROR | Erro na API OpenAI | Log do erro, retry opcional |
| CONTENT_TOO_SHORT | Anotações muito curtas | Warning, continua processamento |

---

## File System Structure

```
project/
├── source/                    # Anotações de entrada
│   ├── nota-1.md
│   └── pasta/
│       └── nota-2.md
├── artigos/                   # Artigos gerados
│   └── titulo-artigo.md
├── templates/
│   └── prompt_template.md     # Template do Agno
└── src/
    └── ...
```

---

## Data Validation

### Frontmatter Schema

```yaml
---
titulo: "Título Opcional"
tags: ["tag1", "tag2"]
data: 2026-04-29
autor: "Nome do Autor"
---
```

### Output Article Schema

```markdown
---
title: "Título do Artigo"
date: 2026-04-29
tags: ["tag1", "tag2"]
sources: ["source/nota-1.md", "source/pasta/nota-2.md"]
---

# Título do Artigo

[Conteúdo gerado em estilo Medium]
```