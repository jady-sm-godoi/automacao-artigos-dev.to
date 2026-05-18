# CLI Contracts: Artigo Blog Generator

## Command: `generate`

Gera um artigo estilo Medium a partir das anotações em `/source`.

### Usage

```
python -m main generate [OPTIONS]
```

### Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--source` | PATH | `source/` | Diretório com anotações |
| `--output` | PATH | `artigos/` | Diretório para artigos |
| `--template` | PATH | `templates/prompt_template.md` | Template do prompt |
| `--verbose` | FLAG | False | Exibe progresso detalhado |
| `--help` | - | - | Mostra ajuda |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Sucesso - artigo gerado |
| 1 | Erro - falha na geração |

### Examples

```bash
# Uso padrão
python -m main generate

# Com diretórios personalizados
python -m main generate --source ./notas --output ./publicados

# Verbose mode
python -m main generate --verbose
```

### Output

**Success**:
```
✓ Lendo anotações de source/...
✓ Processando 3 arquivos...
✓ Gerando artigo com Agno...
✓ Artigo salvo: artigos/titulo-do-artigo.md
```

**Error - No files**:
```
⚠ Nenhum arquivo .md encontrado em source/
Crie arquivos .md no diretório ou use --source para especificar outro caminho.
```

**Error - API**:
```
✗ Erro na API OpenAI: [mensagem de erro]
Verifique sua OPENAI_API_KEY ou tente novamente.
```

---

## Command: `init`

Inicializa a estrutura de diretórios.

### Usage

```
python -m main init [OPTIONS]
```

### Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--source` | PATH | `source/` | Diretório de anotações |
| `--output` | PATH | `artigos/` | Diretório de artigos |
| `--template` | PATH | `templates/` | Diretório de templates |

### Examples

```bash
python -m main init
```

### Output

```
✓ Criado: source/
✓ Criado: artigos/
✓ Criado: templates/prompt_template.md
Estrutura inicializada!
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Chave da API OpenAI |
| `AGNO_MODEL` | No | Modelo a usar (default: gpt-4o) |