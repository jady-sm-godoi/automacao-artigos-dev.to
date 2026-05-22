# Research: Telegram Bot Integration

## 1. Library Choice: python-telegram-bot

| Aspect | Decision |
|--------|----------|
| **Decision** | `python-telegram-bot` v21+ (async) |
| **Rationale** | Padrão da comunidade Telegram Python. Suporta polling e webhook. Bom ecossistema e documentação. Compatível com asyncio do Python 3.11+ |
| **Alternatives** | `telethon` (focado em client API, não bot API), `aiogram` (async, mas menos ecossistema), raw `httpx` (reimplementar roda) |

## 2. Polling vs Webhook

| Aspect | Decision |
|--------|----------|
| **Decision** | Polling (long polling via `updater.start_polling()`) |
| **Rationale** | Simplicidade de setup — não requer domínio público, SSL/TLS, ou configuração de firewall. Suficiente para uso pessoal/pequeno. |
| **Alternatives** | Webhook requer servidor público com HTTPS, mais complexo para teste local |
| **Future** | Adicionar suporte a webhook como opção se escala for necessária |

## 3. Estrutura de Mensagens

| Aspect | Decision |
|--------|----------|
| **Decision** | Cada mensagem de texto vira um `.md` independente em `/source` |
| **Rationale** | Simples, previsível, sem estado de sessão. Usuário gerencia o que enviar. |
| **Naming** | `<timestamp>-<chat_id>-<seq>.md` |
| **Image naming** | `<timestamp>-<chat_id>-<seq>.<ext>` |

## 4. Geração de Artigo via Bot

| Aspect | Decision |
|--------|----------|
| **Decision** | Comando `/gerar` executa subprocesso `artigo generate` e captura stdout |
| **Rationale** | Reusa a CLI existente sem acoplamento. Arturation gera o arquivo em `/artigos`, depois o bot lê e envia. |
| **Long articles** | Se > 4000 chars, enviar como arquivo `.md` anexado (via `InputFile`) |

## 5. Tratamento de Imagens

| Aspect | Decision |
|--------|----------|
| **Decision** | Download via `bot.get_file(file_id)`, salvar em `/source/imagens/` |
| **Rationale** | API do Telegram fornece file_id e URL para download. Salvar com timestamp único. |
| **Formats** | Aceitar: jpg, png, gif, webp. Rejeitar outros com mensagem clara. |

## 6. Dependências

| Pacote | Versão | Razão |
|--------|--------|-------|
| `python-telegram-bot` | >=21.0 | Core do bot Telegram |
| `httpx` | (já existe) | Download de arquivos do Telegram |

Nenhuma outra dependência nova necessária. O projeto já usa httpx.
