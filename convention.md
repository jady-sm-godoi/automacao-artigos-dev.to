---
title: Coding Conventions
date: 2026-04-29
tags:
  - python
  - convencoes
project: 
---

# Coding Conventions

## Python

### Formatação
- Linha máxima: 79 caracteres
- Usar `# noqa: E501` para linhas mais longas quando necessário
- Ruff para lint: `ruff check` — flags E501, PLR2004 e outros
- Ruff para formatação: `ruff format` (tenta quebrar linhas longas automaticamente)
- Rodar `task lint` antes de commitar; `task format` (`ruff check --fix && ruff format .`)
- Deixar uma linha em branco ao final de um arquivo python

### Imports
- Todos os imports no topo do arquivo
- Ordem:stdlib → third-party → local
- Só permitir imports inline:
	- onde não for causar dependência cíclica
	- Onde só fizer sentido fazer o import para uma condição específica

### Testes
- Arquivos: `tests_<app>__<type>.py` (ex: `tests_event__models.py`)
- Layout: `src/tests/<app>/` — uma subpasta por app
- Usar `HTTPStatus` para status codes (não magic numbers)
- Parâmetros via `@pytest.mark.parametrize`
- Markers: `slow`, `events`
- Timeout: 90-180s para suites grandes
- Magic numbers (>2) em asserts: suprimir com `# noqa: PLR2004` ou extrair constante

### Ruff
```bash
task lint   # verificar
task format # formatar
```

`ruff check --fix` corrige issues auto-fixable (imports, etc). `ruff format` apenas formata style.
Não usar `ruff format` sozinho — `task format` faz ambos.

#### Regras relevantes
| Regra | Gatilho | Supressão |
|-------|---------|-----------|
| E501 | Linha >79 chars | `# noqa: E501` (após esgotar quebra de linha) |
| PLR2004 | Magic number em comparação | Extrair constante ou `# noqa: PLR2004` |

Verificar com: `ruff check --select E501,PLR2004 <file>`.

---

## git

### Commits
- Conventional Commits (Add:/fix:/chore:/refact:/feat:)
- Subject ≤50 caracteres (guideline, ~80% aderência)
- Body apenas se necessário

### Branches
- `dev`, `hml`, `main` — branches ativas