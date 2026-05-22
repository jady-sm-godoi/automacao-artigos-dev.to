# Telegram Bot Command Contract

## Interface: Bot do Telegram

O bot expõe os seguintes comandos e handlers. A comunicação é via API do
Telegram (protocolo definido pelo Telegram Bot API).

## Commands

| Command | Args | Description | Handler |
|---------|------|-------------|---------|
| `/start` | — | Mensagem de boas-vindas | `cmd_start()` |
| `/ajuda` | — | Lista comandos disponíveis | `cmd_ajuda()` |
| `/gerar` | — | Executa "artigo generate", retorna artigo | `cmd_gerar()` |
| `/publicar` | `<nome> [--published]` | Publica artigo no Dev.to | `cmd_publicar()` |
| `/listar` | — | Lista arquivos .md em /source | `cmd_listar()` |
| `/status` | — | Contagem de itens em /source | `cmd_status()` |

## Message Handlers

| Content Type | Behavior | Handler |
|-------------|----------|---------|
| Text (< 100 chars) | Rejeita: "Conteúdo muito curto" | `handle_text()` |
| Text (≥ 100 chars) | Salva como .md em /source, confirma | `handle_text()` |
| Photo / Document (image) | Baixa e salva em /source/imagens/ | `handle_image()` |
| Other document | Rejeita: "Apenas imagens são aceitas" | `handle_unsupported()` |

## Error Responses

| Scenario | Response |
|----------|----------|
| Token não configurado | Bot não inicia; erro no console |
| /gerar sem conteúdo | "Nenhuma anotação encontrada em /source" |
| /gerar falha | "Erro ao gerar artigo: {motivo}" |
| /publicar sem artigo | "Artigo não encontrado. Use /listar para ver disponíveis" |
| /publicar sem chave Dev.to | "Chave Dev.to não configurada" |
| API Telegram indisponível | Retry com exponential backoff (via PTB) |

## Response Format

- Texto curto: mensagem de texto normal
- Artigo longo (> 4000 chars): enviar como arquivo .md anexado
- Imagem: confirmação + nome do arquivo salvo
- Erro: mensagem de texto com prefixo "❌ "
